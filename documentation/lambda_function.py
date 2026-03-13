import os
import json
import boto3
from decimal import Decimal

DYNAMO_TABLE = os.environ['DYNAMO_TABLE']

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table(DYNAMO_TABLE)
def get_performance_category(score):
    # This function categorizes the performance based on the score
    if score >= 90:
        return "Excellent"
    elif score >= 75:
        return "Good"
    elif score >= 50:
        return "Average"
    else:
        return "Poor"

def lambda_handler(event, context):
    # TODO implement
    ## This function reads json data from s3 and stores it in dynamodb
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]

    response = s3.get_object(Bucket = bucket, Key = key)
    file_content = response["Body"].read().decode("utf-8")
    data = json.loads(file_content, parse_float=Decimal)

    with table.batch_writer() as batch:
        for student in data:
            student["student_id"] = int(student["student_id"])
            student["weekly_self_study_hours"] = Decimal(student["weekly_self_study_hours"])
            student["attendance_percentage"] = Decimal(student["attendance_percentage"])
            student["class_participation"] = Decimal(student["class_participation"])
            student["grade"] = student["grade"]
            student["total_score"] = Decimal(student["total_score"])
            score = float(student["total_score"])
            student["performance_category"] = get_performance_category(score)
            batch.put_item(Item=student)
        
    
    return {
        'statusCode': 200,
        'message': "Records inserted successfully"
    }
