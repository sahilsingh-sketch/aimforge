import boto3
from botocore.client import Config

import os

url = 'https://s3.us-east-005.backblazeb2.com'
key_id = os.getenv("B2_KEY_ID", "your_b2_key_id")
app_key = os.getenv("B2_APP_KEY", "your_b2_app_key")
bucket = 'AimForge'

b2 = boto3.client(
    's3',
    endpoint_url=url,
    aws_access_key_id=key_id,
    aws_secret_access_key=app_key,
    config=Config(signature_version='s3v4')
)
try:
    print("Testing upload...")
    b2.put_object(Bucket=bucket, Key='test.txt', Body=b'hello world')
    print("Upload succeeded!")
except Exception as e:
    print(f"Upload failed: {e}")
