from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
import os

# Read environment variables...
# for kafka
kafka_bootstrap_servers = os.environ.get('BOOTSTRAP_SERVERS', 'kafka-broker-1:9092,kafka-broker-2:9093')
kafka_topic = os.getenv('KAFKA_TOPIC', 'server-logs')

# for spark
spark_master_url = os.environ.get('SPARK_MASTER_URL', 'spark://spark-master:7077')

# for mariadb
mariadb_url = os.environ.get('MARIADB_URL', 'jdbc:mysql://mariadb:3306/logs')
mariadb_user = os.environ.get('MARIADB_USER')
mariadb_password = os.environ.get('MARIADB_PASSWORD')

# Create Spark session with reduced resources for local deployment
spark = SparkSession.builder \
    .appName("KafkaLogLevelCount") \
    .master(spark_master_url) \
    .config("spark.executor.cores", "1") \
    .config("spark.executor.memory", "1g") \
    .getOrCreate()

# Set Spark logging level to WARN to reduce console output
spark.sparkContext.setLogLevel("WARN")

# Define schema for log messages
log_schema = StructType([
    StructField("timestamp", DoubleType(), True),
    StructField("level", StringType(), True),
    StructField("message", StringType(), True)
])

# Read from Kafka
kafka_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic) \
    .option("startingOffsets", "earliest") \
    .load()

# Parse messages and apply schema
parsed_stream = kafka_stream.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), log_schema).alias("data")) \
    .select("data.*") \
    .withColumn("timestamp", col("timestamp").cast(TimestampType()))

# Aggregate log counts by level and time window
windowed_counts = parsed_stream \
    .withWatermark("timestamp", "30 seconds") \
    .groupBy(
        window(col("timestamp"), "30 seconds", "15 seconds"), # 30 seconds windows sliding every 15 seconds
        ) \
    .agg(
        count(when(col("level") == "INFO", 1)).alias("INFO_count"),
        count(when(col("level") == "ERROR", 1)).alias("ERROR_count"),
        count(when(col("level") == "DEBUG", 1)).alias("DEBUG_count"),
        count(when(col("level") == "WARN", 1)).alias("WARN_count")
    ) \
    .select(
        col("window.start").alias("window_start"),
        col("window.end").alias("window_end"),
        col("INFO_count"),
        col("ERROR_count"),
        col("DEBUG_count"),
        col("WARN_count")
    )

# Output to console
console_query = windowed_counts.writeStream \
    .outputMode("update") \
    .format("console") \
    .option("truncate", "false") \
    .trigger(processingTime='15 seconds') \
    .start()

# Function to write logs to MariaDB
def write_to_mariadb(batch_df, epoch_id):
    connection_properties = {
        "user": mariadb_user,
        "password": mariadb_password,
        "driver": "com.mysql.cj.jdbc.Driver"
    }

    try:
        batch_df.write \
            .format("jdbc") \
            .mode("append") \
            .option("url", mariadb_url) \
            .option("dbtable", "log_data") \
            .options(**connection_properties) \
            .save()
    except Exception as e:
        print(f"Error writing batch {epoch_id}: {str(e)}")

# Write aggregated data to MariaDB
mariadb_query = windowed_counts.writeStream \
    .foreachBatch(write_to_mariadb) \
    .outputMode("update") \
    .trigger(processingTime="15 seconds") \
    .start()

# Wait for termination
spark.streams.awaitAnyTermination()
