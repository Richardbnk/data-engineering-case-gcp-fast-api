from app.bq import client
import os

PROJECT = client.project
RAW_DATASET = os.getenv("BQ_DATASET")
REFINED_DATASET = "refined"


def get_hires_per_quarter():
    query = f"""
    CREATE OR REPLACE TABLE `{PROJECT}.{REFINED_DATASET}.hires_per_quarter` AS
    SELECT 
        d.department, 
        j.job,
        COUNTIF(EXTRACT(QUARTER FROM h.datetime) = 1) AS Q1,
        COUNTIF(EXTRACT(QUARTER FROM h.datetime) = 2) AS Q2,
        COUNTIF(EXTRACT(QUARTER FROM h.datetime) = 3) AS Q3,
        COUNTIF(EXTRACT(QUARTER FROM h.datetime) = 4) AS Q4
    FROM `{PROJECT}.{RAW_DATASET}.hired_employees` h
    JOIN `{PROJECT}.{RAW_DATASET}.departments` d ON h.department_id = d.id
    JOIN `{PROJECT}.{RAW_DATASET}.jobs` j ON h.job_id = j.id
    WHERE EXTRACT(YEAR FROM h.datetime) = 2021
    GROUP BY d.department, j.job
    ORDER BY d.department, j.job
    """
    client.query(query).result()
    return {
        "status": "success",
        "table": f"{PROJECT}.{REFINED_DATASET}.hires_per_quarter",
    }


def get_departments_above_avg():
    query = f"""
    CREATE OR REPLACE TABLE `{PROJECT}.{REFINED_DATASET}.departments_above_avg` AS
    WITH hires AS (
        SELECT department_id, COUNT(*) AS hired
        FROM `{PROJECT}.{RAW_DATASET}.hired_employees`
        WHERE EXTRACT(YEAR FROM datetime) = 2021
        GROUP BY department_id
    ),
    avg_hires AS (
        SELECT AVG(hired) AS mean FROM hires
    )
    SELECT d.id, d.department, h.hired
    FROM hires h
    JOIN `{PROJECT}.{RAW_DATASET}.departments` d ON h.department_id = d.id,
         avg_hires
    WHERE h.hired > avg_hires.mean
    ORDER BY h.hired DESC
    """
    client.query(query).result()
    return {
        "status": "success",
        "table": f"{PROJECT}.{REFINED_DATASET}.departments_above_avg",
    }
