from pymongo import MongoClient

class MongoClient:
    def __init__(self, url="mongodb://localhost:27017/[placeholder]"):
        self.mongoUrl = url
        self.mongoClient = MongoClient(url)

    def close(self):
        self.mongoClient.close()