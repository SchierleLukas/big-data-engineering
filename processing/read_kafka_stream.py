from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Initialize Spark Session
spark = SparkSession \
    .builder \
    .appName("KafkaStreamReader") \
    .getOrCreate()

# Create streaming DataFrame from Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka-broker-1:9092") \
    .option("subscribe", "server-logs") \
    .option("startingOffsets", "earliest") \
    .load()

# Convert value to string for readability
query = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
    .writeStream \
    .format("console") \
    .option("truncate", "false") \
    .start()

# Wait for the streaming to finish
query.awaitTermination()