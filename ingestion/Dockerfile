# Base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install necessary system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    librdkafka-dev

# Copy the requirements file and install Python packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script into the container
COPY logs_producer.py ./

# Define the command to run the Kafka Producer script
CMD ["python", "logs_producer.py"]