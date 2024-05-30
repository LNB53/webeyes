# Base image
FROM php:8.1-fpm-alpine AS base

# Install necessary packages and PHP extensions
RUN apk add --no-cache zlib-dev libpng-dev libzip-dev $PHPIZE_DEPS \
    && docker-php-ext-install exif gd zip pdo_mysql

# Set working directory for the base image
WORKDIR /var/www

# Development stage
FROM base AS dev

# Install Composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/bin --filename=composer

# Copy Composer files
COPY --chown=www-data:www-data composer.json composer.lock ./

# Install Composer dependencies
RUN composer install --prefer-dist --no-ansi --no-dev --no-scripts --no-autoloader

# Copy application source code
COPY --chown=www-data:www-data . .

# Generate optimized autoload files
RUN composer dump-autoload -o

# Build stage
FROM base AS build-fpm

# Install Composer
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

# Copy Composer files
COPY --chown=www-data:www-data composer.json composer.lock ./

# Install Composer dependencies
RUN composer install --prefer-dist --no-ansi --no-dev --no-scripts --no-autoloader

# Copy application source code
COPY --chown=www-data:www-data . .

# Generate optimized autoload files
RUN composer dump-autoload -o

# Run Laravel optimization commands
RUN php artisan optimize

# Final stage
FROM base AS fpm

# Switch to www-data user
USER www-data

# Copy the application code from the build stage
COPY --from=build-fpm /var/www /var/www

# Switch back to root to set permissions
USER root

# Ensure correct permissions
RUN chmod -R 755 /var/www/storage \
    && chmod -R 755 /var/www/bootstrap/cache

# Set entrypoint
ENTRYPOINT ["./entrypoint.sh"]
