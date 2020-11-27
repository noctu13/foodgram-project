# FOODGRAM-PROJECT

Site for creating recipes. Implemented elements: filtering by tags, favorites list, subscription page, shopping page.
Example site: [noctu.ml](https://noctu.ml)

## Getting Started

Download [Docker Desktop](https://www.docker.com/products/docker-desktop) for Mac or Windows. [Docker Compose](https://docs.docker.com/compose) will be automatically installed. On Linux, make sure you have the latest version of [Compose](https://docs.docker.com/compose/install/).

## Enviroment settings

specify the following environment variables in /code/.env

    SECRET_KEY - set your own key
    POSTGRES_PASSWORD - set your own password

See details [Postgres: Environment Variables](https://hub.docker.com/_/postgres)

    DATABASE_URL=psql://postgres:POSTGRES_PASSWORD@db:5432/postgres

See details [Django-environ](https://django-environ.readthedocs.io/en/latest/#installation)

    NGINX_DOMAIN - input your domain

Modify init-letsencrypt.sh file, insert your email and domain.

Run in this directory to install Let’s Encrypt certificates:

    sudo init-letsencrypt.sh

Start your services:

    docker-compose up -d

Install migrations and preload data by executing the "startup.sh" script:

    docker-compose exec web startup.sh

The app will be running at [http://localhost:80](http://localhost:80)

Update nginx config every 34 hours to update ssl certificate:

    docker-compose exec nginx nginx -s reload

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
