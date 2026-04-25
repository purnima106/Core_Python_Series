# backend/config.py

import os
import boto3
from dotenv import load_dotenv

# Load .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

# AWS config
REGION         = os.environ.get("AWS_DEFAULT_REGION", "ap-south-1")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "rag-ml-pipeline-bucket-purnima")
SQS_QUEUE_URL  = os.environ.get("SQS_QUEUE_URL", "")

# AWS clients
S3_CLIENT  = boto3.client("s3", region_name=REGION)
SQS_CLIENT = boto3.client("sqs", region_name=REGION)