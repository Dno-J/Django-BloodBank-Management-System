#!/bin/sh

echo "🔧 Running collectstatic..."
python manage.py collectstatic --noinput || exit 1

echo "🔧 Running migrations..."
python manage.py migrate --noinput || exit 1

echo "🚀 Starting Gunicorn..."
exec gunicorn BBMS.wsgi:application --bind 0.0.0.0:8000
