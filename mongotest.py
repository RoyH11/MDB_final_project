import csv
from pymongo import MongoClient

# MongoDB connection parameters
mongo_uri = "mongodb://localhost:27017"  # Replace with your actual connection string
database_name = "test"  # Replace with your actual database name
collection_name = "test"  # Replace with your actual collection name

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

# Path to your CSV file
csv_file_path = "data/books_data.csv"  # Replace with the actual path to your CSV file

# Open and read the CSV file
with open(csv_file_path, "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)

    total_records = sum(1 for row in reader)
    csvfile.seek(0)

    # Iterate over each row in the CSV file
    for i, row in enumerate(reader, start=1):
        # Insert the row as a document into the MongoDB collection
        collection.insert_one(row) # potnetial error here

        progress_percentage = (i / total_records) * 100
        print(f"Progress: {i}/{total_records} records processed ({progress_percentage:.2f} %)", end="\r")

# Close the MongoDB connection
client.close()

print("\nData imported successfully.")
