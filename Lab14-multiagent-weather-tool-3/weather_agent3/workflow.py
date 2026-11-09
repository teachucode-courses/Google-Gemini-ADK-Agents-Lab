"""A function tool coordinates three AgentTools, without adding a fifth agent."""

import json
import logging
import math
from datetime import datetime, timezone

from google.adk.tools import ToolContext
from google.adk.tools.agent_tool import AgentTool
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from .advisor import advisor_agent
from .converter import converter_agent
from .researcher import research_agent


class WeatherRecord(BaseModel):
    model_config = ConfigDict(extra="allow", allow_inf_nan=False)

    city: str
    temperature_celsius: float | None = Field(ge=-273.15)
    humidity: float | None = Field(ge=0, le=100)
    condition: str | None
    normalized_condition: str
    observed_at: str | None
    sources: list[str]
    notes: list[str]


research_tool = AgentTool(agent=research_agent, propagate_grounding_metadata=True)
converter_tool = AgentTool(agent=converter_agent)
advisor_tool = AgentTool(agent=advisor_agent)


def _record(result: str | dict) -> dict:
    if isinstance(result, str):
        text = result.strip()
        if text.startswith("```") and text.endswith("```"):
            text = "\n".join(text.splitlines()[1:-1])
        result = json.loads(text)
    return WeatherRecord.model_validate(result).model_dump()


async def run_weather_pipeline(city: str, tool_context: ToolContext) -> dict:
    """Research a city's current weather, convert temperatures, and find mock advice.

    Args:
        city: The city and, where known, state/region and country.
        tool_context: ADK-provided context for the internal agent calls.
    """
    if not city.strip():
        return {"status": "error", "message": "A city is required."}
    stage = "research"
    weather = None
    try:
        result = await research_tool.run_async(
            args={"request": json.dumps({"city": city, "current_time_utc":
                                         datetime.now(timezone.utc).isoformat()})},
            tool_context=tool_context,
        )
        weather = _record(result)
        if (any(weather[key] is None for key in
                ("temperature_celsius", "humidity", "condition")) or not weather["sources"]):
            return {"status": "incomplete", "stage": stage, "weather": weather,
                    "message": "Research did not find all required weather values and sources."}
        stage = "conversion"
        converted = _record(await converter_tool.run_async(
            args={"request": json.dumps(weather)}, tool_context=tool_context))
        if any(converted.get(key) is None for key in
               ("temperature_fahrenheit", "temperature_kelvin")):
            return {"status": "incomplete", "stage": stage, "weather": weather,
                    "message": "Converter did not return both converted temperatures."}
        for key in ("temperature_fahrenheit", "temperature_kelvin"):
            if (isinstance(converted[key], bool)
                    or not isinstance(converted[key], (int, float))
                    or not math.isfinite(converted[key])):
                raise ValueError("Invalid converted temperature")
        # Preserve source observations even if an agent accidentally rewrites them.
        converted.update(weather)
        weather = converted
        stage = "advice"
        advised = _record(await advisor_tool.run_async(
            args={"request": json.dumps(converted)}, tool_context=tool_context))
        if not isinstance(advised.get("advice"), dict):
            return {"status": "incomplete", "stage": stage, "weather": weather,
                    "message": "Advisor did not return an advice result."}
        advised.update(converted)
        return {"status": "success", "weather": advised}
    except (ValueError, TypeError, ValidationError):
        return {"status": "error", "stage": stage, "weather": weather,
                "message": "The agent returned malformed weather data. Please retry."}
    except Exception:
        logging.getLogger(__name__).exception("Weather pipeline failed during %s", stage)
        return {"status": "error", "stage": stage, "weather": weather,
                "message": "The agent service failed. Check the server log and API/model configuration."}
