import math


def get_temperature_unit_conversion(celsius: float) -> dict:
    """Convert Celsius to Fahrenheit and Kelvin using Python arithmetic.

    Args:
        celsius: A finite temperature in Celsius, at or above absolute zero.
    """
    if not math.isfinite(celsius) or celsius < -273.15:
        return {"status": "error", "message": "Invalid Celsius temperature."}
    return {
        "status": "success",
        "celsius": celsius,
        "fahrenheit": round(celsius * 9 / 5 + 32, 2),
        "kelvin": round(celsius + 273.15, 2),
    }
