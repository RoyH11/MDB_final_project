from flask import Flask, request, jsonify, render_template
from models import MongoModel, Neo4jModel

app = Flask(__name__)
mongo = MongoModel()
TITLES = mongo.get_all_titles()
mongo.close()

@app.route("/")
def index():
    return render_template("index.html", book_titles=TITLES)

@app.route("/recommendations")
def recommendations():
    mongoModel = MongoModel()
    title = request.args.get("title")
    book = mongoModel.get_book_by_title(title)

    recommendations = mongoModel.get_recommendations(title)
    mongoModel.close()

    return render_template("recommendations.html", recommendations=jsonify(recommendations).json, book=book)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8888, debug=True)
