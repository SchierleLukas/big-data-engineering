CREATE DATABASE IF NOT EXISTS logs;
USE logs;

CREATE TABLE IF NOT EXISTS log_counts (
    start TIMESTAMP,
    end TIMESTAMP,
    count BIGINT,
    PRIMARY KEY (start, end)
);