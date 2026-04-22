import os
import boto3
import pandas as pd
import io
import urllib.parse
import json
import s3fs
from dotenv import load_dotenv

# Load .env from project root (two levels up from worker/)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

# AWS clients
s3_client = boto3.client("s3", region_name="ap-south-1")
sqs = boto3.client("sqs", region_name="ap-south-1")

QUEUE_URL = os.environ.get("SQS_QUEUE_URL", "")
BUCKET    = os.environ.get("S3_BUCKET_NAME", "rag-ml-pipeline-bucket-purnima")

# Expected schema for Glue/Athena compatibility
EXPECTED_DTYPES = {
    "order_id": "string",
    "order_item_id": "int64",
    "product_id": "string",
    "seller_id": "string",
    "shipping_limit_date": "string",
    "price": "float64",
    "freight_value": "float64",
}


def enforce_schema(df: pd.DataFrame) -> pd.DataFrame:
    """Cast columns to expected dtypes and add 'processed' flag."""
    for col, dtype in EXPECTED_DTYPES.items():
        if col in df.columns:
            try:
                df[col] = df[col].astype(dtype)
            except Exception as e:
                print(f"  [WARN] Could not cast column '{col}' to {dtype}: {e}")
    df["processed"] = True
    return df


def process_message(message):
    bucket = message["bucket"]
    key = urllib.parse.unquote_plus(message["key"])

    print(f"Processing: s3://{bucket}/{key}")

    # --- Read CSV from S3 ---
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    df = pd.read_csv(io.BytesIO(obj["Body"].read()))
    print(f"  Rows: {len(df)}, Columns: {list(df.columns)}")

    # --- Schema enforcement ---
    df = enforce_schema(df)

    # --- Derive dataset folder path (folder-based, NOT a single file) ---
    # e.g. raw/sample.csv  →  curated/sample_dataset/
    filename = key.split("/")[-1]                          # sample.csv
    dataset_name = filename.replace(".csv", "_dataset")   # sample_dataset
    prefix = key.replace("raw/", "curated/")              # curated/.../sample.csv
    folder_key = "/".join(prefix.split("/")[:-1]) + f"/{dataset_name}/"
    output_path = f"s3://{bucket}/{folder_key}"

    print(f"  Writing dataset → {output_path}")

    # --- Write as folder-based Parquet dataset via s3fs ---
    fs = s3fs.S3FileSystem(anon=False)
    df.to_parquet(
        output_path,
        engine="pyarrow",
        index=False,
        compression="snappy",
        storage_options={"client_kwargs": {"region_name": "ap-south-1"}},
    )

    print(f"  ✅ Dataset saved: {output_path}")


def poll_sqs():
    print("Waiting for messages...")

    while True:
        response = sqs.receive_message(
            QueueUrl=QUEUE_URL,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10,
            VisibilityTimeout=30,
        )

        messages = response.get("Messages", [])

        if not messages:
            print("No messages yet...")
            continue

        for msg in messages:
            body = json.loads(msg["Body"])
            print("Message received:", body)

            try:
                process_message(body)
            except Exception as e:
                print(f"  [ERROR] Failed to process message: {e}")
                # Do NOT delete — let it retry or go to DLQ
                continue

            sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=msg["ReceiptHandle"],
            )
            print("  Message deleted from queue.")


if __name__ == "__main__":
    poll_sqs()