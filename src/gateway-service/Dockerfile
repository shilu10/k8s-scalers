FROM python:3.12-alpine

# Install Alpine build dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    mariadb-connector-c-dev \
    python3-dev

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Run app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main:app"]