# lambda/handler.py
# AWS Lambda function handler

import json
import boto3

sqs = boto3.client("sqs")

QUEUE_URL = "YOUR_SQS_URL"

def lambda_handler(event, context):
    for record in event["Records"]:
        key = record["s3"]["object"]["key"]

        message = {
            "bucket": record["s3"]["bucket"]["name"],
            "key": key
        }

        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(message)
        )

    return {"status": "Message sent to SQS"}