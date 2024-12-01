import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window
from pyspark.sql.types import StructType, StringType, TimestampType

# Umgebungsvariablen einlesen
spark_master_url = os.getenv('SPARK_MASTER_URL', 'spark://spark-master:7077')
kafka_brokers = os.getenv('BOOTSTRAP_SERVERS', 'kafka-broker-1:9092,kafka-broker-2:9093')

# SparkSession initialisieren
spark = SparkSession.builder \
    .appName("KafkaLogLevelCount") \
    .master(spark_master_url) \
    .getOrCreate()

# Schema für die Kafka-Nachrichten definieren
log_schema = StructType() \
    .add("timestamp", TimestampType()) \
    .add("level", StringType()) \
    .add("message", StringType())

# Kafka-Stream lesen
kafka_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_brokers) \
    .option("subscribe", "server-logs") \
    .option("startingOffsets", "earliest") \
    .load()

# Nachrichten parsen und Schema anwenden
parsed_stream = kafka_stream.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), log_schema).alias("data")) \
    .select("data.*")

# Nur Nachrichten mit Log-Level "INFO" filtern
info_logs = parsed_stream.filter(col("level") == "INFO")

# Anzahl der "INFO"-Logs im Sliding Window berechnen
windowed_counts = info_logs \
    .withWatermark("timestamp", "30 seconds") \
    .groupBy(
        window(col("timestamp"), "30 seconds", "10 seconds")
    ).count()

# Ausgabe auf der Konsole
query = windowed_counts.writeStream \
    .outputMode("update") \
    .format("console") \
    .option("truncate", "false") \
    .start()

# Streaming starten
query.awaitTermination()
