import boto3, json

sqs = boto3.client("sqs", region_name="ap-south-1")

QUEUE_URL = "https://sqs.ap-south-1.amazonaws.com/329177708638/rag-pipeline-queue"

response = sqs.send_message(
    QueueUrl=QUEUE_URL,
    MessageBody=json.dumps({"bucket": "test", "key": "raw/test.csv"})
)

print("Message sent!")
print(response)