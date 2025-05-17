"""
Waits for the API to be ready

Automatically sends the necessary data (CSV files)

Prepares the environment so the system is ready to use without any manual step
"""

import time
import requests

files_to_upload = [
    ("departments", "data/departments.csv"),
    ("jobs", "data/jobs.csv"),
    ("hired_employees", "data/hired_employees.csv"),
]


def wait_for_api(url, timeout=30):
    for _ in range(timeout):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("API is up.")
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
    print("ERORR: API did not start in time.")
    return False


def upload_csv(table_name, filepath):
    with open(filepath, "rb") as f:
        files = {"file": (filepath, f)}
        res = requests.post(
            f"http://localhost:8080/upload_csv/?table_name={table_name}", files=files
        )
        print(f"Uploading {filepath} to {table_name} → {res.status_code} | {res.text}")


if __name__ == "__main__":
    if wait_for_api("http://localhost:8080/"):
        for table_name, filepath in files_to_upload:
            upload_csv(table_name, filepath)
