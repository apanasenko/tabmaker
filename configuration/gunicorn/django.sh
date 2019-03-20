#!/bin/bash

# Dockerized version of gunicorn starter script

NAME="tabmaker"                  # Name of the application
DJANGODIR=/app               # Django project directory
NUM_WORKERS=4           # how many worker processes should Gunicorn spawn
DJANGO_WSGI_MODULE=DebatesTournament.wsgi  # WSGI module name

# Activate the virtual environment
cd ${DJANGODIR}
export PYTHONPATH=${DJANGODIR}:${PYTHONPATH}

# Start your Django Gunicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
gunicorn ${DJANGO_WSGI_MODULE} \
  --pythonpath ${PYTHONPATH} \
  --name ${NAME} \
  --workers ${NUM_WORKERS} \
  --max-requests-jitter 3000 \
  --bind 0.0.0.0:8080 \
  --log-level info \
  --log-file -
