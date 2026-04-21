# worker/processor.py
# Background worker for processing tasks

import boto3
import pandas as pd
import io

BUCKET = "rag-ml-pipeline-bucket"

s3 = boto3.client("s3")

def process_latest_file():
    # list files in raw/
    response = s3.list_objects_v2(Bucket=BUCKET, Prefix="raw/")
    
    files = response.get("Contents", [])
    
    if not files:
        print("No files found")
        return
    
    latest = files[-1]["Key"]
    print("Processing:", latest)

    obj = s3.get_object(Bucket=BUCKET, Key=latest)
    df = pd.read_csv(io.BytesIO(obj["Body"].read()))

    # simple transform
    df["processed"] = True

    buffer = io.BytesIO()
    df.to_parquet(buffer, index=False)

    new_key = latest.replace("raw/", "curated/").replace(".csv", ".parquet")

    s3.put_object(Bucket=BUCKET, Key=new_key, Body=buffer.getvalue())

    print("Saved to:", new_key)

if __name__ == "__main__":
    process_latest_file()