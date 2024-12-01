# Cheat-Sheet for debugging

## Validate if kafka-broker is publishing messages

In one of the kafka brokers terminals run
1. /bin/bash
1. kafka-console-consumer --bootstrap-server kafka-broker-1:9092 --topic server-logs --from-beginning