# dockerfile.sql
FROM mysql:latest

# Set MySQL root password environment variable
ENV MYSQL_ROOT_PASSWORD='administrator'

# Optionally set MySQL database and user if needed
ENV MYSQL_DATABASE=login_database
ENV MYSQL_USER=administator
ENV MYSQL_PASSWORD=administator

# Copy the custom MySQL configuration file into the container
COPY ./my.cnf /etc/mysql/my.cnf

# Copy the initialization SQL script into the container
COPY ./init.sql /docker-entrypoint-initdb.d/

# Expose ports
EXPOSE 3306
