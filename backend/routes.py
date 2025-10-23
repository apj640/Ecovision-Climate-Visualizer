from flask import jsonify, request, Blueprint
from datetime import date
from models import Location, Metric, ClimateData
from const import QUALITY_WEIGHTS
from logic import summarize_climate_data

bp = Blueprint("api", __name__)


def filter_climate_data(location_id, start_date, end_date, metric, quality_threshold):
    """Build ClimateData query from provided filters.

    Note: Multiple filters are combined using AND logic.

    Args:
        location_id (int): The ID of a location to filter by.
        start_date (date): Filter results with date on or after this date.
        end_date (date): Filter results with date on or before this date.
        metric (str): Type of climate data to include in results.
        quality_threshold (str): The minimum quality level to include.

    Returns:
        sqlalchemy.orm.Query: Query with the provided filters.
    """
    query = ClimateData.query
    if location_id:
        query = query.filter(ClimateData.location_id == location_id)
    if start_date:
        query = query.filter(ClimateData.date >= start_date)
    if end_date:
        query = query.filter(ClimateData.date <= end_date)
    if metric:
        query = query.join(Metric).filter(Metric.name == metric)
    if quality_threshold:
        try:
            wanted_qualities = [
                q
                for q, w in QUALITY_WEIGHTS.items()
                if w >= QUALITY_WEIGHTS[quality_threshold]
            ]
        except KeyError:
            raise ValueError("Invalid quality threshold")
        query = query.filter(ClimateData.quality.in_(wanted_qualities))
    return query


@bp.route("/climate", methods=["GET"])
def get_climate_data():
    """
    Retrieve climate data with optional filtering.
    Query parameters: location_id, start_date, end_date, metric, quality_threshold

    Returns climate data in the format specified in the API docs.
    """
    location_id = request.args.get("location_id")
    start_date = request.args.get("start_date", type=date.fromisoformat)
    end_date = request.args.get("end_date", type=date.fromisoformat)
    metric = request.args.get("metric")
    quality_threshold = request.args.get("quality_threshold")
    if quality_threshold and quality_threshold not in QUALITY_WEIGHTS:
        return (
            jsonify(
                {
                    "error": f"Invalid quality_threshold. Must be one of: {QUALITY_WEIGHTS.keys()}"
                }
            ),
            400,
        )
    query = filter_climate_data(
        location_id, start_date, end_date, metric, quality_threshold
    )
    # TODO add pagination if time at end (can use query.paginate())
    results = query.all()
    data = [r.to_dict() for r in results]
    return jsonify(
        {
            "data": data,
            "meta": {"total_count": len(data), "page": 1, "per_page": len(data)},
        }
    )


@bp.route("/locations", methods=["GET"])
def get_locations():
    """
    Retrieve all available locations.

    Returns location data in the format specified in the API docs.
    """
    locations = Location.query.all()
    data = [loc.to_dict() for loc in locations]
    return jsonify({"data": data})


@bp.route("/metrics", methods=["GET"])
def get_metrics():
    """
    Retrieve all available climate metrics.

    Returns metric data in the format specified in the API docs.
    """
    metrics = Metric.query.all()
    data = [m.to_dict() for m in metrics]
    return jsonify({"data": data})


@bp.route("/summary", methods=["GET"])
def get_summary():
    """
    Retrieve quality-weighted summary statistics for climate data.
    Query parameters: location_id, start_date, end_date, metric, quality_threshold

    Returns weighted min, max, and avg values for each metric in the format specified in the API docs.
    """
    location_id = request.args.get("location_id")
    start_date = request.args.get("start_date", type=date.fromisoformat)
    end_date = request.args.get("end_date", type=date.fromisoformat)
    metric = request.args.get("metric")
    quality_threshold = request.args.get("quality_threshold")
    if quality_threshold and quality_threshold not in QUALITY_WEIGHTS:
        return (
            jsonify(
                {
                    "error": f"Invalid quality_threshold. Must be one of: {QUALITY_WEIGHTS.keys()}"
                }
            ),
            400,
        )
    query = filter_climate_data(
        location_id, start_date, end_date, metric, quality_threshold
    )
    climate_data = [data.to_dict() for data in query.all()]
    summary = summarize_climate_data(climate_data)
    return jsonify({"data": summary})


@bp.route("/trends", methods=["GET"])
def get_trends():
    """
    Analyze trends and patterns in climate data.
    Query parameters: location_id, start_date, end_date, metric, quality_threshold

    Returns trend analysis including direction, rate of change, anomalies, and seasonality.
    """
    # TODO: Implement this endpoint
    # 1. Get query parameters from request.args
    # 2. Validate quality_threshold if provided
    # 3. For each metric:
    #    - Calculate trend direction and rate of change
    #    - Identify anomalies (values > 2 standard deviations)
    #    - Detect seasonal patterns if sufficient data
    #    - Calculate confidence scores
    # 4. Format response according to API specification

    return jsonify({"data": {}})
