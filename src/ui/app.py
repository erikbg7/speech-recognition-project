from core import process_request
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/process-data", methods=["POST"])
def process_data():
    text = request.data.decode("utf-8")
    results = process_request(text)
    return results[0].toJSON() if len(results) > 0 else {}
