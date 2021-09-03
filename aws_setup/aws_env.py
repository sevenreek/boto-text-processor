import os
import boto3
from dotenv import load_dotenv

"""
    Loads AWS constants into global variables from an .env file or
    the environment.
"""
load_dotenv()

AWS_ID = os.getenv("aws_access_key_id")
AWS_SECRET = os.getenv("aws_secret_access_key")
AWS_TOKEN = os.getenv("aws_session_token")
AWS_REGION = os.getenv("aws_region", default="us-east-1")
BUCKET_NAME = os.getenv("bucket_name", default="psoir-bucket")
SQS_NAME = os.getenv("queue_name", default="psoir-sqs")


AWS = boto3.Session(
    aws_access_key_id=AWS_ID,
    aws_secret_access_key=AWS_SECRET,
    aws_session_token=AWS_TOKEN,
    region_name=AWS_REGION
)
S3 = AWS.resource("s3")
SQS = AWS.resource("sqs")
EC2 = AWS.resource("ec2")
