-- init.sql
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mail VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);

INSERT INTO users (mail, password)
VALUES ('QuintenVdW@example.com', 'Admin123')
ON DUPLICATE KEY UPDATE mail='QuintenVdW@example.com';
