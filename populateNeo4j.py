from models import Neo4jModel

create_index_user = """
CREATE INDEX FOR (u:User) ON (u.User_id)
"""
create_index_book = """
CREATE INDEX FOR (b:Book) ON (b.Title) 
"""

cypher_load_csv = """
LOAD CSV WITH HEADERS FROM $csvFile AS row 
CALL {
    WITH row 
    MERGE (user:User {User_id: row.User_id}) 
    MERGE (book:Book {Title: row.Title}) 
    CREATE (user)-[:RATED {score: toFloat(row.score)}]->(book) 
} IN TRANSACTIONS
"""

def import_data(path):
    model = Neo4jModel()

    with model.driver.session() as session:
        # uncomment if you need indexes
        session.run(create_index_user)
        session.run(create_index_book)

        session.run(cypher_load_csv, {"csvFile": "file:///" + path})
        
    model.close()
    print(f"\nratings successfully imported.\n")

if __name__ == "__main__":
    import_data("Books_rating_refactored.csv")
