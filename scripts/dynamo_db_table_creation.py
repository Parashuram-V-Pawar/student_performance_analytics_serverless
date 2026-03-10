import logging
from config.s3_config import dynamodb_client

logging.basicConfig(level=logging.INFO)

dynamodb = dynamodb_client()

logging.info("Table creation started...")
try:
    table = dynamodb.create_table(
        TableName="student_performance",
        KeySchema=[{
            "AttributeName":"student_id",
            "KeyType":'HASH'
        }],
        AttributeDefinitions=[
            {
                "AttributeName":"student_id", "AttributeType":'S'
            }
        ],
        BillingMode="PAY_PER_REQUEST"
    )
    logging.info("Table created successfully...")

except dynamodb.exceptions.ResourceInUseException:
    logging.info("Table already exists")
