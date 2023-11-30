from flask import Flask, request, jsonify, render_template
from models.MongoClient import MongoClient
from models.RedisClient import RedisClient
from models.Neo4jClient import Neo4jClient

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8888, debug=True)
