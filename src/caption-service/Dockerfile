FROM python:3.11-alpine

# Add system dependencies for building and networking
RUN apk add --no-cache gcc musl-dev libffi-dev libpq-dev \
    linux-headers libxml2-dev libxslt-dev \
    libjpeg-turbo-dev zlib-dev openblas-dev \
    build-base python3-dev libstdc++ \
    stress-ng

# Set working directory
WORKDIR /app

# Copy only requirements first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run the app using gunicorn with eventlet worker
CMD ["gunicorn", "-k", "eventlet", "-w", "1", "-b", "0.0.0.0:5000", "main:app"]
