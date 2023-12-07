import pymongo
import neo4j
import re

class MongoModel:
    def __init__(self, url="mongodb://localhost:27017"):
        self.mongoUrl = url
        self.client = pymongo.MongoClient(url)
        self.database = self.client["books"]
        self.collection = self.database["books"]

    def close(self):
        self.client.close()

    def get_all_titles(self):
        titles = []
        documents = self.collection.find()

        for document in documents:
            title = document.get("Title")
            if title:
                titles.append(title)

        return titles
    
    def create_index(self):
        # Create a text index on the "description, Title, and categories" fields if it doesn't exist
        index_info = self.collection.index_information()
        if "description_title_categories_text" not in index_info:
            self.collection.create_index([("description", "text"), ("Title", "text")], 
                                    name="description_Title_categories_text", 
                                    weights={"description": 1, "Title": 2, "categories": 2})
            
            print("Created text index on description, Title, and categories")

    def get_book_by_title(self, title):
        regex_title = re.compile(title, re.IGNORECASE)

        target_book = self.collection.find_one({"Title": title})
        if not target_book:
            target_book = self.collection.find_one({"Title": {"$regex": regex_title}})
            
        return {
            "Title": target_book["Title"],
            "description": target_book["description"],
            "categories": target_book["categories"]
        }

    def get_recommendations(self, title):
        target_book = self.collection.find_one({"Title": title})

        if not target_book:
            return []
        
        self.create_index()

        search_result = self.collection.find(
        {
            "$text": {"$search": f'{title} {target_book["description"]} {target_book["categories"]}'},
        },
        {"Title": 1, "description": 1, "categories": 1, "score": {"$meta": "textScore"}}).sort([("score", {"$meta": "textScore"})]).limit(6)

        max_similarity = search_result[0]["score"]

        # Extract recommended books as dictionaries
        recommended_books = [
            {
                "Title": book["Title"],
                "description": book["description"],
                "similarity": f"{book['score']/max_similarity*100:.2f}%",
                "categories": book["categories"]
            }
            for book in search_result if book["_id"] != target_book["_id"]
        ]

        # for if description fails
        if len(recommended_books) != 5:
            search_result = self.collection.find(
            {
                "$text": {"$search": f'{title} {target_book["categories"]}'},
            },
            {"Title": 1, "description": 1, "categories": 1, "score": {"$meta": "textScore"}}).sort([("score", {"$meta": "textScore"})]).limit(6)

            max_similarity = search_result[0]["score"]

            recommended_books = [
                {
                    "Title": book["Title"],
                    "description": book["description"],
                    "similarity": f"{book['score']/max_similarity*100:.2f}%",
                    "categories": book["categories"]
                }
                for book in search_result if book["_id"] != target_book["_id"]
            ]

        return recommended_books


class Neo4jModel:
    def __init__(self, url="bolt://localhost:7687", user="neo4j", password="password"):
        self.url = url
        self.driver = neo4j.GraphDatabase.driver(url, auth=(user, password))

    def close(self):
        self.driver.close()

    def get_all_user_ids(self):
        with self.driver.session() as session:
            result = session.run("MATCH (u:User) RETURN DISTINCT u.User_id")
            user_ids = [record["u.User_id"] for record in result]
            return user_ids
        
    def get_custom_recommendation(self, username):
        with self.driver.session() as session:
            query = """
                    MATCH (u:User {User_id: $userId})-[:RATED]->(bookU:Book) 
                    WITH u, COLLECT(bookU) AS userBooks 

                    MATCH (otherUser:User)-[:RATED]->(bookOther:Book) 
                    WHERE otherUser <> u 
                    WITH otherUser, COLLECT(bookOther) AS otherUserBooks, userBooks 

                    WITH otherUser, 
                        [book in otherUserBooks WHERE book IN userBooks | book] AS sharedBooks, 
                        [book in otherUserBooks WHERE NOT book IN userBooks | book] AS nonSharedBooks 

                    WHERE SIZE(nonSharedBooks) >= 1 

                    WITH sharedBooks, nonSharedBooks, otherUser 
                    ORDER BY SIZE(sharedBooks) DESC 
                    LIMIT 1 

                    UNWIND nonSharedBooks AS book 

                    WITH book, AVG(book.score) AS avgRating, sharedBooks, otherUser  
                    ORDER BY avgRating DESC 
                    LIMIT 1 

                    RETURN book.Title as title, [title IN sharedBooks | title.Title] as sharedBooksTitles, otherUser.User_id 
                    """
            result = session.run(query, userId=username)

            if not result:
                return ""

            record = result.single()

            title = record["title"]
            sharedBooks = record["sharedBooksTitles"]
            similarUser = record["otherUser.User_id"]

            return title, sharedBooks, similarUser
