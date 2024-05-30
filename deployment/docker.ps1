docker-compose down -v

docker-compose up -d --build

Start-Sleep -Seconds 5

echo 'Clearing configuration cache...'
docker-compose exec app php artisan config:clear

echo 'Clearing application cache...'
docker-compose exec app php artisan cache:clear

echo 'Generating key...'
docker-compose exec app php artisan key:generate --verbose

echo 'Optimizing...'
docker-compose exec app php artisan optimize

echo 'App environment variables:'
docker-compose exec app env | Select-String "^DB_" | sort

echo 'Database environment variables:'
docker-compose exec database env | Select-String "^DB_" | sort

echo 'Migrating database...'
docker-compose exec app php artisan migrate --seed
