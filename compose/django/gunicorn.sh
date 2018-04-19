#!/bin/sh
python manage.py migrate
python /app/manage.py collectstatic --noinput
/usr/local/bin/gunicorn config.wsgi --timeout 120 -w 10 -b 0.0.0.0:5000 --chdir=/app
