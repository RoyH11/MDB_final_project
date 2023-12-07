from models import Neo4jModel
import csv


CREATE_USER_QUERY = "MERGE (u:User {User_id: $userId})"
CREATE_BOOK_QUERY = "MERGE (b:Book {Title: $title})"

CREATE_RATED_RELATIONSHIP_QUERY = """
MATCH (u:User {id: $userId}), (b:Book {id: $bookId})
MERGE (u)-[:RATED {score: $score, time: $time, summary: $summary, text: $text, helpfulness: $helpfulness}]->(b)
"""

CREATE_RATED_RELATIONSHIP_QUERY = """
                                  MATCH (u:User {User_id: $userId}), (b:Book {Title: $title}) 
                                  MERGE (u)-[:RATED {score: $score, helpfulness: $helpfulness}]->(b)
                                  """

def create_relationship(tx, row):
    # User node
    tx.run(CREATE_USER_QUERY, userId=row.get("User_id"))

    # Book node
    tx.run(CREATE_BOOK_QUERY, title=row.get("Title"))

    # RATED relationship
    tx.run(
        CREATE_RATED_RELATIONSHIP_QUERY,
        userId=row['User_id'],
        score=row['review/score'],
        helpfulness=row['review/helpfulness'],
        title=row['Title']
    )

def create_indexes(model):
    with model.driver.session() as session:
        session.run("CREATE INDEX FOR (u:User) ON (u.User_id)")
        session.run("CREATE INDEX FOR (b:Book) ON (b.Title)")

def import_data(path):
    model = Neo4jModel()

    create_indexes(model)

    with model.driver.session() as session:
        # Read the CSV file and execute the queries
        with open(path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            total_records = sum(1 for _ in reader)
            csvfile.seek(0) 

            for i, row in enumerate(reader, start=1):
                if i == 1:
                    continue
                if row.get("User_id"):
                    session.write_transaction(create_relationship, row)

                progress_percentage = (i / total_records) * 100
                print(f"Progress: {i-1}/{total_records} records processed ({progress_percentage:.2f}%)", end="\r")

    model.close()
    print(f"\nratings successfully imported.\n")

if __name__ == "__main__":
    import_data("data/Books_rating_small.csv")
