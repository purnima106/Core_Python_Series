# backend/upload.py
# Handles file uploads to AWS S3

from config import s3, BUCKET
import pandas as pd
import datetime

def upload_file(file_path):
    df = pd.read_csv(file_path)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")

    key = f"raw/year=2026/month=04/{timestamp}.csv"

    s3.upload_file(file_path, BUCKET, key)

    print(f"Uploaded to {key}")

if __name__ == "__main__":
    upload_file("../data/sample.csv")