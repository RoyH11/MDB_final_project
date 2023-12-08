from flask import Flask, request, jsonify, render_template
from models import MongoModel, Neo4jModel

app = Flask(__name__)

mongo = MongoModel()
TITLES = mongo.get_all_titles()
mongo.close()

neo4j = Neo4jModel()
USERNAMES = neo4j.get_all_user_ids()
neo4j.close()


@app.route("/")
def index():
    return render_template("index.html", book_titles=TITLES, user_ids=USERNAMES)

@app.route("/recommendations")
def recommendations():
    mongo_model = MongoModel()
    title = request.args.get("title")
    book = mongo_model.get_book_by_title(title)

    recommendations = mongo_model.get_recommendations(title)
    mongo_model.close()

    return render_template("recommendations.html", recommendations=recommendations, book=book)

@app.route("/login")
def custom_recommendations():
    neo4j_model = Neo4jModel()
    username = request.args.get("username")

    return render_template("customRecommendations.html")

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8888, debug=True)
