"""Match observed weather to the supplied synthetic advice records."""

import json
import math
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "mock_weather_advisory_with_advice.json"


def get_weather_advice(celsius: float, humidity: float, condition: str) -> dict:
    """Read mock advice and select a condition/range match nearest in humidity.

    Args:
        celsius: Observed temperature in Celsius.
        humidity: Observed relative humidity percentage (0 to 100).
        condition: sunny, rain, snow, fog, thunderstorm, or an unsupported condition.
    """
    if (not math.isfinite(celsius) or celsius < -273.15
            or not math.isfinite(humidity) or not 0 <= humidity <= 100):
        return {"status": "error", "message": "Invalid temperature or humidity."}
    normalized = condition.strip().lower()
    normalized = {"clear": "sunny", "drizzle": "rain", "mist": "fog"}.get(
        normalized, normalized
    )
    try:
        data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
        # Half-open ranges avoid overlapping endpoints; include the dataset's 40 C cap.
        candidates = [record for record in data["records"]
                      if record["condition"] == normalized
                      and record["temperature"]["min_c"] <= celsius
                      and (celsius < record["temperature"]["max_c"]
                           or celsius == record["temperature"]["max_c"] == 40)]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return {"status": "error", "message": f"Cannot read mock advice: {type(exc).__name__}"}
    if not candidates:
        return {"status": "no_match", "synthetic": True,
                "message": "No matching advice in the mock dataset for this condition and temperature."}
    match = min(candidates, key=lambda record: abs(record["humidity"] - humidity))
    return {
        "status": "success",
        "synthetic": True,
        "advisory": match["advisory"],
        "matched_record": match,
        "humidity_difference": abs(match["humidity"] - humidity),
        "match_method": "Condition and temperature range, then nearest humidity; season is not inferred.",
    }
