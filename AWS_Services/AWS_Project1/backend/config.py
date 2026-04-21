# backend/config.py
# Configuration settings for the project (AWS credentials, bucket names, etc.)


import boto3

AWS_ACCESS_KEY_ID = "AKIAUZJEFHBPJVSDPSY3"
AWS_SECRET_ACCESS_KEY = "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"
REGION = "ap-south-1"

S3_BUCKET_NAME = "rag-ml-pipeline-bucket-purnima"

S3_CLIENT = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION
)
