from flask import Flask
from flask import request
from flask import jsonify

from graph.workflow import graph

app = Flask(__name__)


@app.route("/health")
def health():

    return {"status": "ok"}


@app.route("/query", methods=["POST"])
def query():

    question = request.json["question"]

    result = graph.invoke({"question": question})

    return jsonify({"answer": result["answer"], "sources": result["sources"]})


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)
