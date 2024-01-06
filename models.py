import csv
from datetime import datetime

# Function to add a new record to the CSV file
def add_record(csv_file, record):
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(record)

# Function to read all records from the CSV file
def read_records(csv_file):
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)

def read_records_2(csv_file):
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        records = list(reader)
    return records

# Example usage
csv_file_path = 'database.csv'

# Adding a new record
# record_to_add = ['Type1', 'ID001', str(datetime.now()), str(datetime.now()), str(datetime.now())]

# record_to_add = ['Type', 'ID', 'last_checked', 'last_modified', 'last_vectorised', 'merged/not-merged']

# add_record(csv_file_path, record_to_add)

# Reading all records
# read_records(csv_file_path)

def update_record(csv_file, record_id, new_value, column_index):
    records = read_records_2(csv_file)

    for record in records:
        if record[1] == record_id:  # Assuming ID is in the second column
            record[column_index] = new_value
            break

    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(records)

# Example usage
csv_file_path = 'database.csv'
record_id_to_update = '02'
new_last_modified_value = 'merged'
column_index_to_update = 5  # Assuming 'last modified' is the fourth column (index 3)

# # Update a single value in the record with the specified ID
update_record(csv_file_path, record_id_to_update, new_last_modified_value, column_index_to_update)

# # Reading all records after the update
read_records(csv_file_path)