FROM bitnami/spark:3.5.3

ENV SPARK_VERSION=3.5.3

# Install Python, pip, and wget
USER root
RUN apt-get update && apt-get install -y python3 python3-pip wget

# Set environment variables for Scala
ENV SCALA_VERSION=2.12
ENV SCALA_VERSION_MINOR=.15

# Download necessary JARs
RUN wget https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_${SCALA_VERSION}/${SPARK_VERSION}/spark-sql-kafka-0-10_${SCALA_VERSION}-${SPARK_VERSION}.jar -P /opt/bitnami/spark/jars/ && \
    wget https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/2.8.1/kafka-clients-2.8.1.jar -P /opt/bitnami/spark/jars/ && \
    wget https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.12.0/commons-pool2-2.12.0.jar -P /opt/bitnami/spark/jars/ && \
    wget https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_${SCALA_VERSION}/${SPARK_VERSION}/spark-token-provider-kafka-0-10_${SCALA_VERSION}-${SPARK_VERSION}.jar -P /opt/bitnami/spark/jars/ && \
    wget https://repo1.maven.org/maven2/org/apache/spark/spark-streaming-kafka-0-10_${SCALA_VERSION}/${SPARK_VERSION}/spark-streaming-kafka-0-10_${SCALA_VERSION}-${SPARK_VERSION}.jar -P /opt/bitnami/spark/jars/

# Copy Python dependencies and install them
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Copy the Spark application
COPY read_kafka_stream.py /app/read_kafka_stream.py

# Default command: List files and then run spark-submit
CMD spark-submit --jars /opt/bitnami/spark/jars/spark-sql-kafka-0-10_${SCALA_VERSION}-${SPARK_VERSION}.jar,/opt/bitnami/spark/jars/kafka-clients-2.8.1.jar,/opt/bitnami/spark/jars/commons-pool2-2.12.0.jar,/opt/bitnami/spark/jars/spark-token-provider-kafka-0-10_${SCALA_VERSION}-${SPARK_VERSION}.jar,/opt/bitnami/spark/jars/spark-streaming-kafka-0-10_${SCALA_VERSION}-${SPARK_VERSION}.jar /app/read_kafka_stream.py