/* This SQL script is executed at container start */
CREATE DATABASE IF NOT EXISTS logs;
USE logs;

/* WARNING: Remove this DROP statement in production!
   Only keep for development/testing environments */
DROP TABLE IF EXISTS log_data;

CREATE TABLE IF NOT EXISTS log_data (
    id BIGINT AUTO_INCREMENT,
    window_start TIMESTAMP,
    window_end TIMESTAMP,
    debug_count BIGINT DEFAULT 0,
    info_count BIGINT DEFAULT 0,
    warn_count BIGINT DEFAULT 0,
    error_count BIGINT DEFAULT 0,
    PRIMARY KEY (id),
    INDEX idx_window (window_start, window_end)
);