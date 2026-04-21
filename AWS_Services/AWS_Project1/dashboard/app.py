# dashboard/app.py
# Streamlit or Flask dashboard for visualizing data

import streamlit as st
import boto3

st.title("S3 Data Pipeline Dashboard")

s3 = boto3.client("s3")

bucket = "rag-ml-pipeline-bucket-purnima"

response = s3.list_objects_v2(Bucket=bucket, Prefix="curated/")

files = response.get("Contents", [])

st.write("Processed Files:")

for file in files:
    st.write(file["Key"])