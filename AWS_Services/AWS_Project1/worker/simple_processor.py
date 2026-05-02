import os
import boto3
import pandas as pd
import io
from dotenv import load_dotenv

# Load .env from project root (two levels up from worker/)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

BUCKET = os.environ.get("S3_BUCKET_NAME", "rag-ml-pipeline-bucket-purnima")
REGION = os.environ.get("AWS_DEFAULT_REGION", "ap-south-1")

s3_client = boto3.client("s3", region_name=REGION)

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
                print(f"  [WARN] Could not cast '{col}' to {dtype}: {e}")
    df["processed"] = True
    return df


def process_latest_file():
    print(f"Scanning s3://{BUCKET}/raw/ ...")
    response = s3_client.list_objects_v2(Bucket=BUCKET, Prefix="raw/")
    files = [f for f in response.get("Contents", []) if f["Key"].endswith(".csv")]

    if not files:
        print("No CSV files found in raw/")
        return

    # Sort by LastModified so we always pick the newest file
    latest = sorted(files, key=lambda f: f["LastModified"])[-1]["Key"]
    print(f"Processing: s3://{BUCKET}/{latest}")

    # --- Read ---
    obj = s3_client.get_object(Bucket=BUCKET, Key=latest)
    df = pd.read_csv(io.BytesIO(obj["Body"].read()))
    print(f"  Rows: {len(df)}, Columns: {list(df.columns)}")

    # --- Enforce schema ---
    df = enforce_schema(df)

    # --- Derive folder-based output path (NOT a single file) ---
    # raw/sample.csv  →  curated/sample_dataset/
    filename = latest.split("/")[-1]                         # e.g. sample.csv
    dataset_name = filename.replace(".csv", "_dataset")      # e.g. sample_dataset
    output_path = f"s3://{BUCKET}/curated/{dataset_name}/"

    print(f"  Writing dataset → {output_path}")

    # --- Write folder-based Parquet via pandas + s3fs ---
    df.to_parquet(
        output_path,
        engine="pyarrow",
        index=False,
        compression="snappy",
        storage_options={"client_kwargs": {"region_name": REGION}},
    )

    print(f"  ✅ Dataset saved: {output_path}")
    print("  → Re-run your Glue crawler, then query Athena.")


if __name__ == "__main__":
    process_latest_file()