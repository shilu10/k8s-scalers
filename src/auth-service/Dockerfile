FROM python:3.12-alpine

# Install Alpine build dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    python3-dev \
    mariadb-connector-c-dev \
    stress-ng

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run the Flask app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8001", "main:app"]
