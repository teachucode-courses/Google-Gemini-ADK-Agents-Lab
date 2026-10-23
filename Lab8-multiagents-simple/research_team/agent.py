from google.adk.agents import SequentialAgent

from .researcher import researcher
from .summarizer import summarizer


root_agent = SequentialAgent(
    name="research_and_summary_pipeline",
    description=(
        "Researches the user's topic and then produces "
        "a concise sourced summary."
    ),
    sub_agents=[
        researcher,
        summarizer,
    ],
)