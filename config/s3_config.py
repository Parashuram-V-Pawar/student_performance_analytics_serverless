import os
import boto3
from dotenv import load_dotenv

# -----------------------------------------------------------------------
# Load environment variables
# -----------------------------------------------------------------------
load_dotenv()

# -----------------------------------------------------------------------
# AWS configuration
# -----------------------------------------------------------------------
AWS_REGION = os.getenv("AWS_REGION")
BUCKET_NAME = os.getenv("BUCKET_NAME")

# -----------------------------------------------------------------------
# client initialization functions
# -----------------------------------------------------------------------
def get_s3_client():
    session = boto3.Session(region_name=AWS_REGION)
    return session.client("s3")

def dynamodb_client():
    session = boto3.Session(region_name=AWS_REGION)
    return session.client("dynamodb")