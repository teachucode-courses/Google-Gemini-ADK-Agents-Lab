# Filesystem MCP Server Tools

This project starts `@modelcontextprotocol/server-filesystem` with `npx -y`.
The inventory below was checked against the published `2.2.0` package on
November 10, 2026. Because the command does not pin a package version, a later
run may use a newer release with a different tool inventory.

## Tools provided by the server

| Tool | Purpose |
| --- | --- |
| `read_file` | Read a file as text. Deprecated; use `read_text_file` instead. |
| `read_text_file` | Read a text file, optionally limiting output to its first or last lines. |
| `read_media_file` | Read a file as base64 with its MIME type, for media and other binary files. |
| `read_multiple_files` | Read several files in one operation. |
| `write_file` | Create a file or overwrite an existing file. |
| `append_file` | Append text to a file, creating it if it does not exist. |
| `edit_file` | Make targeted text edits to a file, with an option to preview changes. |
| `create_directory` | Create a directory and any missing parent directories. |
| `list_directory` | List a directory's entries. |
| `list_directory_with_sizes` | List directory entries with file sizes and summary statistics. |
| `move_file` | Move or rename a file or directory. |
| `copy_file` | Copy a regular file to a new location without overwriting an existing destination. |
| `search_files` | Find files and directories by path/name pattern. |
| `directory_tree` | Return a recursive JSON representation of a directory tree. |
| `get_file_info` | Get metadata for a file or directory. |
| `list_allowed_directories` | Show the directories the server is allowed to access. |

The server checks file operations against the allowed directories passed at
startup.

## Tools enabled in this agent

The `tool_filter` in `file_assistant_agent/agent.py` enables these server tools:

- `read_file` (deprecated)
- `read_multiple_files`
- `list_directory`
- `directory_tree`
- `search_files`
- `get_file_info`
- `list_allowed_directories`
- `write_file`
- `create_directory`

File and directory deletion is not available: the published `2.2.0` server
package does not register `delete_file` or `delete_directory`. Adding tool
names to the agent's filter cannot add capabilities the server does not provide.

## References

- [Filesystem MCP Server README](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)
- [Published npm package](https://www.npmjs.com/package/@modelcontextprotocol/server-filesystem)
