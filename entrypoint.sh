#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi


echo "before pythoncreate"

python manage.py flush --no-input
python manage.py createsuperuser --username=admin --email=admin@admin.com --noinput
python manage.py migrate

echo "after pythoncreate"
exec "$@"