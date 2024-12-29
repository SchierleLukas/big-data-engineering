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
log_weights = [0.1, 0.6, 0.2, 0.1]  # Normal weights for log levels

# Error wave configuration
error_wave_active = False
error_wave_start_time = None

# Set maximum runtime
start_time = time.time()
max_runtime = 5 * 60  # 5 minutes in seconds

try:
    while True:
        current_time = time.time()

        # Stop after maximum runtime
        if current_time - start_time > max_runtime:
            print("Maximum runtime reached. Shutting down...")
            break

        # Check if an error wave should start
        if not error_wave_active:
            if random.random() < 0.01:  # Approx. 1% chance per iteration to start an error wave
                error_wave_active = True
                error_wave_start_time = current_time
                print("Error wave started!")
        
        # Adjust log weights if error wave is active
        if error_wave_active:
            log_weights = [0.05, 0.1, 0.2, 0.65]  # Increase ERROR log probability
            if current_time - error_wave_start_time > 45:  # Error wave lasts for 45 seconds
                error_wave_active = False
                log_weights = [0.1, 0.6, 0.2, 0.1]  # Reset to normal weights
                print("Error wave ended.")

        # Generate a log
        log_level = random.choices(log_levels, weights=log_weights, k=1)[0]
        log = {"timestamp": current_time, "level": log_level, "message": f"Sample {log_level.lower()} log"}
        producer.produce(kafka_topic, key=str(current_time), value=json.dumps(log), callback=delivery_report)

        # Ensure the message is sent
        producer.poll(0)

        print(f"Sent: {log}")
        time.sleep(random.uniform(0.1, 5))  # Random sleep between 0.1 and 5 seconds

except KeyboardInterrupt:
    # Wait for all messages to be sent before terminating the program
    print("Shutting down producer...")
    producer.flush()
