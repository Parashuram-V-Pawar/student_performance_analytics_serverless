import json
import random

records = []
start_id = 1000001

for i in range(500):
    student_id = str(start_id + i)

    weekly_hours = round(random.uniform(5, 20), 1)
    attendance = round(random.uniform(50, 100), 1)
    participation = round(random.uniform(3, 10), 1)
    total_score = round(random.uniform(40, 100), 1)

    # Assign grade based on score
    if total_score >= 90:
        grade = "A"
    elif total_score >= 75:
        grade = "B"
    elif total_score >= 60:
        grade = "C"
    elif total_score >= 50:
        grade = "D"
    else:
        grade = "F"

    record = {
        "student_id": student_id,
        "weekly_self_study_hours": str(weekly_hours),
        "attendance_percentage": str(attendance),
        "class_participation": str(participation),
        "total_score": str(total_score),
        "grade": grade
    }

    records.append(record)

# Save to JSON file
with open("data/students_records.json", "w") as f:
    json.dump(records, f, indent=4)

print("JSON file 'students_200_records.json' created successfully.")