import logging
from config.s3_config import dynamodb_client

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize dynamodb client
dynamodb = dynamodb_client()

# Table creation logic
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
                "AttributeName":"student_id", "AttributeType":'N'
            }
        ],
        BillingMode="PAY_PER_REQUEST"
    )
    logging.info("Table created successfully...")
except dynamodb.exceptions.ResourceInUseException:
    logging.info("Table already exists")
    
dynamodb.get_waiter('table_exists').wait(TableName='student_performance')
logging.info("Table is now active")