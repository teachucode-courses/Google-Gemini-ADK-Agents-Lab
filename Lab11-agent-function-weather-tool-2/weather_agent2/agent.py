from google.adk.agents.llm_agent import Agent

from .get_temperature_unit_conversion import get_temperature_unit_conversion
from .get_weather import get_weather

root_agent = Agent(
    model='gemini-3.5-flash',
    name="weather_agent",
    description="A weather assistant that can check weather and convert temperatures.",
    instruction="""You are a helpful weather assistant.
    When the user asks about a city, follow these steps:
    1. Call 'get_weather' for the city.
    2. Take 'temperature_celsius' from the result and ALWAYS call
       'get_temperature_unit_conversion' with it before replying.
    3. Reply with the conditions and the temperature in Celsius, Fahrenheit and Kelvin.
    Never do the conversion yourself; always use the tool. Keep responses clear and friendly.""",
    tools=[get_weather, get_temperature_unit_conversion],  # Pass functions directly as tools
)
