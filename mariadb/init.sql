CREATE DATABASE IF NOT EXISTS logs;
USE logs;

/* WARNING: Remove this DROP statement in production!
   Only keep for development/testing environments */
DROP TABLE IF EXISTS log_data;

CREATE TABLE IF NOT EXISTS log_data (
    id BIGINT AUTO_INCREMENT,
    window_start TIMESTAMP,
    window_end TIMESTAMP,
    count BIGINT,
    PRIMARY KEY (id),
    INDEX idx_window (window_start, window_end)
);