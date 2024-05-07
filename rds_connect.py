# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/
import base64

import boto3
import psycopg2
import json
from botocore.exceptions import ClientError

secret_name = "postgres-v13-rds-debit-card-creds"
client = boto3.client('secretsmanager', region_name='us-east-1')

def get_rds_credentials(secret_name):
    try:
        # Fetch the secret value
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)

        # Check if the secret uses the Secrets Manager binary field
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            secret_dict = json.loads(secret)
            return secret_dict
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            secret_dict = json.loads(decoded_binary_secret)
            return secret_dict
    except Exception as e:
        print(f"Error fetching secret: {e}")
        return None


def connect_and_create_db():
    connection = None

    try:

        credentials = get_rds_credentials(secret_name)
        if credentials:
            print("Fecthed RDS Credentials:")
            username = credentials['username']
            password = credentials['password']
            # Depending on how you've structured your secret, you might need
            # to adjust the keys (e.g., 'username' and 'password') accordingly.
        else:
            print("Failed to fetch credentials.")

        connection = psycopg2.connect(
            host='debit-card-purchase-rds.cl086oceawz9.us-east-1.rds.amazonaws.com',
            port=5432,
            user=username,
            password=password
        )
        connection.autocommit = True


        if connection is not None:
            print("Successfully connected to the RDS instance.")

            cursor = connection.cursor()


            cursor.execute("DROP DATABASE TransactionDB")
            # Create a new database
            cursor.execute("CREATE DATABASE TransactionDB")
            print("Database created successfully.")

            cursor.execute("SELECT datname FROM pg_database")
            print(cursor.fetchall())

            cursor.execute("DROP TABLE customers")

            create_table = """ CREATE TABLE customers (
                              customer_id INT CONSTRAINT no_null NOT NULL,
                              debit_card_number VARCHAR(255) CONSTRAINT no_null1 NOT NULL,
                              bank_name VARCHAR(255) CONSTRAINT no_null2 NOT NULL,
                              total_amount_spend DECIMAL(10,2) CONSTRAINT no_null3 NOT NULL,
                              CONSTRAINT pkey PRIMARY KEY(customer_id,debit_card_number,bank_name))"""

            cursor.execute(create_table)
            print("Table Created Successfully!")

            cursor.execute("SELECT * FROM pg_catalog.pg_tables")
            print(cursor.fetchall())

        else:
            print("Failed to connect to the RDS instance.")
    except psycopg2.Error as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection is not None:
            cursor.close()
            connection.close()
            print("Connection closed.")


if __name__ == "__main__":
    connect_and_create_db()