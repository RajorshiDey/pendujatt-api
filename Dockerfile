# Use a lightweight Python image
FROM python:3.11-slim

# Install Chromium and dependencies
RUN apt-get update && apt-get install -y wget gnupg unzip curl chromium chromium-driver \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variables for Chrome
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Set workdir
WORKDIR /app

# Copy files
COPY . .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Render autodetection
EXPOSE 8080

# Start Flask with gunicorn (Render expects this format)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers=1", "app:app"]


