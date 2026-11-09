# Student Challenge: Build a Multi-Agent Weather Assistant

## Your task

Build a weather assistant using the **Google ADK framework**. Your system must use **four agents** that work together to research weather, convert temperatures, and provide advice.

Use **Lab11-agent-function-weather-tool-2** as your starting reference. Build your own implementation and be prepared to explain your design decisions.

> **Getting started:** Think of this application as a team of four people. Each person has one job, and the team shares its findings. Your job is to define those roles and make sure the right information reaches the next person.

## Learning objectives

By completing this challenge, you should be able to:

- Divide a task among agents with clear responsibilities.
- Write agent instructions and register tools.
- Use ADK Google Search to find current information.
- Create a Python function that an agent can call.
- Pass information between agents without losing details.
- Read a JSON dataset and select relevant advice.
- Handle missing information without inventing answers.
- Test individual tools and the complete multi-agent workflow.

## Required agents

| Agent | Responsibility | Required tool or data |
| --- | --- | --- |
| **1. Orchestrator** | Receives the user's request, coordinates the work, and writes the final response. Only this agent communicates with the user. | Your workflow coordination |
| **2. Research agent** | Searches for the city's current temperature in Celsius, relative humidity, and weather conditions. | ADK Google Search |
| **3. Converter agent** | Converts Celsius to Fahrenheit and Kelvin while preserving the researched information. | A Python function in a separate file |
| **4. Advisor agent** | Selects suitable advice based on the weather information. | Instructor-provided `mock_weather_advisory_with_advice.json` |

## Required workflow

```text
User asks about a city
        |
        v
Orchestrator assigns the research
        |
        v
Research agent finds current weather
        |
        v
Converter agent adds Fahrenheit and Kelvin
        |
        v
Advisor agent selects advice from the mock data
        |
        v
Orchestrator prepares the final response
        |
        v
User receives the result
```

Each handoff must preserve the information gathered by the previous agents. You may choose your coordination approach, but you must explain how it preserves the required order and keeps the orchestrator as the only user-facing agent.

> **What is a handoff?** A handoff means passing one agent's result to the next agent. For example, the converter needs the Celsius value, but it must also pass along the city, humidity, conditions, and sources. Otherwise, the advisor or orchestrator will lose information it needs.

## Provided dataset: everyone uses the same data

Your instructor will supply **`mock_weather_advisory_with_advice.json`**. Everyone must use this exact file without modifying its records, replacing it with another dataset, or adding advice.

The advisor must select advice from this dataset based on the researched temperature, humidity, and weather conditions. If no suitable record exists, report that no matching advice is available. Do not invent replacement advice.

The dataset supplies **mock advice only**. Current city weather must still come from Google Search. Do not present the dataset's example humidity, temperature ranges, or season labels as current weather observations.

In your README, explain your matching rules so your results can be compared consistently with other submissions.

> **What does mock mean?** Mock data is example data supplied for practice. A record describing rain does not prove it is raining in the user's city. First find the actual weather, then use the file to look for advice that fits it.

## Build requirements

### 1. Collect the city

The orchestrator must identify the city requested by the user. Ask for clarification when the city is missing or ambiguous.

> **Think about the user:** A name such as Springfield can refer to several places. Asking for the state or country can prevent the whole team from researching the wrong location.

### 2. Research current weather

The research agent must use ADK Google Search to find:

- Temperature in Celsius (centigrade).
- Relative humidity as a percentage.
- Current weather conditions.
- Source links and the observation time, when available.

Use current observations where available. Do not silently substitute a forecast, daily high, or feels-like temperature. Clearly identify missing information instead of guessing.

> **Check the meaning of each value:** An observation reports measured weather at a particular time. A forecast predicts future weather. Keep the source and time with the readings so the final answer can explain where the information came from.

### 3. Convert temperatures using a tool

Create a separate Python function file that converts Celsius to Fahrenheit and Kelvin. Register the function as a tool for the converter agent.

The converter agent must call this function instead of performing the calculation itself. Return both converted values and preserve the original weather information.

```text
Fahrenheit = Celsius * 9 / 5 + 32
Kelvin = Celsius + 273.15
```

Document your rounding approach and how your function handles invalid input.

> **Agent versus tool:** The converter agent decides to request a conversion. The Python function performs the arithmetic and returns the numbers. Check the function with a known input, such as 0 Celsius, before connecting it to the agent.

### 4. Select advice from the supplied JSON file

The advisor must read the instructor's dataset, directly or through a tool, and select suitable advice using the information received from the converter.

Define and document:

- How weather descriptions are matched to the dataset's condition labels.
- How temperature ranges are matched, including shared boundaries.
- How humidity affects selection when it differs from the example values.
- How ties between suitable records are resolved.
- Whether season affects matching and, if so, how it is determined.
- What happens when no suitable record exists or the file cannot be read.

You may normalize incoming weather descriptions, but you must not modify the supplied dataset. Do not force an unsupported condition into an unrelated category just to obtain advice.

