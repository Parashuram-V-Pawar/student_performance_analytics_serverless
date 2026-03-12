# import statements
import logging
from config.s3_config import dynamodb_resource
from boto3.dynamodb.conditions import *

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize DynamoDB resource and table
dynamodb = dynamodb_resource()
table = dynamodb.Table("student_performance")

def query_top_students_by_gradea():
    '''
    Retrieve the top 10 students with grade 'A' using the
    'grade_total_score_index', ordered by highest total score.
    '''
    logging.info("Querying top students with grade A...")
    result = table.query(
        IndexName="grade_total_score_index",
        KeyConditionExpression=Key("grade").eq("A"),
        ProjectionExpression="student_id, grade",
        ScanIndexForward=False,
        Limit=10
    )
    logging.info("Top students with grade A:")
    for item in result["Items"]:
        print(f"Student ID: {item['student_id']}, Grade: {item['grade']}")
    logging.info("Finished querying top students with grade A.")

def query_students_with_highest_scores():
    '''
    Retrieve students with the highest total score among
    those who have grade 'A'.
    '''
    logging.info("Querying students with highest scores...")
    result = table.query(
        IndexName="grade_total_score_index",
        KeyConditionExpression = Key("grade").eq("A"),
        ScanIndexForward=False,
        Limit=1
    )
    highest_score = result["Items"][0]["total_score"]
    result2 = table.query(
        IndexName="grade_total_score_index",
        KeyConditionExpression = Key("grade").eq("A") & Key("total_score").eq(highest_score),
        ProjectionExpression="student_id, grade, total_score",
    )
    logging.info("Students with highest scores:")
    for item in result2["Items"]:
        print(f"Student ID: {item['student_id']}, Grade: {item['grade']}, Total Score: {item['total_score']}")

    LastEvaluatedKey = result.get("LastEvaluatedKey")
    while LastEvaluatedKey:
        result = table.query(
            IndexName="grade_total_score_index",
            KeyConditionExpression = Key("grade").eq("A") & Key("total_score").eq(highest_score),
            ProjectionExpression="student_id, grade, total_score",
            ExclusiveStartKey=LastEvaluatedKey
        )
        for item in result["Items"]:
            print(f"Student ID: {item['student_id']}, Grade: {item['grade']}, Total Score: {item['total_score']}")
        LastEvaluatedKey = result.get("LastEvaluatedKey")
    logging.info("Finished querying students with highest scores.")

if __name__ == "__main__":
    query_top_students_by_gradea()
    query_students_with_highest_scores()

    