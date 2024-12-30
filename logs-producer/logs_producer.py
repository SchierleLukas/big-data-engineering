import os
from confluent_kafka import Producer
import json
import time
import random

# Environment-Variable
bootstrap_servers = os.getenv('BOOTSTRAP_SERVERS', 'kafka-broker-1:9092,kafka-broker-2:9093')
kafka_topic = os.getenv('KAFKA_TOPIC', 'server-logs')

# Konfiguration des Producers
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

# Erzeugung des Producers
producer = Producer(producer_config)

# Simulierung der Log-Level mit Gewichtungen
log_levels = ["DEBUG", "INFO", "WARN", "ERROR"]
log_weights = [0.1, 0.6, 0.2, 0.1]  # Definition der normalen Gewichtung der Log-Level

error_wave_active = False
error_wave_start_time = None

# Definition der maximalen Laufzeit
start_time = time.time()
max_runtime = 5 * 60  # 5 Minuten in Sekunden

try:
    while True:
        current_time = time.time()

        # Stop nach maximaler Laufzeit
        if current_time - start_time > max_runtime:
            print("Maximum runtime reached. Shutting down...")
            break

        # Mögliche Error-Wave-Aktivierung
        if not error_wave_active:
            if random.random() < 0.01:  # Definition der Error-Wave-Wahrscheinlichkeit
                error_wave_active = True
                error_wave_start_time = current_time
                print("Error wave started!")
        
        # Anpassung der Gewichtung, falls Error-Wave aktiv ist
        if error_wave_active:
            log_weights = [0.05, 0.1, 0.2, 0.65]  # Erhöhung der Error-Wahrscheinlichkeit
            if current_time - error_wave_start_time > 45:  # Definition der Error-Wave-Dauer
                error_wave_active = False
                log_weights = [0.1, 0.6, 0.2, 0.1]  # Zurücksetzen der Gewichtung
                print("Error wave ended.")

        # Log-Generierung
        log_level = random.choices(log_levels, weights=log_weights, k=1)[0]
        log = {"timestamp": current_time, "level": log_level, "message": f"Sample {log_level.lower()} log"}
        producer.produce(kafka_topic, key=str(current_time), value=json.dumps(log), callback=delivery_report)

        producer.poll(0)

        print(f"Sent: {log}")
        time.sleep(random.uniform(0.1, 5))  # Definition des Intervalls zwischen den Log-Nachrichten

except KeyboardInterrupt:
    # Warten, dass alle Nachrichten gesendet sind, bevor das Programm beendet wird.
    print("Shutting down producer...")
    producer.flush()
