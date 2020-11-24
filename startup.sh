#!/bin/sh

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py shell < preload.py

exec "$@"
