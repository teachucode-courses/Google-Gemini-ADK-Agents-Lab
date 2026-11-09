import json
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from weather_agent3 import workflow
from weather_agent3.agent import root_agent
from weather_agent3.get_temperature_unit_conversion import get_temperature_unit_conversion
from weather_agent3.get_weather_advice import get_weather_advice


class ToolTests(unittest.TestCase):
    def test_conversion(self):
        for celsius, fahrenheit, kelvin in [(0, 32, 273.15), (-40, -40, 233.15), (25, 77, 298.15)]:
            result = get_temperature_unit_conversion(celsius)
            self.assertEqual(result["fahrenheit"], fahrenheit)
            self.assertEqual(result["kelvin"], kelvin)

    def test_invalid_values(self):
        for value in [float("nan"), float("inf"), -274]:
            self.assertEqual(get_temperature_unit_conversion(value)["status"], "error")
        self.assertEqual(get_weather_advice(20, 101, "rain")["status"], "error")

    def test_advice_and_boundaries(self):
        result = get_weather_advice(25, 82, "rain")
        self.assertEqual(result["advisory"], "Warm and wet. Use light rain protection and breathable clothing.")
        self.assertEqual(result["humidity_difference"], 3)
        for celsius, band in [(0, "cold"), (10, "mild"), (20, "warm"), (30, "hot"), (40, "hot")]:
            self.assertEqual(get_weather_advice(celsius, 45, "sunny")["matched_record"]["temperature"]["range"], band)

    def test_no_invented_advice(self):
        for celsius, condition in [(20, "cloudy"), (41, "sunny"), (-21, "snow")]:
            self.assertEqual(get_weather_advice(celsius, 50, condition)["status"], "no_match")


class WorkflowTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.weather = {"city": "Example City", "temperature_celsius": 25,
                        "humidity": 82, "condition": "light rain", "normalized_condition": "rain",
                        "observed_at": "2026-10-28T12:00:00Z",
                        "sources": ["https://example.com/weather"], "notes": []}

    async def test_order_and_complete_handoff(self):
        calls = []

        async def research(**kwargs):
            calls.append("research")
            self.assertEqual(json.loads(kwargs["args"]["request"])["city"], "Example City")
            return json.dumps(self.weather)

        async def convert(**kwargs):
            calls.append("conversion")
            incoming = json.loads(kwargs["args"]["request"])
            self.assertEqual(incoming, self.weather)
            return json.dumps({**incoming, "temperature_fahrenheit": 77, "temperature_kelvin": 298.15})

        async def advise(**kwargs):
            calls.append("advice")
            incoming = json.loads(kwargs["args"]["request"])
            self.assertEqual(incoming["temperature_kelvin"], 298.15)
            self.assertEqual(incoming["sources"], self.weather["sources"])
            return json.dumps({**incoming, "advice": get_weather_advice(25, 82, "rain")})

        with patch.multiple(workflow,
                            research_tool=SimpleNamespace(run_async=research),
                            converter_tool=SimpleNamespace(run_async=convert),
                            advisor_tool=SimpleNamespace(run_async=advise)):
            result = await workflow.run_weather_pipeline("Example City", None)
        self.assertEqual(calls, ["research", "conversion", "advice"])
        self.assertEqual(result["status"], "success")
        self.assertTrue(result["weather"]["advice"]["synthetic"])
        self.assertEqual(root_agent.name, "weather_orchestrator")
        self.assertFalse(root_agent.sub_agents)

    async def test_missing_humidity_stops_pipeline(self):
        self.weather["humidity"] = None
        research = SimpleNamespace(run_async=AsyncMock(return_value=json.dumps(self.weather)))
        converter = SimpleNamespace(run_async=AsyncMock())
        with patch.multiple(workflow, research_tool=research, converter_tool=converter):
            result = await workflow.run_weather_pipeline("Example City", None)
        self.assertEqual(result["status"], "incomplete")
        converter.run_async.assert_not_called()

    async def test_malformed_research(self):
        research = SimpleNamespace(run_async=AsyncMock(return_value="not JSON"))
        with patch.object(workflow, "research_tool", research):
            result = await workflow.run_weather_pipeline("Example City", None)
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["stage"], "research")


if __name__ == "__main__":
    unittest.main()
