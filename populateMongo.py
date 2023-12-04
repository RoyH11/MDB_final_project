from models import MongoModel
import csv

def import_data(collection_name, path):

    # MongoDB connection parameters
    mongo_uri = "mongodb://localhost:27017"  
    database_name = "books"  

    # Connect to MongoDB
    model = MongoModel(mongo_uri)

    client = model.client

    db = client[database_name]
    collection = db[collection_name]

    rows_to_insert = []


    # TODO batch size dont do all at once

    # Open and read the CSV file
    with open(path, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        total_records = sum(1 for _ in reader)  # Get the total number of records
        csvfile.seek(0)  # Reset the file pointer to the beginning

        # Iterate over each row in the CSV file
        for i, row in enumerate(reader, start=1):

            if i == 1:
                continue

            rows_to_insert.append(row)
            # Print progress
            progress_percentage = (i / total_records) * 100
            print(f"Progress: {i-1}/{total_records} records processed ({progress_percentage:.2f}%)", end="\r")


    collection.insert_many(rows_to_insert)
    # Close the MongoDB connection
    model.close()

    print(f"\n{collection_name} successfully imported.\n")


if __name__ == "__main__":
    import_data("books", "data/books_data.csv")
    import_data("ratings", "data/Books_rating.csv")

