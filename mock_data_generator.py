import csv
from random import randint, choice
from datetime import datetime, timedelta
from faker import Faker
from faker.providers import company

fake = Faker()

# Define customer names
customer_names = [fake.unique.name() for i in range(20)]
assert len(set(customer_names)) == len(customer_names)

# Define bank names
fake.add_provider(company)
bank_names = [fake.unique.company() + " Bank" for y in range(5)]
assert len(set(bank_names)) == len(bank_names)

# Define debit card types
card_types = ["Visa", "Mastercard"]

# Define the number of transactions per day
transactions_per_day = 12

# Dictionary for customer information
customer_information = {}


# Generate 1 transaction for a specific date
def generate_transaction(customer_name, current_date):
    if customer_name not in customer_information:
        # generate card number and assign bank to the customer
        card_number = f"{randint(1000, 9999)}-{randint(1000, 9999)}-{randint(1000, 9999)}-{randint(1000, 9999)}"
        bank_name = choice(bank_names)
        customer_information[customer_name] = {
            "customer_id" :randint(10000000, 99999999),
            "debit_card_number": card_number,
            "debit_card_type": choice(card_types),
            "bank_name":bank_name
        }

    # use information to add customer name
    transaction_data = customer_information[customer_name].copy()
    transaction_data["name"] = customer_name
    # set transaction date to the current date
    transaction_date = str(current_date)
    amount = round(randint(10, 100) + randint(0, 99) / 100, 2)
    transaction_data["transaction_date"] = transaction_date
    transaction_data["amount_spend"] = amount
    return transaction_data


# generate a list of transactions for a particular date
def generate_transactions(num_transactions, current_date):
    transactions = []
    for _ in range(num_transactions):
        transactions.append(generate_transaction(choice(customer_names), current_date))
    return transactions

# write data to a CSV file
def write_to_csv(data, filename):
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["customer_id", "name", "debit_card_number",
                                                  "debit_card_type","bank_name","transaction_date",
                                                  "amount_spend"])
        writer.writeheader()
        writer.writerows(data)
    return

# generate the data and write to csv
def generate_data(current_date, date_str):
    transactions = generate_transactions(transactions_per_day, current_date)
    write_to_csv(transactions, f"date = {date_str}.csv")

    print(f"Generated mock transaction data date = {date_str}.csv and saved in csv files")
    return



# Set the current date
current_date = datetime.now().date()
num_days = 5

# generate data for 5 days
# Loop through the 5 days and generate data for each day
for i in range(num_days):
    # Convert the current date to a string
    date_str = current_date.strftime("%Y-%m-%d")

    # Call the generate_data function with the current date and date string
    generate_data(current_date, date_str)

    # Increment the current date by one day
    current_date -= timedelta(days=1)

