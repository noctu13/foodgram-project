# FOODGRAM-PROJECT

Site for creating recipes. Implemented elements: filtering by tags, favorites list, subscription page, shopping page.
Example site: [noctu.ml](https://noctu.ml)

## Getting Started

Download [Docker Desktop](https://www.docker.com/products/docker-desktop) for Mac or Windows. [Docker Compose](https://docs.docker.com/compose) will be automatically installed. On Linux, make sure you have the latest version of [Compose](https://docs.docker.com/compose/install/).

## Enviroment settings

specify the following environment variables in /code/.env

    SECRET_KEY - set your own key

    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=postgres
    DB_HOST=db
    DB_PORT=5432

See details [Django settings: DATABASES](https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-DATABASES)

    POSTGRES_USER=postgres
    POSTGRES_PASSWORD - set your own password

See details [Postgres: Environment Variables](https://hub.docker.com/_/postgres)

    NGINX_PORT=80
    NGINX_IP=0.0.0.0
    NGINX_HOST=http://web:8000

Run in this directory:

    docker-compose up -d

Install migrations and preload data by executing the "startup.sh" script:

    docker-compose exec web startup.sh

The app will be running at [http://localhost:80](http://localhost:80)

## Other commands

Run other Django management commands, e.g.:

    docker-compose exec web ./manage.py createsuperuser

Or get a bash prompt within the web container:

    docker-compose exec web bash

Stop it all running:

    docker-compose down

If you change something in `docker-compose.yml` then you'll need to build
things again:

    docker-compose build

Or, just for the `web` container:

    docker-compose build web
