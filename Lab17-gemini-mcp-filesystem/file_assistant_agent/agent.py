import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

from dotenv import load_dotenv
load_dotenv()

# --- MCP Tools ---
# Model Context Protocol (MCP) is an open standard for connecting AI agents to external tools.
# ADK's McpToolset connects to an MCP server and automatically discovers its available tools.
# Here, we use the filesystem MCP server to give the agent controlled access to files and directories.
# Define the directory the agent is allowed to access
# _allowed_path = os.path.dirname(os.path.abspath(__file__))

_allowed_path = r"C:\Users\hmira"

root_agent = LlmAgent(
    model="gemini-3.5-flash",
    name="file_assistant",
    description="An agent that can read, explore, and create files and directories using MCP filesystem tools.",
    instruction=f"""You are a helpful file assistant.
    You have access to the filesystem through MCP tools.
    The allowed directory is: {_allowed_path}
    You can read files, list directories, search for files, and create files and directories.
    Always respect the allowed directory boundaries.
    Do not overwrite or modify existing files unless the user explicitly asks you to.
    When showing file contents, format them nicely for the user.""",
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="npx",
                    args=[
                        "-y",
                        "@modelcontextprotocol/server-filesystem",
                        _allowed_path,
                    ],
                ),
                timeout=30,
            ),
            # Only expose read and create operations.
            tool_filter=[
                "read_file",
                "read_multiple_files",
                "list_directory",
                "directory_tree",
                "search_files",
                "get_file_info",
                "list_allowed_directories",
                "write_file",
                "create_directory",
            ],
        )
    ],
)
