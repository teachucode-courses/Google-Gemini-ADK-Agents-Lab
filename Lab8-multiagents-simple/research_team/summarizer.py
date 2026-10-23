from google.adk.agents import Agent

from .config import MODEL


summarizer = Agent(
    name="summarizer",
    model=MODEL,
    description=(
        "Summarizes research findings into a concise, "
        "well-structured response."
    ),
    instruction=(
        "Create the final answer using only the research findings below.\n\n"
        "Research findings:\n"
        "{research_findings}\n\n"
        "Format the answer as:\n"
        "1. A concise 2-3 sentence overview\n"
        "2. Three to five key points\n"
        "3. A Sources section containing the source URLs\n\n"
        "Do not add claims that are absent from the research findings."
    ),
)
