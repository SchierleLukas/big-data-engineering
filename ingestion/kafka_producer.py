from kafka import KafkaProducer
import json
import time

# Verbinde mit Kafka
producer = KafkaProducer(bootstrap_servers='localhost:9092',
                          value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Simuliere Logs
while True:
    log = {"timestamp": time.time(), "level": "INFO", "message": "Sample log"}
    producer.send('server-logs', log)
    print(f"Sent: {log}")
    time.sleep(1)
