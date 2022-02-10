#!/bin/sh

set -e

echo "Waiting for PostgreSQL..."

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$DB_HOST" -U "$POSTGRES_USER" -c '\q'; do
  >&2 echo "PostgresSQL is unavailable - sleeping"
  sleep 1
done

echo "PostgreSQL started"

#python manage.py flush --no-input
echo "Run python migrate"
python manage.py migrate

echo "Run python createsuperuser"
python manage.py createsuperuser --username=admin --email=admin@admin.com --noinput

echo "Run python runserver"
python manage.py runserver 0.0.0.0:8000

