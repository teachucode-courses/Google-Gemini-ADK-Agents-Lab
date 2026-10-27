from pathlib import Path

from google.adk.agents.llm_agent import Agent
from google.adk.tools.openapi_tool import OpenAPIToolset

openapi_spec_path = Path(__file__).resolve().parent.parent / 'httpbin_openapi.yaml'
openapi_spec_string = openapi_spec_path.read_text(encoding='utf-8')

# --- Create OpenAPIToolset ---
httpbin_toolset = OpenAPIToolset(
    spec_str=openapi_spec_string,
    spec_str_type='yaml',
    # No authentication needed for httpbin.org
)

root_agent = Agent(
    model='gemini-3.5-flash',
    name='api_agent',
    description="An agent that interacts with REST APIs using OpenAPI-generated tools.",
    instruction="""You are an API testing assistant.
    You have access to tools generated from an OpenAPI specification for httpbin.org.
    Use the available tools to fulfill user requests:
    - test_get_request: Send a GET request with query parameters
    - test_post_request: Send a POST request with JSON body
    - get_ip_address: Get the origin IP address
    - get_user_agent: Get the User-Agent string
    When making requests, clearly explain what you're doing and show the results.""",
    tools=[httpbin_toolset],
)
