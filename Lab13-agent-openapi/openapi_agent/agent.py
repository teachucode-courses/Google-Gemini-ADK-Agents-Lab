from pathlib import Path

from google.adk.agents.llm_agent import Agent
from google.adk.tools.openapi_tool import OpenAPIToolset

OPENAPI_SPEC_PATH = Path(__file__).with_name("httpbin_openapi.yaml")
OPENAPI_SPEC = OPENAPI_SPEC_PATH.read_text(encoding="utf-8")

httpbin_toolset = OpenAPIToolset(
    spec_str=OPENAPI_SPEC,
    spec_str_type="yaml",
)

root_agent = Agent(
    model="gemini-3.5-flash",
    name="api_agent",
    description="Tests HTTP requests with the public httpbin.org API.",
    instruction="""You are an HTTP API testing assistant with tools for httpbin.org.

Choose the tool that matches the user's request:
- Use test_get_request to send an optional message as a query parameter.
- Use test_post_request to send a JSON body containing the requested name and/or message.
- Use get_ip_address to retrieve the request's origin IP address.
- Use get_user_agent to retrieve the request's User-Agent header.

Ask a brief clarifying question when the requested method or required request data is
unclear. Make the API call before describing its result, and report only information
returned by the tool. Summarize the result clearly without claiming that a request
succeeded if the tool reports an error.""",
    tools=[httpbin_toolset],
)
