# Import statements
import os
import logging
from botocore.exceptions import *
from scripts.csv_to_json import csv_to_json_func
from config.s3_config import get_s3_client, BUCKET_NAME

# Initialize logging
logging.basicConfig(level=logging.INFO)

def upload_file_to_s3(local_file = 'data/students_records.json', s3_key = "raw", bucket_name = BUCKET_NAME):
    '''
    Upload a CSV or JSON file to an S3 bucket.
    If the input file is CSV, it is converted to JSON before uploading.

    Args:
        local_file (str): Path to the local file.
        s3_key (str): S3 prefix (folder) where the file will be stored.
        bucket_name (str): Target S3 bucket name.
    '''
    s3 = get_s3_client()
    file_ext = os.path.splitext(local_file)[1].lower()
    try:
        if file_ext == ".csv":
            json_file = csv_to_json_func(local_file)
        elif file_ext == ".json":
            json_file = local_file
        else:
            raise ValueError("Unsupported file format. Only CSV and JSON are allowed.")
        if not os.path.exists(json_file):
            logging.error("File doesn't exist. please check the path")
            return
        try:
            s3.upload_file(
                json_file,
                bucket_name,
                f'{s3_key}/{os.path.basename(json_file)}'
            )
            logging.info(f"Upload successful: s3://{bucket_name}/{s3_key}/{os.path.basename(json_file)}")
        except NoCredentialsError:
            logging.error("AWS credentials not available.")
        except Exception as e:
            logging.error(f"Upload failed: {e}")
    except ValueError as ve:
        logging.error(ve)

def list_s3_files(bucket_name = BUCKET_NAME):
    '''
    List all files available in the specified S3 bucket.

    Args:
        bucket_name (str): Name of the S3 bucket.
    '''
    s3 = get_s3_client()
    try:
        response = s3.list_objects_v2(Bucket = bucket_name)
        if 'Contents' in response:
            logging.info(f"Files in bucket '{bucket_name}':")
            for obj in response['Contents']:
                logging.info(f" - {obj['Key']}")
        else:
            logging.info(f"No files found in bucket '{bucket_name}'.")
    except Exception as e:
        logging.error(f"Failed to list files: {e}")

if __name__ == "__main__":
    upload_file_to_s3()
    list_s3_files()