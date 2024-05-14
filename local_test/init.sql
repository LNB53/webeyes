-- init.sql
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);

INSERT INTO users (username, password)
VALUES ('QuintenVdW', 'Admin123')
ON DUPLICATE KEY UPDATE username='QuintenVdW';
