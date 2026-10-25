def get_temperature_unit_conversion(celsius: float) -> dict:
    """Converts a temperature from Celsius to Fahrenheit and Kelvin.

    Args:
        celsius: The temperature in Celsius to convert.

    Returns:
        A dictionary with the temperature in Fahrenheit and Kelvin.
    """
    fahrenheit = (celsius * 9 / 5) + 32
    kelvin = celsius + 273.15
    return {
        "celsius": celsius,
        "fahrenheit": round(fahrenheit, 2),
        "kelvin": round(kelvin, 2),
    }
