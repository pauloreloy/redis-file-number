import boto3
from botocore.exceptions import ClientError
import datetime

# Configuration
bucket_name = 'arquivosgeraispaulo'
object_key = 'teste2.txt'
region = 'us-east-1'

# Initialize the S3 client
s3_client = boto3.client('s3', region_name=region)

# Upload an object
try:
    s3_client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body='This is the original content.'
    )
    print("Object uploaded successfully.")
except ClientError as e:
    print(f"Error uploading object: {e}")

# Set Object Lock retention
try:
    s3_client.put_object_retention(
        Bucket=bucket_name,
        Key=object_key,
        Retention={
            'Mode': 'COMPLIANCE',
            'RetainUntilDate': (datetime.datetime.now() + datetime.timedelta(days=1)).isoformat()
        }
    )
    print("Object retention set successfully.")
except ClientError as e:
    print(f"Error setting object retention: {e}")

# Attempt to overwrite the same object
try:
    s3_client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body='This is the new content.'
    )
    print("Object overwritten successfully.")
except ClientError as e:
    print(f"Error overwriting object: {e}")
