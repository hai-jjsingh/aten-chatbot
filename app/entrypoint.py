import os

from ingestion.bootstrap import bootstrap
from app.app import app

if __name__ == "__main__":

    bootstrap()

    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"

    app.run(host="0.0.0.0", port=5000, debug=debug)
