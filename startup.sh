#!/bin/sh

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py preload 'ingredients.json'
python manage.py inittags

exec "$@"
