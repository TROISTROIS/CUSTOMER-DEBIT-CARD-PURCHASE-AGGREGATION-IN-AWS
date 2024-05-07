import boto3

s3 = boto3.client("s3")
target_bucket = "customer-debit-card-daily-transactions"

def upload_to_s3(filename, date_str):
    """Uploads a CSV file to S3 with Hive-style partitioning"""
    file_path = f"raw_data/date={date_str}"  # Hive-style partitioning
    s3.upload_file(f'/{filename}', target_bucket, file_path)
    print(f"File uploaded to S3 Bucket {target_bucket}/{file_path}")
    return

