from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search


root_agent = Agent(
    model='gemini-3.5-flash',
    name='root_agent',
    description='An agent that can search the web using Google Search.',
    instruction="""You are a helpful research assistant.
    Use Google Search to find current, accurate information for the user's questions.
    Always cite your sources when possible.
    If you're unsure about something, search for it rather than guessing.""",
    tools=[google_search]
)