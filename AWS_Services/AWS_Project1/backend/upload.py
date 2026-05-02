# backend/upload.py

from config import S3_CLIENT, S3_BUCKET_NAME, SQS_CLIENT, SQS_QUEUE_URL
import pandas as pd
import datetime
import os
import json

def upload_file(file_path):
    df = pd.read_csv(file_path)

    # Keep only required columns
    df = df[[
        "order_id",
        "order_item_id",
        "product_id",
        "seller_id",
        "price",
        "freight_value"
    ]]

    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M")

    key = f"raw/year={datetime.datetime.utcnow().year}/month={datetime.datetime.utcnow().month:02d}/{timestamp}.csv"

    # Save cleaned CSV temporarily
    temp_path = "temp.csv"
    df.to_csv(temp_path, index=False)

    # Upload to S3
    S3_CLIENT.upload_file(temp_path, S3_BUCKET_NAME, key)

    print(f"Uploaded to s3://{S3_BUCKET_NAME}/{key}")

    # Send SQS message
    message = {
        "bucket": S3_BUCKET_NAME,
        "key": key
    }

    SQS_CLIENT.send_message(
        QueueUrl=SQS_QUEUE_URL,
        MessageBody=json.dumps(message)
    )

    print("Message sent to SQS")

    os.remove(temp_path)


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "sample.csv")
    upload_file(file_path)