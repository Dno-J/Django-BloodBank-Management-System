# 🐍 Use official slim Python image
FROM python:3.11-slim

# 🔧 Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 📁 Set working directory
WORKDIR /app

# 🧱 Install system dependencies for WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libgobject-2.0-0 \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 📦 Install Python dependencies
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 📁 Copy project files
COPY . .

# 🔐 Make entrypoint executable
RUN chmod +x entrypoint.sh

# 🚀 Run entrypoint
ENTRYPOINT ["./entrypoint.sh"]
