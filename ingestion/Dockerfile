# Dockerfile to package the Kafka Producer script

# Base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install necessary system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    librdkafka-dev

# Copy the requirements file and the script into the container
COPY requirements.txt ./
COPY logs_producer.py ./

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Define the command to run the Kafka Producer script
CMD ["python", "logs_producer.py"]