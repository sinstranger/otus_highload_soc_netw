#!/usr/bin/env bash

python src/manage.py create_tables
#uwsgi \
#  --chdir=/app \
#  --module=qblog.wsgi:application \
#  --env DJANGO_SETTINGS_MODULE=qblog.settings.server_dev \
#  --master --pidfile=/tmp/project-master.pid \
#  --http=0.0.0.0:8000 --processes=5 --uid=1000 --gid=1000 --harakiri=20 --max-requests=5000 --vacuum

uwsgi \
  --chdir=./src \
  --module=social.wsgi:application \
  --master --pidfile=/tmp/project-master.pid \
  --http=0.0.0.0:8000 --processes=5 --uid=1000 --gid=1000 --harakiri=20 --max-requests=5000 --vacuum
