# 1 Student Risk Detection
# Add a new field:
# at_risk
# Mark students as True if:
# attendance_percentage < 60
# OR
# total_score < 50
import logging
import concurrent.futures
from config.s3_config import *
from boto3.dynamodb.conditions import *

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize DynamoDB resource and table
from botocore.config import Config
import boto3

config = Config(max_pool_connections=50)

dynamodb = boto3.resource(
    "dynamodb",
    config=config
)
table = get_table()


TOTAL_SEGMENTS = 8
def process_segment(segment):
    logging.info(f"Processing segment {segment}...")
    response = table.scan(
        Segment=segment,
        TotalSegments=TOTAL_SEGMENTS,
        ProjectionExpression="student_id, attendance_percentage, total_score, at_risk"
    )
    while True:
        logging.info(f"Segment {segment}: Retrieved {len(response['Items'])} items.")
        for item in response["Items"]:
            attendance = float(item["attendance_percentage"])
            score = float(item["total_score"])
            at_risk = attendance < 60 or score < 50
            if item.get("at_risk") != at_risk:
                table.update_item(
                    Key={"student_id": item["student_id"]},
                    UpdateExpression="SET at_risk = :v",
                    ExpressionAttributeValues={":v": at_risk}
                )
        if "LastEvaluatedKey" not in response:
            break
        response = table.scan(
            Segment=segment,
            TotalSegments=TOTAL_SEGMENTS,
            ProjectionExpression="student_id, attendance_percentage, total_score, at_risk",
            ExclusiveStartKey=response["LastEvaluatedKey"]
        )
    logging.info(f"Completed processing segment {segment}.")


def student_at_risk():
    logging.info("Starting at-risk student detection...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=TOTAL_SEGMENTS) as executor:
        executor.map(process_segment, range(TOTAL_SEGMENTS))
    logging.info("Updated at_risk status for all students.")

# Generate a leaderboard of:
# Top 10 students by total_score

def leaderboard_top_students():
    logging.info("Generating leaderboard of top students...")
    response = table.scan(
        ProjectionExpression="student_id, total_score"
    )
    students = response["Items"]
    students.sort(key=lambda x: x["total_score"], reverse=True)
    top_students = students[:10]
    logging.info("Top 10 students by total score:")
    for student in top_students:
        print(f"Student ID: {student['student_id']}, Total Score: {student['total_score']}")
    logging.info("Leaderboard generation completed.")

if __name__ == "__main__":
    student_at_risk()
    leaderboard_top_students()