# app.py - EcoVision: Climate Visualizer API
# This file contains basic Flask setup code to get you started.
# You may opt to use FastAPI or another framework if you prefer.

from flask import Flask
from flask_cors import CORS
import os
from database import db
import models


def build_conn_str():
    """Build the MySQL connection string from environment variables."""
    host = os.environ.get("PG_HOST", "127.0.0.1")
    user = os.environ.get("PG_USER", "postgres")
    password = os.environ.get("PG_PASSWORD", "postgres")
    db = os.environ.get("DB", "postgres")
    return f"postgresql+psycopg2://{user}:{password}@{host}/{db}"


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.config["SQLALCHEMY_DATABASE_URI"] = build_conn_str()

with app.app_context():
    db.init_app(app)
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
