import pymongo
import neo4j
import redis

class MongoModel:
    def __init__(self, url="mongodb://localhost:27017"):
        self.mongoUrl = url
        self.client = pymongo.MongoClient(url)

    def close(self):
        self.client.close()


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