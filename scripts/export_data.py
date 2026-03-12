import os
import json
import logging
import pandas as pd
from config.s3_config import *
from decimal import Decimal
from scripts.upload_data import upload_file_to_s3

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize AWS clients and DynamoDB table
s3 = get_s3_client()
dynamodb = dynamodb_resource()
table = get_table()

# Configuring constant variables
EXPORT_FORMAT = "json"

# Convert DynamoDB Decimal to float
def decimal_to_float(obj):
    '''
    DynamoDB returns numeric values as Decimal objects. This helper
    function converts them to float so they can be serialized when
    exporting records to JSON.

    Args:
        obj (Decimal): DynamoDB Decimal object.

    Returns:
        float: Converted float value.

    Raises:
        TypeError: If the object is not a Decimal type.
    '''
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


# Fetch all records from DynamoDB
def fetch_all_records():
    '''
    This function performs a full table scan and handles pagination
    using the `LastEvaluatedKey` attribute returned by DynamoDB.
    All retrieved items are accumulated and returned as a list.

    Returns:
        list[dict]: A list of items retrieved from the DynamoDB table.

    Notes:
        DynamoDB scan operations may return partial results if the
        dataset is large. This function automatically continues
        scanning until all records are fetched.
    '''
    logging.info("Fetching records from DynamoDB...")
    items = []
    response = table.scan()
    items.extend(response["Items"])
    while "LastEvaluatedKey" in response:
        response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        items.extend(response["Items"])
    logging.info(f"Fetched {len(items)} records from DynamoDB")
    return items


# Save file locally
def save_file(items, format_type):
    '''
    The records can be saved in either JSON or CSV format. The output
    file is stored inside the `analytics/` directory, which will be
    created automatically if it does not already exist.

    Args:
        items (list[dict]): List of DynamoDB records to export.
        format_type (str): Output file format. Supported values are
                           "json" and "csv".

    Returns:
        str: Path to the saved file.

    Raises:
        ValueError: If the provided format type is not supported.
    '''
    logging.info(f"Saving file in {format_type} format...")
    os.makedirs("analytics", exist_ok=True)
    if format_type == "json":
        file_name = "analytics/student_performance.json"
        with open(file_name, "w") as f:
            json.dump(items, f, indent=4, default=decimal_to_float)
    elif format_type == "csv":
        file_name = "analytics/student_performance.csv"
        df = pd.DataFrame(items)
        df.to_csv(file_name, index=False)
    else:
        raise ValueError("Unsupported format")
    logging.info(f"File saved locally: {file_name}")
    return file_name


def main():
    '''
    Execute the full student performance export pipeline.

    This function orchestrates the following steps:
    1. Fetch all records from the DynamoDB table.
    2. Save the retrieved records locally in the specified format
       (JSON or CSV).
    3. Upload the exported file to the configured S3 bucket.

    Returns:
        None
    '''
    logging.info("Starting data export process...")
    items = fetch_all_records()
    file_name = save_file(items, EXPORT_FORMAT)
    upload_file_to_s3(file_name, s3_key = "analytics")

if __name__ == "__main__":
    main()