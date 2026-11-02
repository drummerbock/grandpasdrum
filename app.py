from flask import Flask, jsonify, render_template

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify(status="ok", application="grandpasdrum")


@app.get("/")
def index():
    return render_template("index.html")
