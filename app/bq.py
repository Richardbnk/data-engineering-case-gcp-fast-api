from google.cloud import bigquery
import os

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET = os.getenv("BQ_DATASET")

client = bigquery.Client()


def get_table_ref(table_name: str):
    return f"{PROJECT_ID}.{DATASET}.{table_name}"
