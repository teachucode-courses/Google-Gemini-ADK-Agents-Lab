import warnings
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

# 1. Load the OPENAI_API_KEY from your .env file
load_dotenv()
warnings.filterwarnings("ignore")

# 2. Define the OpenAI Model via LiteLLM
openai_llm = LiteLlm(model="openai/gpt-4") 

# 3. Define the Agent as 'root_agent' so the CLI can find it
root_agent = Agent(
    name="helpful_agent",
    model=openai_llm,
    description="A helpful assistant that answers user questions.",
    instruction="You are a friendly and concise assistant. Answer user questions clearly.",
)