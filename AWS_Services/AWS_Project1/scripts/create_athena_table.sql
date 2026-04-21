-- scripts/create_athena_table.sql
-- SQL script to create an Athena table

CREATE EXTERNAL TABLE curated_data (
    column1 string,
    column2 int
)
STORED AS PARQUET
LOCATION 's3://rag-ml-pipeline-bucket/curated/';