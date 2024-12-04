FROM bitnami/spark:3.5.3

# Install Python, pip, and wget
USER root
RUN apt-get update && apt-get install -y python3 python3-pip wget

# Set version environment variables
ENV KAFKA_CLIENT_VERSION=2.8.1
ENV SPARK_VERSION=3.5.3
ENV SCALA_VERSION=2.12

# Download necessary JARs for Kafka Integration
RUN wget https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_${SCALA_VERSION}/${SPARK_VERSION}/spark-sql-kafka-0-10_${SCALA_VERSION}-${SPARK_VERSION}.jar -P /opt/bitnami/spark/jars/ && \
    wget https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/${KAFKA_CLIENT_VERSION}/kafka-clients-${KAFKA_CLIENT_VERSION}.jar -P /opt/bitnami/spark/jars/ && \
    wget https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.12.0/commons-pool2-2.12.0.jar -P /opt/bitnami/spark/jars/ && \
    wget https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_${SCALA_VERSION}/${SPARK_VERSION}/spark-token-provider-kafka-0-10_${SCALA_VERSION}-${SPARK_VERSION}.jar -P /opt/bitnami/spark/jars/ && \
    wget https://repo1.maven.org/maven2/org/apache/spark/spark-streaming-kafka-0-10_${SCALA_VERSION}/${SPARK_VERSION}/spark-streaming-kafka-0-10_${SCALA_VERSION}-${SPARK_VERSION}.jar -P /opt/bitnami/spark/jars/

# Download MariaDB JDBC driver
RUN wget https://downloads.mariadb.com/Connectors/java/connector-java-2.7.4/mariadb-java-client-2.7.4.jar -P /opt/bitnami/spark/jars/

# Copy Python dependencies and install them
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Copy the Spark application
COPY log_analyzer_spark.py /app/log_analyzer_spark.py

ENV JARS_PATHS="/opt/bitnami/spark/jars/spark-sql-kafka-0-10_${SCALA_VERSION}-${SPARK_VERSION}.jar,\
/opt/bitnami/spark/jars/kafka-clients-${KAFKA_CLIENT_VERSION}.jar,\
/opt/bitnami/spark/jars/commons-pool2-2.12.0.jar,\
/opt/bitnami/spark/jars/spark-token-provider-kafka-0-10_${SCALA_VERSION}-${SPARK_VERSION}.jar,\
/opt/bitnami/spark/jars/spark-streaming-kafka-0-10_${SCALA_VERSION}-${SPARK_VERSION}.jar\
/opt/bitnami/spark/jars/mariadb-java-client-2.7.4.jar"

CMD spark-submit --jars ${JARS_PATHS} /app/log_analyzer_spark.py