> **What does normalize mean?** It means using consistent labels for equivalent descriptions. For example, you might decide that "clear skies" matches "sunny." Explain your choices; a different condition such as "cloudy" should not automatically become "sunny."

> **Watch the boundaries:** If one temperature range ends at 10 Celsius and another begins at 10 Celsius, decide which range owns that exact value. Also decide what to do when more than one record matches. Your rules should give a predictable result.

### 5. Produce one complete response

The advisor must return its results and the weather information to the orchestrator. The orchestrator then drafts the final response containing:

- City and country, when known.
- Temperature in Celsius, Fahrenheit, and Kelvin.
- Relative humidity and weather conditions.
- Observation time and source links, when available.
- Advice clearly labeled as coming from a **synthetic mock dataset**.
- Any missing information, failures, or limitations.

Only the orchestrator may ask the user questions or deliver the final answer.

> **Check completeness:** Imagine reading only the final response. Could you identify the city, understand the weather, find the sources, and tell which advice came from the practice dataset? Internal agent messages should not be needed to understand it.

## Suggested starting steps

1. Draw your agent workflow before coding.
2. Define the information each agent receives and returns.
3. Inspect the supplied JSON file and decide on your matching rules.
4. Build and check the temperature conversion function independently.
5. Configure each agent's responsibility, instructions, and tools.
6. Connect the agents in the required order.
7. Test the complete workflow and document the results.

> **Build one piece at a time:** Start with a small working part, check its output, and then connect the next part. If the final answer is wrong, inspect the information passed at each step to find where the problem first appears.

## Test your solution

Demonstrate these scenarios:

| Scenario | What to check |
| --- | --- |
| A clearly identified city | The system retrieves weather and returns all available required fields. |
| A missing or ambiguous location | The orchestrator requests clarification. |
| A second city in the same conversation | The system performs fresh research and does not reuse the first city's readings. |
| Weather with a matching advisory record | Advice comes from the supplied dataset and follows your documented rules. |
| Weather without a matching advisory record | The system reports no matching advice without inventing a replacement. |
| Missing research data | The system identifies missing values and avoids unsupported calculations or advice. |
| A failed tool call | The system explains the failure without claiming the workflow succeeded. |

Use controlled sample inputs to test conversion and advice matching independently of live weather. Include a temperature at a range boundary and a humidity value that differs from the dataset's reference values.

For conversion, useful checks include:

| Celsius | Expected Fahrenheit | Expected Kelvin |
| --- | --- | --- |
| 0 | 32 | 273.15 |
| 25 | 77 | 298.15 |
| -40 | -40 | 233.15 |

Distinguish tests using sample or mocked inputs from tests that actually call Gemini and Google Search.

> **Why use sample inputs?** Live weather changes, so it cannot reliably produce every situation you need to test. A fixed sample lets you check a boundary or missing value whenever you want. Label samples clearly and never present them as live observations.

## Example user prompts

- `What is the weather in London, UK, right now? Include clothing advice.`
- `Check Toronto, Canada. Show Celsius, Fahrenheit, Kelvin, and humidity.`
- `Now check Sydney, Australia.`
- `What is the weather like?`

Actual weather readings will vary. Assessment focuses on correct tool use, information flow, matching rules, and honest handling of missing data.

## What to submit

- Your complete Google ADK application containing the four agents.
- The separate Python temperature conversion function.
- The unchanged instructor-provided advisory dataset.
- A `requirements.txt` listing the required dependencies.
- An `.env.example` containing configuration placeholders without API keys or other credentials.
- A README explaining setup, how to run the application, agent responsibilities, data flow, and advice matching rules.
- Evidence of your tests, including example outputs and any known limitations.

Do not submit your private `.env`, credentials, or virtual environment folder.

> **Write for a classmate:** Your README should help another student install and run the project without asking you for missing steps. An `.env.example` shows the setting names and safe placeholders; your private `.env` contains your own configuration.

## Assessment rubric

| Area | Weight |
| --- | --- |
| Four agents with clear responsibilities | 20% |
| Correct workflow and complete data handoffs | 25% |
| Google Search and Python conversion tool usage | 20% |
| Advice matching and missing-data handling | 20% |
| Testing, documentation, and code clarity | 15% |
| **Total** | **100%** |

## Final checklist

- [ ] I built four agents with the required responsibilities.
- [ ] Only the orchestrator communicates with the user.
- [ ] The research agent uses ADK Google Search.
- [ ] The converter agent calls a Python function in a separate file.
- [ ] Each handoff preserves the weather information and sources.
- [ ] The advisor uses the instructor's unchanged JSON dataset.
- [ ] My matching rules and boundary behavior are documented.
- [ ] Unsupported conditions and missing data do not produce invented answers.
- [ ] The final response includes all available required information and labels mock advice.
- [ ] I tested the required scenarios and documented the results.
- [ ] My submission includes setup instructions and contains no credentials.
