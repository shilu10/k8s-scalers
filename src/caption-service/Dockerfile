FROM python:3.11-alpine

# Optional: install dependencies for packages that require building
RUN apk add --no-cache gcc musl-dev libffi-dev

# Set working directory
WORKDIR /app

# Copy only requirements first
COPY requirements.txt .

# Install dependencies (cached if requirements.txt hasn't changed)
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the code
COPY . .

# Run the app
ENTRYPOINT ["python3", "main.py"]
