import json
import sys
import datetime
from pathlib import Path
from database import db
from models import Location, Metric, ClimateData


file_path = Path(__file__).parents[1].resolve() / "data" / "sample_data_clean.json"


def populate_db(app, clear=False):
    if not file_path.exists():
        print("No sample data file found at", file_path)
        sys.exit(1)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(
            f"Failed to parse {file_path.resolve()}. Ensure the file contains valid JSON."
        )
        print(e)
        sys.exit(1)

    with app.app_context():
        if clear:
            print("Clearing existing data...")
            db.drop_all()

        # Create tables if they don't exist
        db.create_all()
        if ClimateData.query.first() or Metric.query.first() or Location.query.first():
            print(
                "Data already exists in the database. Use --clear to delete existing data before inserting."
            )
            sys.exit(1)

        print("Populating DB with initial data...")

        # Insert locations
        locs = data.get("locations", [])
        for l in locs:
            loc = Location()
            loc.id = l["id"]
            loc.name = l["name"]
            loc.latitude = l.get("latitude", 0.0)
            loc.longitude = l.get("longitude", 0.0)
            loc.region = l.get("region", "")
            loc.country = l.get("country", "")
            db.session.merge(loc)  # merge to allow id-preserving upserts

        # Insert metrics
        metrics = data.get("metrics", [])
        for m in metrics:
            metric = Metric()
            metric.id = m["id"]
            metric.name = m["name"]
            metric.display_name = m.get("display_name")
            metric.unit = m.get("unit")
            metric.description = m.get("description")
            db.session.merge(metric)

        # Insert climate data
        rows = data.get("climate_data", [])
        for r in rows:
            cd = ClimateData()
            cd.id = r["id"]
            cd.location_id = r["location_id"]
            cd.metric_id = r["metric_id"]
            # parse date string into a date object
            try:
                cd.date = datetime.date.fromisoformat(r["date"])
            except Exception:
                cd.date = r["date"]
            cd.value = r["value"]
            cd.quality = r["quality"]
            db.session.merge(cd)

        db.session.commit()
        print(
            f"Inserted {len(locs)} locations, {len(metrics)} metrics, {len(rows)} climate_data rows"
        )
