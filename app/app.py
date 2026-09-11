import os

from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template

from graph.workflow import graph

app = Flask(__name__)


@app.route("/")
def index():

    return render_template("index.html")


@app.route("/health")
def health():

    return {"status": "ok"}


@app.route("/query", methods=["POST"])
def query():

    payload = request.get_json(silent=True) or {}

    question = payload.get("question")

    if not question or not isinstance(question, str):
        return jsonify({"error": "'question' is required and must be a string"}), 400

    try:
        result = graph.invoke({"question": question})
    except Exception:
        app.logger.exception("Failed to answer question")
        return jsonify({"error": "Failed to process the question"}), 500

    return jsonify({"answer": result["answer"], "sources": result["sources"]})


if __name__ == "__main__":

    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"

    app.run(host="0.0.0.0", port=5000, debug=debug)
