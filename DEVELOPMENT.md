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

1. Open a terminal in the MariaDB container and start a bash session:
    ```sh
    /bin/bash
    ```

2. Connect to the MariaDB server:
    ```sh
    mysql -u root -p
    ```

3. Enter password "password" when prompted.

4. Show all databases:
    ```sql
    SHOW DATABASES;
    ```

5. Select the database you want to view, for example `logs`:
    ```sql
    USE logs;
    ```

6. List the tables in the selected database:
    ```sql
    SHOW TABLES;
    ```

7. View the contents of a specific table, for example `log_data`:
    ```sql
    SELECT * FROM log_data;
    ```

## Add or Edit a Dashboard in Grafana

To add or edit a dashboard in Grafana and ensure it is persistent in the repository and available when the project is restarted with Docker Compose, follow these steps:

1. **Access Grafana**:
    - Open `http://localhost:3000` in your browser.
    - Log in with the default credentials `admin`/`admin`.

2. **Create or Edit a Dashboard**:
    - Create a new dashboard or edit an existing one as needed.
    - Save the dashboard.

3. **Export the Dashboard**:
    - Go to the dashboard settings and select `JSON Model`.
    - Copy the JSON content.

4. **Save the JSON to the Repository**:
    - Create a new JSON file or update an existing one in the `grafana/provisioning/dashboards/` directory. For example, `grafana/provisioning/dashboards/my_dashboard.json`.
    - Paste the copied JSON content into this file and save it.

5. **Check the `dashboards.yaml` (Optional)**:
    - Ensure that the `grafana/provisioning/dashboards/dashboards.yaml` file includes the path to your new or updated dashboard JSON file. For example:
      ```yaml
      apiVersion: 1

      providers:
        - name: "default"
          orgId: 1
          folder: ""
          type: file
          disableDeletion: false
          editable: true
          options:
            path: /etc/grafana/provisioning/dashboards
      ```

6. **Restart Grafana**:
    - Restart the Grafana service to apply the changes:
      ```sh
      docker compose restart grafana
      ```
