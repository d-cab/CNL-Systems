# Dockerfile
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Prevent Python from buffering logs
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn

# Copy app code
COPY . .

# Expose Gunicorn port
EXPOSE 8000

# Default command: Gunicorn
# Replace 'app:create_app()' with your actual app entry point if you use factory pattern
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
