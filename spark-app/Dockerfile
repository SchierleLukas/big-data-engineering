FROM bitnami/spark:3.5.3

# Install Python, pip, and wget
USER root
RUN apt-get update && apt-get install -y python3 python3-pip wget

# Set version environment variables for integration of Kafka
ENV KAFKA_CLIENT_VERSION=2.8.1
ENV SPARK_VERSION=3.5.3
ENV SCALA_VERSION=2.12

# Download necessary JARs for Kafka Integration
RUN cd /opt/bitnami/spark/jars/ && \
    wget https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_${SCALA_VERSION}/${SPARK_VERSION}/spark-sql-kafka-0-10_${SCALA_VERSION}-${SPARK_VERSION}.jar && \
    wget https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/${KAFKA_CLIENT_VERSION}/kafka-clients-${KAFKA_CLIENT_VERSION}.jar && \
    wget https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.12.0/commons-pool2-2.12.0.jar && \
    wget https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_${SCALA_VERSION}/${SPARK_VERSION}/spark-token-provider-kafka-0-10_${SCALA_VERSION}-${SPARK_VERSION}.jar && \
    wget https://repo1.maven.org/maven2/org/apache/spark/spark-streaming-kafka-0-10_${SCALA_VERSION}/${SPARK_VERSION}/spark-streaming-kafka-0-10_${SCALA_VERSION}-${SPARK_VERSION}.jar

# Set MySQL connector version
ENV MYSQL_CONNECTOR_VERSION=8.0.33

# Download MySQL connector (, which is compatible with MariaDB)
RUN wget https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/${MYSQL_CONNECTOR_VERSION}/mysql-connector-j-${MYSQL_CONNECTOR_VERSION}.jar -P /opt/bitnami/spark/jars/

# Set the working directory
WORKDIR /app

# Copy Python dependencies
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the Spark application
COPY logs_analyzer_spark.py logs_analyzer_spark.py

# Switch back to non-root user
USER 1001

# Set the JARs paths
ENV JARS_PATHS="/opt/bitnami/spark/jars/spark-sql-kafka-0-10_${SCALA_VERSION}-${SPARK_VERSION}.jar,\
/opt/bitnami/spark/jars/kafka-clients-${KAFKA_CLIENT_VERSION}.jar,\
/opt/bitnami/spark/jars/commons-pool2-2.12.0.jar,\
/opt/bitnami/spark/jars/spark-token-provider-kafka-0-10_${SCALA_VERSION}-${SPARK_VERSION}.jar,\
/opt/bitnami/spark/jars/spark-streaming-kafka-0-10_${SCALA_VERSION}-${SPARK_VERSION}.jar,\
/opt/bitnami/spark/jars/mysql-connector-j-${MYSQL_CONNECTOR_VERSION}.jar"

# Define the command to run the Spark application
CMD spark-submit --jars ${JARS_PATHS} logs_analyzer_spark.py
