import logging
from config.s3_config import dynamodb_resource
from decimal import Decimal

logging.basicConfig(level=logging.INFO)

dynamodb = dynamodb_resource()
table = dynamodb.Table("student_performance")

# Function to categorizes the performance based on the score
def get_performance_category(score):
    if score >= 90:
        return "Excellent"
    elif score >= 75:
        return "Good"
    elif score >= 50:
        return "Average"
    else:
        return "Poor"


# Function to insert a new student record
def insert_record(table,  student_id, weekly_hours, attendance, participation, score, grade):
    logging.info("Inserting new record into the table...")
    table.put_item(
        Item={
            "student_id": student_id,
            "weekly_self_study_hours": weekly_hours,
            "attendance_percentage": attendance,
            "class_participation": participation,
            "total_score": score,
            "grade": grade,
            "performance_category": get_performance_category(score)
        }
    )
    logging.info("Insertion completed...")

# Function to retrieve student performance data using: student_id
def read_data(table, student_id):
    logging.info("Reading data from DynamoDB...")
    result = table.get_item(
        Key = {
            "student_id": student_id
        }
    )
    print(result["Item"])
    logging.info("Reading completed...")

# Function to update records
def update_record(table, student_id, column_name, new_value):
    logging.info("Updating existing data...")
    table.update_item(
        Key = {
            "student_id": student_id
        },
        UpdateExpression = f"SET {column_name} = :ap",
        ExpressionAttributeValues = {
            ":ap" : new_value
        }
    )
    logging.info("Updation completed...")

# Function to delete a record
def delete_record(table, student_id):
    logging.info("Deleting record...")
    table.delete_item(
        Key = {
            "student_id": student_id
        }
    )
    logging.info("Record deleted...")


# Main execution
if __name__ == "__main__":
    insert_record(
        table,
        student_id = 1000001,
        weekly_hours = Decimal("14.6"),
        attendance = Decimal("75.7"),
        participation = Decimal("9.5"),
        score = Decimal("45.9"),
        grade = "B"
    )
    read_data(table, student_id = 1000001)
    update_record(table, 
        student_id = 1000001, 
        column_name = 'attendance_percentage', 
        new_value = Decimal("80.4")
    )
    delete_record(table, student_id = 1000001)