# big-data-engineering
This repository is used for the exam in the module "W3M20027 Big Data Engineering"

# Systemarchitektur

```mermaid
graph TD
    subgraph Ingestion_Layer
        A[Server Logs] --> B[Apache Kafka]
    end

    subgraph Stream_Processing_Layer
        B --> C[Apache Spark Streaming]
        C --> D[Anomaly Detection Algorithm]
    end

    subgraph Serving_Layer
        D --> E[MariaDB]
    end

    subgraph Visualization_Layer
        E --> F[Grafana Dashboard]
    end

    style A fill:#f9f,stroke:#333,stroke-width:4px
    style B fill:#fc9,stroke:#333,stroke-width:2px
    style C fill:#9cf,stroke:#333,stroke-width:2px
    style D fill:#cfc,stroke:#333,stroke-width:2px
    style E fill:#ffc,stroke:#333,stroke-width:2px
    style F fill:#ccf,stroke:#333,stroke-width:2px
