#Stage 1: Build environment
FROM python:3.10-slim as builder
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Optional: If you need mysqlclient installed separately for some reason:
# RUN pip install --no-cache-dir mysqlclient

# Copy app files
COPY . .
RUN touch .env

# Stage: main
FROM builder AS main
RUN python manage.py collectstatic --noinput
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
