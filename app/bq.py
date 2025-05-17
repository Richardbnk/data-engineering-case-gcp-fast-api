from google.cloud import bigquery
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis do .env

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET = os.getenv("BQ_DATASET")

client = bigquery.Client()
