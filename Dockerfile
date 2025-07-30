# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . .

# Collect static files and run migrations
RUN python BBMS/manage.py collectstatic --noinput
RUN python BBMS/manage.py migrate --noinput

# Start the app with Gunicorn
CMD ["gunicorn", "BBMS.wsgi:application", "--bind", "0.0.0.0:8000"]
