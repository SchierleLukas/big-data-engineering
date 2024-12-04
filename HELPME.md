# Cheat-Sheet for debugging
## Validate Kafka Broker Message Publishing

To validate if the Kafka broker is publishing messages, follow these steps:

1. Open a terminal and start a bash session:
    ```sh
    /bin/bash
    ```

2. Run the Kafka console consumer to read messages from the beginning of the `server-logs` topic:
    ```sh
    kafka-console-consumer --bootstrap-server kafka-broker-1:9092 --topic server-logs --from-beginning
    ```

## View inside the MariaDB

To view the contents of the MariaDB, follow these steps:

1. Open a terminal and connect to the MariaDB server:
    ```sh
    mysql -u root -p
    ```

2. Enter password "password" when prompted.

3. Show all databases:
    ```sql
    SHOW DATABASES;
    ```

4. Select the database you want to view, for example `logs`:
    ```sql
    USE logs;
    ```

5. List the tables in the selected database:
    ```sql
    SHOW TABLES;
    ```

6. View the contents of a specific table, for example `logs_count`:
    ```sql
    SELECT * FROM logs_count;
    ```