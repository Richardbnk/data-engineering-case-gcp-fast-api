import pandas as pd
from fastapi import UploadFile
from app.bq import client, get_table_ref

schema_map = {
    "departments": ["id", "department"],
    "jobs": ["id", "job"],
    "hired_employees": ["id", "name", "datetime", "department_id", "job_id"],
}


def load_csv_to_bigquery(file: UploadFile, table_name: str):
    try:
        expected_columns = schema_map.get(table_name)
        if not expected_columns:
            return {"status": "failed", "error": f"Unknown table '{table_name}'"}

        df = pd.read_csv(file.file, names=expected_columns, header=None)

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
