from app import app

from flask import jsonify
from datetime import datetime

@app.route("/healthcheck")
def healthcheck():
    return jsonify(datetime.today(), "Service status: OK"), 200
