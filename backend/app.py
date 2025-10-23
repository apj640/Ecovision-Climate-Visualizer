# app.py - EcoVision: Climate Visualizer API
# This file contains basic Flask setup code to get you started.
# You may opt to use FastAPI or another framework if you prefer.

from flask import Flask
from flask_cors import CORS
import click
import os
from database import db
import models
from routes import bp


def build_conn_str():
    """Build the Postgres connection string from environment variables."""
    host = os.environ.get("PG_HOST", "127.0.0.1")
    user = os.environ.get("PG_USER", "postgres")
    password = os.environ.get("PG_PASSWORD", "postgres")
    db = os.environ.get("DB", "postgres")
    return f"postgresql+psycopg2://{user}:{password}@{host}/{db}"


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.register_blueprint(bp, url_prefix="/api/v1")
app.config["SQLALCHEMY_DATABASE_URI"] = build_conn_str()

with app.app_context():
    db.init_app(app)
    db.create_all()


@click.option(
    "--clear",
    is_flag=True,
    default=False,
    help="Clear existing data before populating.",
)
@app.cli.command("seed")
def seed_command(clear):
    """Populate the database with initial data."""
    from seed import populate_db

    populate_db(app, clear)


@app.cli.command("dropdb")
def drop_db_command():
    """Drop all tables in the database."""
    print("Clearing existing data...")
    db.drop_all()


if __name__ == "__main__":
    app.run(debug=True)
