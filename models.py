import pymongo
from neo4j import GraphDatabase
from redis import Redis

class MongoClient:
    def __init__(self, url="mongodb://localhost:27017"):
        self.mongoUrl = url
        self.mongoClient = pymongo.MongoClient(url)

    def close(self):
        self.mongoClient.close()


class Neo4jClient:
    def __init__(self, url="bolt://localhost:7687", user="[placeholder]", password="[placeholder]"):
        self.neo4jUrl = url
        self.neo4jDriver = GraphDatabase.driver(url, auth=(user, password))

    def close(self):
        self.neo4jDriver.close()


class RedisClient:
    def __init__(self, port=6379):
        self.redisClient = Redis(port=port)

    def close(self):
        self.redisClient.close()