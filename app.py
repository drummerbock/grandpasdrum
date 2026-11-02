from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify(status="ok", application="grandpasdrum")


@app.get("/")
def index():
    return "Grandpa's Drum is being prepared.", 200
