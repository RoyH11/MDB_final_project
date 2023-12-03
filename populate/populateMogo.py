from pymongo import MongoClient
import pandas as pd

def import_data(collection_name, my_csv_file_path):

    # Set up MongoDB connection
    client = MongoClient("mongodb://192.168.240.1:27017")
    db = client["books"]
    print(db)
    collection = db[collection_name]
    print(collection)

    # Specify the CSV file path
    csv_file_path = my_csv_file_path

    # Set the batch size
    batch_size = 50

    # Line count
    line_count = 0

    # Read CSV file in chunks and insert data into MongoDB in batches
    for chunk in pd.read_csv(csv_file_path, chunksize=batch_size):
        # Convert the chunk to a list of dictionaries (each row becomes a dictionary)
        data = chunk.to_dict(orient="records")

        # Increment line count
        line_count += len(data)

        # Insert data into MongoDB
        collection.insert_many(data)

        # Print progress
        print(f"Processed {line_count} lines.")
        
    print(f"{csv_file_path} imported successfully.")




if __name__ == "__main__":
    import_data("books_data", "data/books_data.csv")
    import_data("books_rating", "data/Books_rating.csv")

