from neo4j import GraphDatabase

class Neo4jClient:
    def __init__(self, url="bolt://localhost:7687", user="[placeholder]", password="[placeholder]"):
        self.neo4jUrl = url
        self.neo4jDriver = GraphDatabase.driver(url, auth=(user, password))

    def close(self):
        self.neo4jDriver.close()