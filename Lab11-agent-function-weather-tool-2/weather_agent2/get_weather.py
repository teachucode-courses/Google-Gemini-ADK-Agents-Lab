def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city: The name of the city to get the weather for.

    Returns:
        A dictionary with the weather report and the temperature in Celsius
        (temperature_celsius), which can be passed to
        get_temperature_unit_conversion.
    """
    # Mock weather data (temperatures in Celsius)
    mock_data = {
        "Toronto": {"report": "Sunny. Light breeze from the west.", "temperature_celsius": 22.0},
        "New York": {"report": "Cloudy. Chance of rain in the evening.", "temperature_celsius": 15.0},
        "London": {"report": "Clear skies. Humidity at 45%.", "temperature_celsius": 20.0},
        "Paris": {"report": "Partly cloudy. Pleasant conditions.", "temperature_celsius": 18.0},
        "Sydney": {"report": "Warm. UV index is high.", "temperature_celsius": 28.0},
    }
    key = city.strip().title()
    if key in mock_data:
        return {"status": "success", **mock_data[key]}
    return {
        "status": "error",
        "message": f"Weather data not available for '{city}'. Available cities: {', '.join(mock_data)}.",
    }
