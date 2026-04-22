-- scripts/create_athena_table.sql
-- Creates the Athena external table pointing at the curated Parquet dataset folder.
-- Run this AFTER the Glue crawler has detected the schema, OR use it as a
-- manual override when you want fine-grained control over column types.
--
-- Bucket  : rag-ml-pipeline-bucket-purnima
-- Dataset : curated/sample_dataset/   (folder-based, NOT a single .parquet file)
-- Format  : Parquet + Snappy compression

CREATE EXTERNAL TABLE IF NOT EXISTS sample_dataset (
    order_id           STRING,
    order_item_id      BIGINT,
    product_id         STRING,
    seller_id          STRING,
    shipping_limit_date STRING,
    price              DOUBLE,
    freight_value      DOUBLE,
    processed          BOOLEAN
)
STORED AS PARQUET
LOCATION 's3://rag-ml-pipeline-bucket-purnima/curated/sample_dataset/'
TBLPROPERTIES ('parquet.compress' = 'SNAPPY');

-- Verify with:
-- SELECT * FROM sample_dataset LIMIT 10;