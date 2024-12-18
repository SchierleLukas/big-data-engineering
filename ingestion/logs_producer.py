import os
from confluent_kafka import Producer
import json
import time
import random

# Zugriff auf die Umgebungsvariable
bootstrap_servers = os.getenv('BOOTSTRAP_SERVERS', 'localhost:9092')

# Konfiguration des Producers
def delivery_report(err, msg):
    """
    Callback-Funktion, die ausgeführt wird, wenn eine Nachricht 
    erfolgreich gesendet wurde oder ein Fehler aufgetreten ist.
    """
    if err is not None:
        print(f'Nachricht fehlgeschlagen: {err}')
    else:
        print(f'Nachricht erfolgreich gesendet: {msg.topic()} [{msg.partition()}]')

producer_config = {
    'bootstrap.servers': bootstrap_servers
}

# Erstelle den Producer
producer = Producer(producer_config)

# Simuliere Logs
try:
    while True:
        log = {"timestamp": time.time(), "level": "INFO", "message": "Sample log"}
        producer.produce('server-logs', key=str(time.time()), value=json.dumps(log), callback=delivery_report)
        
        # Stellt sicher, dass die Nachricht gesendet wird
        producer.poll(0)
        
        print(f"Sent: {log}")
        time.sleep(random.uniform(0.1, 5))  # Random sleep between 0.1 and 5 seconds
except KeyboardInterrupt:
    # Warte darauf, dass alle Nachrichten gesendet wurden, bevor das Programm beendet wird
    print("Beenden des Producers...")
    producer.flush()
