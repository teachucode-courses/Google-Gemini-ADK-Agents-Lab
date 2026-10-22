import asyncio
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

from dotenv import load_dotenv
load_dotenv()

import warnings
warnings.filterwarnings("ignore")

# --- Step 1: Define the Agent ---
agent = Agent(
    name="helpful_agent",
    model="openai/gpt-4",
    description="A helpful assistant that answers user questions.",
    instruction="You are a friendly and concise assistant. Answer user questions clearly.",
)

# --- Step 2: Create Session Service and Session ---
session_service = InMemorySessionService()

APP_NAME = "my_app"
USER_ID = "user_1"
SESSION_ID = "session_001"

session = asyncio.run(
    session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
)

# --- Step 3: Create the Runner ---
runner = Runner(
    agent=agent,
    app_name=APP_NAME,
    session_service=session_service,
)


# --- Step 4: Define the interaction function ---
def call_agent(query: str):
    """Send a message to the agent and print the final response."""
    print(f"\n>>> User: {query}")

    # Wrap the user query as a Content object
    message = types.Content(role="user", parts=[types.Part(text=query)])

    # Run the agent loop — iterate over events until we get the final response
    final_response = "No response received."
    for event in runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=message):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text

    print(f"<<< Agent: {final_response}")


# --- Step 5: Run a multi-turn conversation ---
if __name__ == "__main__":
    call_agent("What are the main components of agentic AI?")
    call_agent("What is its significance?")
    call_agent("Summarize the conversation so far in one paragraph.")