# Serverless Student Performance Analytics System

## Project Overview
This project implements a serverless data processing system on AWS to analyze student academic performance data.
The system automatically processes datasets uploaded by faculty members, stores student records, and enables performance analysis.

---
## System Architecture
Faculty uploads dataset → S3 Bucket → S3 Event Trigger → Lambda Function → DynamoDB Table
```
Dataset uploaded to S3
          ↓
S3 triggers Lambda function
          ↓
Lambda reads dataset and processes records
          ↓
Performance category calculated
          ↓
Records stored in DynamoDB
          ↓
Python scripts perform CRUD and analytics operations
          ↓ 
Export Data to S3
```
---
## Dataset Information
### Dataset Source:
https://www.kaggle.com/datasets/nabeelqureshitiii/student-performance-dataset/data

### Dataset Fields:
|Field	| Description |
|--------|------------|
| student_id	| Unique ID of student |
| weekly_self_study_hours	| Weekly study hours |
| attendance_percentage	| Attendance percentage |
| class_participation	| Participation score |
| total_score	| Final performance score |
| grade	| Final grade |

---
## Technology and Services Used
```
Cloud Platform: AWS
AWS Services:
    - Amazon S3 – Dataset storage and event trigger
    - AWS Lambda – Serverless data processing
    - Amazon DynamoDB – NoSQL database for storing student records
Programming Language: Python 3
Libraries: boto3
```

---
## Features
- Automatic dataset processing using S3 trigger and Lambda
- Storage of processed records in DynamoDB
- Full CRUD operations using Python scripts
- Query operations for analytics
- Global Secondary Index (GSI) for efficient queries
- Student risk detection
- Leaderboard generation
- Export records to JSON and CSV

---
### Installation
```
Clone the repository
-> git clone https://github.com/your-repository/serverless-student-performance-analytics.git

Move to project folder
-> cd serverless-student-performance-analytics

Create virtual environment
-> python3 -m venv venv
-> source venv/bin/activate

Install dependencies
-> pip install -r requirements.txt
```

## Execution
```
Run Python scripts
- python3 -m scripts.dynamo_db_table_creation

Note : After crearting table, create a lambda trigger
    Refer lambda_functioon.txt in documentation for Steps to create a lambda function.

After creating lambda function execute these.
- python3 -m scripts.upload_data   
- python3 -m scripts.crud_operations      
- python3 -m scripts.query_operations   
- python3 -m scripts.gsi_indexing  
- python3 -m scripts.queries_on_gsi
- python3 -m scripts.export_data  
- python3 -m scripts.advanced_queries    
```

## Author
```
Parashuram V Pawar
GitHub username: Parashuram-V-Pawar
```