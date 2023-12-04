import pymongo
import neo4j
import redis
from bson.son import SON

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
    
    def create_text_index(self):
        database = self.client["books"]
        collection = database["books"]
        # Create a text index on the "description" field if it doesn't exist
        index_info = collection.index_information()
        if "description_text" not in index_info:
            collection.create_index([("description", "text")], name="description_text")
    
    def get_recommendations(self, title):
        # Find the document for the provided title
        query = {"Title": title}
        database = self.client["books"]
        collection = database["books"]

        target_book = collection.find_one(query)

        if target_book:
            # Use full-text search to find similar books based on the description
            search_result = collection.find(
                {"$text": {"$search": target_book['description']}},
                {"score": {"$meta": "textScore"}}
            ).sort([("score", {"$meta": "textScore"})]).limit(6)

            # Extract recommended titles
            recommended_titles = [book["Title"] for book in search_result if book["_id"] != target_book["_id"]]

            return recommended_titles
        else:
            print("damn")
            return []


class Neo4jModel:
    def __init__(self, url="bolt://localhost:7687", user="[placeholder]", password="[placeholder]"):
        self.neo4jUrl = url
        self.driver = neo4j.GraphDatabase.driver(url, auth=(user, password))

    def close(self):
        self.driver.close()


class RedisModel:
    def __init__(self, port=6379):
        self.client = redis.Redis(port=port)

    def close(self):
        self.client.close()