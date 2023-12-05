from flask import Flask, request, jsonify, render_template
from models import MongoModel, Neo4jModel, RedisModel

app = Flask(__name__)


@app.route("/")
def index():
    mongoModel = MongoModel()

    # this is horribly inefficent, it finds all book titles
    # then passes it to the page every time
    titles = mongoModel.get_all_titles()
    mongoModel.close()

    return render_template("index.html", book_titles=titles)

@app.route("/book", methods=["GET"])
def get_book():
    mongoModel = MongoModel()

    title = request.args.get('title')

    selected_book = mongoModel.get_book(title)
    mongoModel.close()

    return selected_book

# doesnt work at the moment

# @app.route("/recommendations")
# def recommendations():
#     mongoModel = MongoModel()
#     title = request.args.get("title")
#     recommendations = mongoModel.get_recommendations(title)
#     mongoModel.close()

#     return render_template("recommendations.html", recommendations=jsonify(recommendations).json, title=title)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8888, debug=True)
