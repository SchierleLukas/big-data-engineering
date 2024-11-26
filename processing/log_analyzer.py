from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col

spark = SparkSession.builder \
    .appName("LogAnalyzer") \
    .getOrCreate()

schema = "timestamp DOUBLE, level STRING, message STRING"

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "server-logs") \
    .load()

logs = df.selectExpr("CAST(value AS STRING)").select(from_json(col("value"), schema).alias("log")).select("log.*")

logs.writeStream \
    .outputMode("append") \
    .format("console") \
    .start() \
    .awaitTermination()
