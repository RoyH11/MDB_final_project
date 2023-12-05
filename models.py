import pymongo
import neo4j
import json

class MongoModel:
    def __init__(self, url="mongodb://localhost:27017"):
        self.mongoUrl = url
        self.client = pymongo.MongoClient(url)

    def close(self):
        self.client.close()

    def get_all_titles(self):
        titles = []
        database = self.client["books"]
        collection = database["books"]

        documents = collection.find()

        for document in documents:
            title = document.get("Title")
            if title:
                titles.append(title)

        return titles
    
    def get_book(self, title):
        database = self.client["books"]
        collection = database["books"]

        book_document = collection.find_one({"Title": title})
        
        book_dict = {
                key: value for key, value in book_document.items() if key != "_id"
            }
        return book_dict
    
    def create_text_index(self):
        database = self.client["books"]
        collection = database["books"]

        # Create a text index on the "description" field if it doesn't exist
        index_info = collection.index_information()
        if "description_text" not in index_info:
            collection.create_index([("description", "text")], name="description_text")
            print("Created text index on description")

    def get_recommendations(self, title):
        database = self.client["books"]
        collection = database["books"]

        target_book = collection.find_one({"Title": title})

        search_result = collection.find(
                {"$text": {"$search": target_book['description']}},
                {"score": {"$meta": "textScore"}}
            ).sort([("score", {"$meta": "textScore"})]).limit(6)

        # Extract recommended books as dictionaries
        recommended_books = [
            {
                "title": book["Title"],
                "description": book["description"],
                "similarity": book["score"],
                "categories": book["categories"]
            }
            for book in search_result if book["_id"] != target_book["_id"]
        ]

        return recommended_books


class Neo4jModel:
    def __init__(self, url="bolt://localhost:7687", user="[placeholder]", password="[placeholder]"):
        self.neo4jUrl = url
        self.driver = neo4j.GraphDatabase.driver(url, auth=(user, password))

    def close(self):
        self.driver.close()
