# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy all project files
COPY . .

# Collect static files and run migrations
RUN python BBMS/manage.py collectstatic --noinput
RUN python BBMS/manage.py migrate --noinput

# Expose port
EXPOSE 8000

# Start server
CMD ["gunicorn", "BBMS.wsgi:application", "--chdir", "BBMS", "--bind", "0.0.0.0:8000"]
