import pymongo
from pymongo import MongoClient

# Connect to the MongoDB server
client = MongoClient("mongodb://localhost:27017")  # Replace with your actual connection string
db = client["books"]  # Replace with your actual database name
collection = db["books_data"]  # Replace with your actual collection name

# Define the query criteria
query = {"Title": "Its Only Art If Its Well Hung!"}

# Execute the findOne query
result = collection.find_one(query)

# Print the result on the screen
if result:
    print("Book Found:")
    print("Title:", result["Title"])
    print("Authors:", result["authors"])
    print("Image:", result["image"])
    print("Preview Link:", result["previewLink"])
    print("Published Date:", result["publishedDate"])
    print("Info Link:", result["infoLink"])
    print("Categories:", result["categories"])
else:
    print("Book not found.")

# Close the MongoDB connection
client.close()
