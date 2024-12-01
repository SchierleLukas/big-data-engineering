from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
import os

# Create Spark session
spark = SparkSession.builder \
    .appName("KafkaLogLevelCount") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Set Spark logging level to WARN
spark.sparkContext.setLogLevel("WARN")

# Get Kafka broker addresses from environment variable
kafka_brokers = os.environ.get('BOOTSTRAP_SERVERS')

# Define schema for log messages
log_schema = StructType() \
    .add("timestamp", DoubleType()) \
    .add("level", StringType()) \
    .add("message", StringType())

# Read from Kafka
kafka_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_brokers) \
    .option("subscribe", "server-logs") \
    .option("startingOffsets", "earliest") \
    .load()

# Parse messages and apply schema
parsed_stream = kafka_stream.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), log_schema).alias("data")) \
    .select("data.*")

# Convert timestamp from seconds since epoch to TimestampType
parsed_stream = parsed_stream.withColumn("timestamp", col("timestamp").cast(TimestampType()))

# Filter only INFO level logs
info_logs = parsed_stream.filter(col("level") == "INFO")

# Count INFO logs in sliding window
windowed_counts = info_logs \
    .withWatermark("timestamp", "30 seconds") \
    .groupBy(
        window(col("timestamp"), "30 seconds", "10 seconds")
    ).count()

# Output to console
console_query = windowed_counts.writeStream \
    .outputMode("update") \
    .format("console") \
    .option("truncate", "false") \
    .trigger(processingTime='10 seconds') \
    .start()

# # Write to MariaDB
# jdbc_url = "jdbc:mysql://docker-mariadb-1:3306/logs"
# jdbc_properties = {
#     "user": "root",
#     "password": "password",
#     "driver": "org.mariadb.jdbc.Driver"
# }

# def write_to_mariadb(batch_df, batch_id):
#     batch_df.write.jdbc(url=jdbc_url, table="log_counts", mode="append", properties=jdbc_properties)

# mariadb_query = windowed_counts.writeStream \
#     .outputMode("update") \
#     .foreachBatch(write_to_mariadb) \
#     .trigger(processingTime='10 seconds') \
#     .start()

# Start streaming
console_query.awaitTermination()