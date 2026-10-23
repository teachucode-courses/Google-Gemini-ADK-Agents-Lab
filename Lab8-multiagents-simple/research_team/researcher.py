from google.adk.agents import Agent
from google.adk.tools import google_search

from .config import MODEL


researcher = Agent(
    name="researcher",
    model=MODEL,
    description=(
        "Researches a topic on the web and returns detailed findings "
        "with sources."
    ),
    instruction=(
        "Research the user's topic using google_search. "
        "Return detailed findings as bullet points. "
        "Include the source URLs provided by the search results. "
        "Do not produce the final user-facing summary."
    ),
    tools=[google_search],
    output_key="research_findings",
)