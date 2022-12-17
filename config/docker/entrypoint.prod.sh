#!/bin/sh

cd finble

python manage.py collectstatic --no-input
python manage.py makemigrations vote
python manage.py migrate

exec "$@"