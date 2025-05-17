FROM python:3.11-slim

WORKDIR /app

# Copy all project files into the container
COPY . /app

# Set environment variables
ENV PYTHONPATH=/app
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/data-project.json

# Install system dependencies including curl
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make start script executable
RUN chmod +x /app/start.sh

# Run the start script to launch the API and upload CSVs
CMD ["/app/start.sh"]
