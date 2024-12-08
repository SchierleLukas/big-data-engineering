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
    .select("data.*") \
    .withColumn("timestamp", col("timestamp").cast(TimestampType())) \
    .filter(col("level") == "INFO")

# Count INFO logs in sliding window
windowed_counts = parsed_stream \
    .withWatermark("timestamp", "30 seconds") \
    .groupBy(
        window(col("timestamp"), "30 seconds", "15 seconds")
    ).count()

# Flatten the window struct
flattened_counts = windowed_counts.select(
    col("window.start").alias("window_start"),
    col("window.end").alias("window_end"),
    col("count")
)

# Output to console
console_query = flattened_counts.writeStream \
    .outputMode("update") \
    .format("console") \
    .option("truncate", "false") \
    .trigger(processingTime='10 seconds') \
    .start()


def write_to_mariadb(batch_df, epoch_id):
    jdbc_url = "jdbc:mysql://mariadb:3306/logs"
    
    connection_properties = {
        "user": "root",
        "password": "password",
        "driver": "com.mysql.cj.jdbc.Driver"
    }

    try:
        batch_df.select(
            col("window_start").cast("timestamp"),
            col("window_end").cast("timestamp"),
            col("count").cast("bigint")
        ).write \
            .format("jdbc") \
            .mode("append") \
            .option("url", jdbc_url) \
            .option("dbtable", "log_data") \
            .options(**connection_properties) \
            .save()
    except Exception as e:
        print(f"Error writing batch {epoch_id}: {str(e)}")

mariadb_query = flattened_counts.writeStream \
    .foreachBatch(write_to_mariadb) \
    .outputMode("update") \
    .trigger(processingTime="15 seconds") \
    .start()

spark.streams.awaitAnyTermination()