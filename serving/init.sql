CREATE DATABASE IF NOT EXISTS logs;

USE logs;

CREATE TABLE IF NOT EXISTS anomalies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DOUBLE,
    level VARCHAR(10),
    message TEXT
);
