from database import db


class Location(db.Model):
    __tablename__ = "location"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    region = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "region": self.region,
            "country": self.country,
        }


class Metric(db.Model):
    __tablename__ = "metric"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "display_name": self.display_name,
            "unit": self.unit,
            "description": self.description,
        }


class ClimateData(db.Model):
    __tablename__ = "climate_data"
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"), nullable=False)
    metric_id = db.Column(db.Integer, db.ForeignKey("metric.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    value = db.Column(db.Float, nullable=False)
    quality = db.Column(db.String(50), nullable=False)

    location = db.relationship(
        "Location", backref=db.backref("climate_data", lazy=True)
    )
    metric = db.relationship("Metric", backref=db.backref("climate_data", lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "location_id": self.location_id,
            "location_name": self.location.name,
            "date": self.date.isoformat(),
            "metric": self.metric.name,
            "value": self.value,
            "unit": self.metric.unit,
            "quality": self.quality,
        }
