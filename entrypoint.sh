#!/bin/bash
set -e

# Navigate to where manage.py is
cd /app/BBMS

echo "⚙️ Running database migrations..."
python manage.py migrate --noinput

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "🚀 Starting Gunicorn server..."
exec gunicorn BBMS.wsgi:application --bind 0.0.0.0:8000