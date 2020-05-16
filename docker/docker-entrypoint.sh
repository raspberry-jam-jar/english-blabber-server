#!/bin/bash

set -x

PORT=${PORT:=8000}

POSTGRES_HOST=${POSTGRES_HOST:="127.0.0.1"}

POSTGRES_PASSWORD=${POSTGRES_PASSWORD:=""}

POSTGRES_PORT=${POSTGRES_PORT:="5432"}

POSTGRES_USER=${POSTGRES_USER:="postgres"}

POSTGRES_DB=${POSTGRES_DB:="blabber"}

SECRET_KEY=${SECRET_KEY:="secret"}

EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD:=""}

EMAIL_HOST_USER=${EMAIL_HOST_USER:=""}

SUPERUSER_NAME=${SUPERUSER_NAME:="admin"}

SUPERUSER_EMAIL=${SUPERUSER_EMAIL:="admin@mail.ru"}

SUPERUSER_PASSWORD=${SUPERUSER_PASSWORD:=""}

set +x

if [ -z "${POSTGRES_PASSWORD}" ]; then
    >&2 echo "Postgres password is not specified"
    exit 1
fi

if [ -z "${SUPERUSER_PASSWORD}" ]; then
    >&2 echo "Superuser password is not specified"
    exit 1
fi

>&2 echo "Pull project"
git pull

export DATABASE_URL="psql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
export PYTHONPATH="$PYTHONPATH:$(pwd)/modules:$(pwd)/conf"
cp conf/.env.template conf/.env

>&2 echo "Waiting for Postgres"

./wait-for-it.sh  -h "${POSTGRES_HOST}" -p "${POSTGRES_PORT}" -t 90 -- >&2 echo "Postgres is ready"

output="$(PGPASSWORD="${POSTGRES_PASSWORD}" psql -h "${POSTGRES_HOST}" -p "${POSTGRES_PORT}" -U "${POSTGRES_USER}" -lqt| cut -d \| -f 1 | grep "${POSTGRES_DB}")"

>&2 echo "Apply migrations"
python manage.py migrate

>&2 echo "Create superuser if do not exist"
django_create_superuser.py

>&2 echo "Collect static files"
python manage.py collectstatic --noinput

sudo mkdir -p /etc/ssl/blabber
if [ -z "$(ls -A /etc/ssl/blabber)" ]; then
    >&2 echo "Generate SSL certificates"
    sudo openssl req -x509 -newkey rsa:2048 -keyout /etc/ssl/blabber/blabber.key -out /etc/ssl/blabber/blabber.crt \
    -days 30 -nodes -subj "/C=US/ST=California/L=Palo Alto/O=StackStorm/OU=Information Technology/CN=$(hostname)"
else
   >&2 echo "Use existed certificates"
fi

>&2 echo "Start server"
gunicorn -b 0.0.0.0:"$PORT" --keyfile /etc/ssl/blabber/blabber.key --certfile /etc/ssl/blabber/blabber.crt wsgi:application
