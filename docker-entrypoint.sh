#!/bin/bash

# Migrate the database first
echo "Migrating the database before starting the server"
export DJANGO_SETTINGS_MODULE="zaba.settings_docker"

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting server"
python manage.py runserver  0.0.0.0:8000