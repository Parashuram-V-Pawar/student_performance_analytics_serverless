# import statements
import logging
from config.s3_config import dynamodb_client

#Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize DynamoDB client
dynamodb = dynamodb_client()

def create_gsi_on_grade_score():
    '''
    Create a Global Secondary Index (GSI) on the student_performance table
    using grade as the partition key and total_score as the sort key.
    '''
    try:
        logging.info("Creating GSI on grade and total score...")
        dynamodb.update_table(
            TableName="student_performance",

            AttributeDefinitions = [
                {
                    "AttributeName" : "grade",
                    "AttributeType" : "S"
                },
                {
                    "AttributeName" : "total_score",
                    "AttributeType" : "N"
                }
            ],
            GlobalSecondaryIndexUpdates = [
            {
                "Create": {
                    "IndexName": "grade_total_score_index",

                    "KeySchema": [
                        {
                            "AttributeName": "grade",
                            "KeyType": "HASH"
                        },
                        {
                            "AttributeName": "total_score",
                            "KeyType": "RANGE"
                        }
                    ],

                    "Projection": {
                        "ProjectionType": "ALL"
                    }
                }
            }
            ]
        )
        logging.info("GSI creation request submitted.")
    except Exception as e:
        logging.error("Error creating GSI: %s", e)

if __name__ == "__main__":
    create_gsi_on_grade_score()