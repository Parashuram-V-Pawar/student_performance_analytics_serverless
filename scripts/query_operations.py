import logging
from decimal import Decimal
from boto3.dynamodb.conditions import *
from config.s3_config import dynamodb_resource


logging.basicConfig(level=logging.INFO)

dynamodb = dynamodb_resource()
table = dynamodb.Table("student_performance")

def query_attendance_morethan_90():
    logging.info("Querying students with attendance more than 90%...")
    result = table.scan(
        FilterExpression=Attr("attendance_percentage").gt(Decimal("90.0"))
    )
    print("Students with attendance more than 90%:")
    for item in result["Items"]:
        print(item)
    logging.info("Query completed. Found %d students with attendance more than 90%%.", len(result["Items"]))


def query_weekly_study_hours_morethan_10():
    logging.info("Querying students with weekly study hours more than 10...")
    result = table.scan(
        FilterExpression=Attr("weekly_self_study_hours").gt(Decimal("10.0"))
    )
    print("Students with weekly study hours more than 10:")
    for item in result["Items"]:
        print(item)
    logging.info("Query completed. Found %d students with weekly study hours more than 10.", len(result["Items"]))


def query_students_in_excellent_performance():
    logging.info("Querying students with excellent performance...")
    result = table.scan(
        FilterExpression=Attr("performance_category").eq("Excellent")
    )
    print("Students with excellent performance:")
    for item in result["Items"]:
        print(item)
    logging.info("Query completed. Found %d students with excellent performance.", len(result["Items"]))


if __name__ == "__main__":
    query_attendance_morethan_90()
    query_weekly_study_hours_morethan_10()
    query_students_in_excellent_performance()
