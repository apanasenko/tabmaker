#!/usr/bin/env bash
set -e

composeprod() {
    docker-compose -f ${PWD}/docker-compose.prod.yml $@;
}

composeprod pull
composeprod run --rm backend python manage.py migrate --noinput
composeprod run --rm backend python manage.py collectstatic --noinput
composeprod up -d
