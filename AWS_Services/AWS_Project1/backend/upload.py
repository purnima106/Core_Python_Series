# backend/upload.py
# Handles file uploads to AWS S3

from config import S3_CLIENT, S3_BUCKET_NAME
import pandas as pd
import datetime
import os

def upload_file(file_path):
    df = pd.read_csv(file_path)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")

    key = f"raw/year=2026/month=04/{timestamp}.csv"

    S3_CLIENT.upload_file(file_path, S3_BUCKET_NAME, key)

    print(f"Uploaded to {key}")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "sample.csv")
    upload_file(file_path)