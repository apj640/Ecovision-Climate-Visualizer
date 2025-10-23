import pandas as pd
import numpy as np
from typing import List
from const import QUALITY_WEIGHTS


def summarize_climate_data(climate_data: List[dict]):
    """Return summary statistics per metric.

    Args:
        climate_data: list of climate data measurements (see models.ClimateData.to_dict)

    Returns:
      dict: keyed by metric name with min/max/avg/weighted_avg/unit and quality distribution.
    """
    if not climate_data:
        return {}

    df = pd.DataFrame(climate_data)
    result = {}
    for metric, group in df.groupby("metric"):
        vals = group["value"].astype(float)
        # Get unit from first row in metric group
        unit = group["unit"].iloc[0]

        # simple stats, round to 1 to match expected response from api.md
        summary = {
            "min": round(float(vals.min()), 1),
            "max": round(float(vals.max()), 1),
            "avg": round(float(vals.mean()), 1),
            "unit": unit,
        }

        # weighted avg using QUALITY_WEIGHTS
        weights = group["quality"].map(QUALITY_WEIGHTS).astype(float)
        summary["weighted_average"] = np.average(vals, weights=weights).round(1)

        # quality distribution
        dist = group["quality"].value_counts(normalize=True).round(1).to_dict()
        for quality in QUALITY_WEIGHTS.keys():
            if quality not in dist:
                dist[quality] = 0.0
        summary["quality_distribution"] = dist

        result[metric] = summary
    return result
