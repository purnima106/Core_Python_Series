# AWS Project 1

## Overview
This project demonstrates an end-to-end AWS data pipeline.

## Project Structure

```
AWS_Project1/
├── backend/
│   ├── upload.py         # Handles file uploads to S3
│   ├── config.py         # AWS configuration & settings
│
├── lambda/
│   ├── handler.py        # AWS Lambda function handler
│   ├── requirements.txt  # Lambda dependencies
│
├── worker/
│   ├── processor.py      # Background data processor
│   ├── requirements.txt  # Worker dependencies
│
├── dashboard/
│   ├── app.py            # Dashboard application
│
├── scripts/
│   ├── create_athena_table.sql  # Athena table creation script
│
├── data/
│   ├── sample.csv        # Sample input data
│
├── requirements.txt      # Root-level dependencies
└── README.md             # Project documentation
```

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure AWS credentials in `backend/config.py`

## Usage

- **Upload data**: Run `backend/upload.py` to upload files to S3
- **Lambda**: Deploy `lambda/handler.py` to AWS Lambda
- **Worker**: Run `worker/processor.py` for background processing
- **Dashboard**: Launch `dashboard/app.py` to view results
- **Athena**: Execute `scripts/create_athena_table.sql` to set up the Athena table
