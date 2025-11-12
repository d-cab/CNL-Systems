# ===============================
# Base image
# ===============================
FROM python:3.11-slim

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# Install system dependencies (for things like Pillow, psycopg2, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency list first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Ensure instance directory exists for SQLite and uploads
RUN mkdir -p /app/instance && mkdir -p /app/cnl/static/uploads

# Set environment variables for Flask
ENV FLASK_APP=cnl:create_app
ENV FLASK_ENV=production
ENV FLASK_DEBUG=False

# Expose Flask/Gunicorn port
EXPOSE 8000

# Use entrypoint to run migrations + start Gunicorn
ENTRYPOINT ["./entrypoint.sh"]
