# Use Python 3.9 slim as the base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    wget \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
# Copy the startup script from the docker/app directory
COPY docker/app/startup.sh /app/startup.sh
RUN chmod +x /app/startup.sh
# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Copy the startup script
COPY startup.sh /app/startup.sh
RUN chmod +x /app/startup.sh

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["/app/startup.sh"]
