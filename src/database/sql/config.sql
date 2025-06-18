CREATE DATABASE IF NOT EXISTS VaultXSafe;

USE VaultXSafe;

CREATE TABLE IF NOT EXISTS user_id_password (
    id INT AUTO_INCREMENT PRIMARY KEY,
    field VARCHAR(100),
    user_id VARCHAR(255),
    user_password VARCHAR(255),
    created_time DATETIME,
    last_edited_time DATETIME
);
