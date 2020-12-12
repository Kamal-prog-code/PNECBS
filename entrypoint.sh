#!/bin/sh
set -e

if [ "x$DJANGO_MANAGE_COLLECTSTATIC" = 'xon' ]; then
  echo "Collecting static files"
  python manage.py collectstatic --noinput
  echo "Done: Collecting static files"
fi

if [ "x$DJANGO_MANAGE_MIGRATE" = 'xon' ]; then
  echo "Migrating database"
  python manage.py migrate --noinput
  echo "Done: Migrating database"
fi

exec "$@"
