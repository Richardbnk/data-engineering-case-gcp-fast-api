from fastapi import FastAPI, UploadFile, File
from app.load import load_csv_to_bigquery

app = FastAPI()


@app.get("/")
def root():
    return {"message": "API is up"}


@app.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...), table_name: str = "hired_employees"):
    return load_csv_to_bigquery(file, table_name)
