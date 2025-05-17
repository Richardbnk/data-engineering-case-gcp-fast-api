FROM python:3.11-slim

WORKDIR /app

# Copy all project files into the container
COPY . /app

# Copy environment variables and service account credentials
COPY .env .env
COPY credentials/ credentials/

# Set the environment variable for GCP authentication
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/data-project.json

# Install all Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start the FastAPI application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
