from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search
from google.adk.code_executors import BuiltInCodeExecutor

# Uses Gemini's built-in Python execution capability: the model can run code
# for computations and use the execution results when forming its response.
# BuiltInCodeExecutor() enables Gemini’s built-in Python execution capability. 
# When a task needs computation—such as solving math or analyzing data—the model can write and run Python, 
# then use the result in its response. 
# It’s separate from google_search, which lets the agent look up factual information.

root_agent = Agent(
    model='gemini-3.5-flash',
    name='code_exec_agent',
    description="An agent that can write and execute Python code.",
    instruction="""You are a helpful assistant that can write and execute Python code.
    When given a mathematical problem, data analysis task, or any computation,
    write Python code to solve it.
    Return the result clearly to the user.
    You can also use Google Search for factual information.""",
    tools=[google_search],
    code_executor=BuiltInCodeExecutor(),
)
