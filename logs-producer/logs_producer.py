import os
from confluent_kafka import Producer
import json
import time
import random

# Access the environment variables
bootstrap_servers = os.getenv('BOOTSTRAP_SERVERS', 'kafka-broker-1:9092,kafka-broker-2:9093')
kafka_topic = os.getenv('KAFKA_TOPIC', 'server-logs')

# Producer configuration
producer_config = {
    'bootstrap.servers': bootstrap_servers
}

# Create the producer
producer = Producer(producer_config)

# Callback function for message delivery
def delivery_report(err, msg):
    """
    Callback function that is executed when a message
    has been successfully delivered or when an error occurs.
    """
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message successfully delivered: {msg.topic()} [{msg.partition()}]')

# Settings for log generation
log_levels = ["DEBUG", "INFO", "WARN", "ERROR"]
normal_weights = [0.1, 0.6, 0.2, 0.1]
error_weights = [0.05, 0.1, 0.2, 0.65]
error_wave_active = False
error_wave_duration = 90
error_wave_start = None

# Keep simulating logs until KeyboardInterrupt
try:
    while True:
        now = time.time()

        # Activate Error wave by 1% chance, if not already active
        if not error_wave_active and random.random() < 0.01:
            error_wave_active = True
            error_wave_start = now
            print("Error wave started!")

        # Determine current weights for log levels
        if error_wave_active:
            current_weights = error_weights
            # End error wave after duration
            if now - error_wave_start > error_wave_duration:
                error_wave_active = False
                current_weights = normal_weights
                print("Error wave ended.")
        else:
            current_weights = normal_weights

        # Generate log
        log_level = random.choices(log_levels, weights=current_weights, k=1)[0]
        log = {"timestamp": now, "level": log_level, "message": f"Sample {log_level} log"}
        producer.produce(kafka_topic, key=str(now), value=json.dumps(log), callback=delivery_report)
        producer.poll(0)

        print(f"Sent: {log}")
        time.sleep(random.uniform(0.1, 5))

except KeyboardInterrupt:
    # Wait for all messages to be sent before terminating the program
    print("Shutting down producer...")
    producer.flush()
