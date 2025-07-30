#!/bin/sh

echo "Current directory: $(pwd)"
echo "List files:"
ls -la

echo "List BBMS directory:"
ls -la BBMS

echo "🔧 Running collectstatic..."
python manage.py collectstatic --noinput

echo "🔧 Running migrations..."
python manage.py migrate --noinput

echo "🚀 Starting Gunicorn..."
exec gunicorn BBMS.wsgi:application --bind 0.0.0.0:8000
