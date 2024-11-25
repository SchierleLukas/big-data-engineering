# big-data-engineering
This repository is used for the exam in the module "W3M20027 Big Data Engineering"

# Systemarchitektur

```mermaid
graph TD
    subgraph Ingestion_Layer
        A1[Log-Datenquelle 1] -->|Sendet Logs| B[Apache Kafka]
        A2[Log-Datenquelle 2] -->|Sendet Logs| B
        A3[Log-Datenquelle 3] -->|Sendet Logs| B
    end

    subgraph Stream_Processing_Layer
        B -->|Konsumiert Daten| C[Apache Spark Streaming]
        C -->|Verarbeitet Daten| D[Transformierte Daten]
    end

    subgraph Long-Term_Storage
        B -->|Archiviert Logs| G[Hadoop HDFS]
    end

    subgraph Serving_Layer
        D -->|Speichert aggregierte Ergebnisse| E[MariaDB]
    end

    subgraph Dashboard
        E -->|Abfrage der Daten| F[Grafana / Web-Dashboard]
    end

    G -->|Batch-Verarbeitung| H[Apache Spark Batch]
    H -->|Langzeit-Analysen| E

# End Systemarchitektur
