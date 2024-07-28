import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import datetime

def upload_file_to_s3_with_object_lock(bucket_name, file_path, object_key):
    # Initialize a session using Amazon S3
    s3_client = boto3.client('s3')

    try:
        # Upload the file
        s3_client.upload_file(file_path, bucket_name, object_key)

        # Apply object lock configuration
        s3_client.put_object_retention(
            Bucket=bucket_name,
            Key=object_key,
            Retention={
                'Mode': 'GOVERNANCE',  # or 'COMPLIANCE'
                'RetainUntilDate': (datetime.datetime.now() + datetime.timedelta(days=1)).isoformat()
            }
        )
        print(f"File {file_path} uploaded to {bucket_name}/{object_key} with object lock for 1 day.")
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available")
    except PartialCredentialsError:
        print("Incomplete credentials provided")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    bucket_name = 'arquivosgerais'
    file_path = './teste.txt'
    object_key = 'teste.txt'

    upload_file_to_s3_with_object_lock(bucket_name, file_path, object_key)