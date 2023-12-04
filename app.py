from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route("/")
def index():
    # TODO populate with all titles
    titles = []
    return render_template("index.html", book_titles=jsonify(titles).json)

@app.route("/recommendations", methods=["GET"])
def recommendations():
    title = request.args.get("title")
    # TODO get recommendations based off description and reviews
    recommendations = []
    return render_template("recommendations.html", recommendations=jsonify(recommendations).json)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8888, debug=True)
