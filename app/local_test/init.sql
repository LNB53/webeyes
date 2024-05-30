-- init.sql
drop schema if exists login_database;
create schema login_database;
create table login_database.users
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    mail VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL
);
