# backend/config.py
# All secrets and config come from .env (never hardcoded here).
# python-dotenv loads .env automatically when this module is imported.

import os
import boto3
from dotenv import load_dotenv

# Load .env from the project root (one level up from backend/)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

# AWS config
REGION         = os.environ.get("AWS_DEFAULT_REGION", "ap-south-1")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "rag-ml-pipeline-bucket-purnima")
SQS_QUEUE_URL  = os.environ.get("SQS_QUEUE_URL", "")

# boto3 automatically reads AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
# from the environment — no need to pass them explicitly.
S3_CLIENT = boto3.client("s3", region_name=REGION)
