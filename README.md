# CUSTOMER-DEBIT-CARD-PURCHASE-AGGREGATION-IN-AWS 

<br>
In this project, I will develop a data processing pipeline using AWS services and Python. The goal is to aggregate customer debit card purchases on a daily basis and update the aggregated data in a PostgreSQL table hosted on Amazon RDS. I will work with AWS S3 for data storage, AWS Glue for data processing, and Amazon RDS for data persistence.
<br>

## Objectives
<br>
1. Generate mock daily transaction data and store it in CSV files.<br>
2. Upload daily transaction CSV files to an AWS S3 bucket using a Hive-style partition.<br>
3. Set up a PostgreSQL table in Amazon RDS to store aggregated transaction data.<br>
4. Write an AWS Glue job to process daily transactions from S3, aggregate them, and update the RDS PostgreSQL table. <br>

