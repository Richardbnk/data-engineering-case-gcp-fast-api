import pandas as pd
from app.bq import client, get_table_ref
from fastapi import UploadFile
from google.cloud import bigquery

schema_map = {
    "departments": [
        bigquery.SchemaField("id", "INTEGER"),
        bigquery.SchemaField("department", "STRING"),
    ],
    "jobs": [
        bigquery.SchemaField("id", "INTEGER"),
        bigquery.SchemaField("job", "STRING"),
    ],
    "hired_employees": [
        bigquery.SchemaField("id", "INTEGER"),
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("datetime", "TIMESTAMP"),
        bigquery.SchemaField("department_id", "INTEGER"),
        bigquery.SchemaField("job_id", "INTEGER"),
    ],
}


def recreate_table(table_name: str):
    table_id = get_table_ref(table_name)
    try:
        client.delete_table(table_id, not_found_ok=True)
        print(f"[INFO] Deleted existing table: {table_id}")
    except Exception as e:
        print(f"[WARN] Could not delete table {table_id}: {e}")
    table = bigquery.Table(table_id, schema=schema_map[table_name])
    client.create_table(table)
    print(f"[INFO] Recreated table: {table_id}")


def load_csv_to_bigquery(file: UploadFile, table_name: str):
    try:
        # Recreate the destination table
        recreate_table(table_name)

        # Read and format the CSV

        df = pd.read_csv(file.file, header=None)
        df.columns = [field.name for field in schema_map[table_name]]

        # Force correct column types
        if table_name == "hired_employees":
            df.columns = ["id", "name", "datetime", "department_id", "job_id"]

            # Remove lines with missing key columns
            df.dropna(
                subset=["id", "department_id", "job_id", "datetime"], inplace=True
            )

            df["id"] = df["id"].astype(int)
            df["department_id"] = df["department_id"].astype(int)
            df["job_id"] = df["job_id"].astype(int)
            df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

        if table_name == "departments":
            df["id"] = df["id"].astype(int)

        if table_name == "jobs":
            df["id"] = df["id"].astype(int)

        # Upload to BigQuery
        table_id = get_table_ref(table_name)
        job = client.load_table_from_dataframe(df, table_id)
        job.result()

        return {"status": "success", "rows": len(df)}

    except Exception as e:
        return {"status": "failed", "error": str(e)}


def insert_batch_rows(rows: list[dict], table_name: str):
    if not rows:
        return {"status": "failed", "reason": "No rows provided."}
    if len(rows) > 1000:
        return {"status": "failed", "reason": "Batch limit exceeded (max 1000)."}

    table_id = get_table_ref(table_name)
    errors = client.insert_rows_json(table_id, rows)
    if errors:
        return {"status": "failed", "errors": errors}
    return {"status": "success", "rows_inserted": len(rows)}
