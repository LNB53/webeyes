# dockerfile.sql
FROM mysql:latest
COPY ./my.cnf /etc/mysql/my.cnf
COPY ./init.sql /docker-entrypoint-initdb.d/
