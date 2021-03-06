FROM python:3.6

ADD . /app/
WORKDIR /app

ENV DJANGO_SETTINGS_MODULE DebatesTournament.settings

RUN pip3 install --no-cache-dir -r /app/requirements.txt
RUN python manage.py collectstatic -c --noinput
