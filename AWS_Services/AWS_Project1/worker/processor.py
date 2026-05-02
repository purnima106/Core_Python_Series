# worker/processor.py

import os
import boto3
import pandas as pd
import io
import urllib.parse
import json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

s3_client = boto3.client("s3", region_name="ap-south-1")
sqs = boto3.client("sqs", region_name="ap-south-1")

QUEUE_URL = os.environ.get("SQS_QUEUE_URL")
BUCKET = os.environ.get("S3_BUCKET_NAME")

EXPECTED_DTYPES = {
    "order_id": "string",
    "order_item_id": "int64",
    "product_id": "string",
    "seller_id": "string",
    "price": "float64",
    "freight_value": "float64",
}

def enforce_schema(df):
    df = df[[
        "order_id",
        "order_item_id",
        "product_id",
        "seller_id",
        "price",
        "freight_value"
    ]]

    for col, dtype in EXPECTED_DTYPES.items():
        df[col] = df[col].astype(dtype)

    return df


def process_message(message):
    bucket = message["bucket"]
    key = urllib.parse.unquote_plus(message["key"])

    print(f"Processing: s3://{bucket}/{key}")

    obj = s3_client.get_object(Bucket=bucket, Key=key)
    df = pd.read_csv(io.BytesIO(obj["Body"].read()))

    df = enforce_schema(df)

    now = datetime.utcnow()

    folder_key = (
        f"curated/orders/"
        f"year={now.year}/"
        f"month={now.month:02d}/"
        f"day={now.day:02d}/"
    )

    output_path = f"s3://{bucket}/{folder_key}"

    print(f"Writing to {output_path}")

    df.to_parquet(
        output_path,
        engine="pyarrow",
        compression="snappy",
        index=False
    )

    print("Parquet written successfully.")


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

            try:
                process_message(body)
            except Exception as e:
                print(f"ERROR: {e}")
                continue

            sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=msg["ReceiptHandle"],
            )

            print("Message processed and deleted.")


if __name__ == "__main__":
    poll_sqs()