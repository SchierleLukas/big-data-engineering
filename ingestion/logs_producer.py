import os
from confluent_kafka import Producer
import json
import time
import random

# Access the environment variable
bootstrap_servers = os.getenv('BOOTSTRAP_SERVERS', 'kafka-broker-1:9092,kafka-broker-2:9093')
kafka_topic = os.getenv('KAFKA_TOPIC', 'server-logs')

# Producer configuration
def delivery_report(err, msg):
    """
    Callback function that is executed when a message
    has been successfully delivered or when an error occurs.
    """
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message successfully delivered: {msg.topic()} [{msg.partition()}]')

producer_config = {
    'bootstrap.servers': bootstrap_servers
}

# Create the producer
producer = Producer(producer_config)

# Simulate logs with weighting
log_levels = ["DEBUG", "INFO", "WARN", "ERROR"]
log_weights = [0.1, 0.6, 0.2, 0.1]  # Weights for log levels

try:
    while True:
        log_level = random.choices(log_levels, weights=log_weights, k=1)[0]
        log = {"timestamp": time.time(), "level": log_level, "message": f"Sample {log_level.lower()} log"}
        producer.produce(kafka_topic, key=str(time.time()), value=json.dumps(log), callback=delivery_report)
        
        # Ensure the message is sent
        producer.poll(0)
        
        print(f"Sent: {log}")
        time.sleep(random.uniform(0.1, 5))  # Random sleep between 0.1 and 5 seconds
except KeyboardInterrupt:
    # Wait for all messages to be sent before terminating the program
    print("Shutting down producer...")
    producer.flush()
