#!/bin/bash

DJANGODIR=/app
cd ${DJANGODIR}
export PYTHONPATH=${DJANGODIR}:${PYTHONPATH}

python manage.py runserver 0.0.0.0:8080
