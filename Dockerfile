# 🐍 Use official slim Python image
FROM python:3.11-slim

# 🔧 Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 📁 Set working directory to project root
WORKDIR /app

# 📦 Install dependencies
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 📁 Copy entire project
COPY . .

# 🔐 Make entrypoint executable
RUN chmod +x entrypoint.sh

# 🚀 Run entrypoint script
ENTRYPOINT ["./entrypoint.sh"]
