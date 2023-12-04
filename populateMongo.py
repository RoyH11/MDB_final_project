from models import MongoClient
import csv

def import_data(collection_name, path):

    # MongoDB connection parameters
    mongo_uri = "mongodb://localhost:27017"  
    database_name = "books"  

    # Connect to MongoDB
    client = MongoClient(mongo_uri).mongoClient

    db = client[database_name]
    collection = db[collection_name]

    # Open and read the CSV file
    with open(path, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        total_records = sum(1 for _ in reader)  # Get the total number of records
        csvfile.seek(0)  # Reset the file pointer to the beginning

        # Iterate over each row in the CSV file
        for i, row in enumerate(reader, start=1):
            # skip headers
            if i == 1:
                continue

            # Insert the row as a document into the MongoDB collection
            collection.insert_one(row)

            # Print progress
            progress_percentage = (i / total_records) * 100
            print(f"Progress: {i}/{total_records} records processed ({progress_percentage:.2f}%)", end="\r")

    # Close the MongoDB connection
    client.close()

    print(f"\n{collection_name} successfully imported.\n")


if __name__ == "__main__":
    import_data("books", "data/books_data.csv")
    import_data("ratings", "data/Books_rating.csv")

