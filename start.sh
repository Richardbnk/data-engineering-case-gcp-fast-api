#!/bin/bash

# Start the FastAPI API in the background
uvicorn app.main:app --host 0.0.0.0 --port 8080 &

# Wait for the API to be up
echo "[BOOTSTRAP] Waiting for API to be ready..."
until curl -s http://localhost:8080/ > /dev/null; do
  sleep 1
done
echo "[BOOTSTRAP] API is up. Sending CSVs..."

# Upload CSVs via API (one-time load)
curl -X POST "http://localhost:8080/upload_csv/?table_name=departments" -F "file=@data/departments.csv"
curl -X POST "http://localhost:8080/upload_csv/?table_name=jobs" -F "file=@data/jobs.csv"
curl -X POST "http://localhost:8080/upload_csv/?table_name=hired_employees" -F "file=@data/hired_employees.csv"

# Keep the container alive
wait
