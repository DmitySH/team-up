#!/bin/sh
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py shell < test_fillers/generator.py

exec "$@"
