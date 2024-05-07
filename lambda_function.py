import json
from mock_data_generator import *
from upload_to_s3 import *
from rds_connect import *
from datetime import datetime, timedelta

# Set the current date as today
start_date = datetime.now().date()
num_days = 5


def lambda_handler(event, context):
    current_date = start_date

    # Generate data for 5 days
    for i in range(num_days):
        # Convert the current date to a string
        date_str = current_date.strftime("%Y-%m-%d")

        # Call the generate_data function with the current date and date string
        generate_data(current_date, date_str)

        # Upload the generated CSV to S3
        upload_to_s3(f"date = {date_str}.csv", date_str)

        # Increment the current date by one day
        current_date += timedelta(days=1)

    # Connect to RDS, create customers database and customer_transactions table
    connect_and_create_db()

    return {
        'statusCode': 200,
        'body': json.dumps(f'Customer Data Generated, Created new RDS DB and Table.')
    }