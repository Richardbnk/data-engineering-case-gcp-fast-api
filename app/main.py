from fastapi import FastAPI, UploadFile, File
from app.load import load_csv_to_bigquery
from app.queries import get_hires_per_quarter, get_departments_above_avg

app = FastAPI()


@app.get("/")
def root():
    return {"message": "API is up"}


# Load
@app.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...), table_name: str = "hired_employees"):
    return load_csv_to_bigquery(file, table_name)


# Queries
@app.get("/export/hires_by_quarter")
def export_hires_by_quarter():
    return get_hires_per_quarter()


@app.get("/export/departments_above_avg")
def export_departments_above_avg():
    return get_departments_above_avg()
