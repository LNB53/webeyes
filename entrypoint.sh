#!/bin/sh

wait_for_mysql() {
  local host="$1"
  local port="$2"
  local max_retries=60
  local wait_seconds=1
  local attempt=1

  echo "Waiting for MySQL to be available at $host:$port..."
  until nc -z "$host" "$port"; do
    if [ "$attempt" -ge "$max_retries" ]; then
      echo "Error: Unable to connect to MySQL at $host:$port after $max_retries attempts"
      exit 1
    fi
    echo "Attempt $attempt/$max_retries: MySQL not yet available, waiting $wait_seconds second(s)..."
    sleep "$wait_seconds"
    attempt=$((attempt + 1))
  done
  echo "MySQL is available at $host:$port"
}

# Wait for the database to be ready
echo "Waiting on database..."
wait_for_mysql "$DB_HOST" "$DB_PORT"

# Generate application key
echo "Generating key..."
php artisan key:generate

# Clear cache, routes, config, and views
echo "Clearing application cache..."
php artisan cache:clear
echo "Clearing routing cache..."
php artisan route:clear
echo "Clearing configuration cache..."
php artisan config:clear
echo "Clearing views cache..."
php artisan view:clear

# Optimize application
echo "Optimizing..."
php artisan optimize

# Run migrations and seed
echo "Migrating"
php artisan migrate --seed

# Start the Vite production build
echo "Building assets with Vite"
npm run build

# Start PHP-FPM
echo "Starting FastCGI Process Manager"
exec php-fpm

echo "Done!"
