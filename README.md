# 📊 Data Engineering Case - GCP (FastAPI)

This project is a full-stack data engineering solution that:
- Loads historical CSV data into Google BigQuery
- Recreates tables automatically to ensure clean initial loads
- Exposes a FastAPI service with endpoints to trigger and export analytical reports
- Containerized via Docker and designed for local and cloud environments

## 🚀 Features

- REST API built with **FastAPI**
- GCP integration with **BigQuery**
- Automatically loads tables to `raw` dataset:
  - `departments.csv`
  - `jobs.csv`
  - `hired_employees.csv`
- Generates refined reporting tables in `refined` dataset
- Containerized with Docker for easy execution
- Includes bootstrap logic that auto-loads data when the container runs

## 🧾 Requirements

- Docker Desktop running
- GCP Project with BigQuery enabled
- Service Account JSON key file (credentials/data-project_template.json)
- CSV files:
  - `data/departments.csv`
  - `data/jobs.csv`
  - `data/hired_employees.csv`

## Evidences of the execution of the project

You can find evidence of the project execution, such as screenshots and result outputs, in the [evidences folder](https://github.com/Richardbnk/data-engineering-case-gcp-fast-api/tree/main/evidences).

## 🐳 Running the project

### 1. Clone the repository

```bash
git clone https://github.com/Richardbnk/data-engineering-case-gcp-fast_api.git
cd data-engineering-case-gcp-fast_api
```

### 2. Add credentials and .~~env~~

- Place your GCP service account key in:  
  `credentials/data-project.json`

```
GCP_PROJECT_ID = data-project-452300
BQ_DATASET = raw
```

### 3. Build and run the Docker container

```bash
docker build -t gcp-data-api .
docker run -p 8000:8080 --env-file .env gcp-data-api
```

Once started, the API will load the CSVs automatically and be available at:  
`http://localhost:8000/docs`

## 📈 Reports – How to run

Two analytical endpoints are available to **generate and export reports** into BigQuery (`refined` dataset). These reports are written as new tables using SQL logic everytime the link is opened.

### 🔹 1. Hires Per Quarter

Generates a table showing the number of hires per department and job in **2021**, broken down by quarter.

**Endpoint:**

```http
GET http://localhost:8000/export/hires_by_quarter
```

**Creates Table:**

```text
refined.hires_per_quarter
```

**Example Output:**

| department     | job        | Q1 | Q2 | Q3 | Q4 |
|----------------|------------|----|----|----|----|
| Staff          | Recruiter  | 3  | 0  | 7  | 11 |
| Staff          | Manager    | 2  | 1  | 0  | 2  |
| Supply Chain   | Manager    | 0  | 1  | 3  | 0  |

### 🔹 2. Departments Above Average

Generates a list of departments that hired **more employees than the average** number of hires across all departments in 2021.

**Endpoint:**

```http
GET http://localhost:8000/export/departments_above_avg
```

**Creates Table:**

```text
refined.departments_above_avg
```

**Example Output:**

| id | department     | hired |
|----|----------------|--------|
| 7  | Staff          | 45     |
| 9  | Supply Chain   | 12     |

## 🧪 Testing the API

You can access Swagger UI for testing:

`http://localhost:8000/docs`

You can also test with `curl`:

```bash
curl http://localhost:8000/export/hires_by_quarter
curl http://localhost:8000/export/departments_above_avg
```

## ✨ Bonus: Cloud Ready

This project is ready to run with GCP products like:
- **Cloud Run**
- **Cloud Composer (for DAG scheduling)**
- **Vertex AI Workbench** (if desired for orchestrating models)