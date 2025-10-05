# Use official Python image
FROM python:3.11-slim

# Install dependencies and Chrome
RUN apt-get update && apt-get install -y wget gnupg unzip curl \
    && apt-get install -y chromium chromium-driver \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=True
ENV PORT=8080

# Copy files
WORKDIR /app
COPY . .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Start app
CMD exec gunicorn --bind :$PORT app:app
