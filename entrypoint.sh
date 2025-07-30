#!/bin/sh

echo "🔧 Running collectstatic..."
python bbms/manage.py collectstatic --noinput

echo "🔧 Running migrations..."
python bbms/manage.py migrate --noinput

echo "🚀 Starting Gunicorn..."
# --chdir bbms sets working dir to /app/bbms so BBMS.wsgi can be found
exec gunicorn BBMS.wsgi:application --chdir bbms --bind 0.0.0.0:8000
