import pymongo
from pymongo import MongoClient

# Connect to the MongoDB server
client = MongoClient("mongodb://localhost:27017")  # Replace with your actual connection string
db = client["books"]  # Replace with your actual database name
collection = db["books_data"]  # Replace with your actual collection name

# Define the query criteria
query = {"Title": "Its Only Art If Its Well Hung!"}

# Execute the findOne query
result = collection.find_one()

# Print the result
print(result)

# Close the MongoDB connection
client.close()
