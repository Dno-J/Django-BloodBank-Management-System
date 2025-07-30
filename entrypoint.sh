#!/bin/sh

echo "🔧 Running collectstatic..."
python bbms/manage.py collectstatic --noinput

echo "🔧 Running migrations..."
python bbms/manage.py migrate --noinput

echo "🚀 Starting Gunicorn..."
exec gunicorn bbms.wsgi:application --bind 0.0.0.0:8000
