### MCP Server (AI Integration)
You can expose your Zettelkasten to AI assistants (like Claude Desktop or Cursor) using the Model Context Protocol (MCP).

**Configuration for Cursor:**
1. Go to **Cursor Settings** > **Features** > **MCP Servers**.
2. Click **+ Add new MCP server**.
3. Enter the following details:
   - **Name**: `zk-smart-search`
   - **Type**: `stdio`
   - **Command**: `/YOUR/ABSOLUTE/PATH/TO/zk-smart-search/venv/bin/python`
   - **Args**: `/YOUR/ABSOLUTE/PATH/TO/zk-smart-search/mcp_server.py`

**Configuration for Claude Desktop:**
Add this to your `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "zk-smart-search": {
      "command": "/YOUR/ABSOLUTE/PATH/TO/zk-smart-search/venv/bin/python",
      "args": ["/YOUR/ABSOLUTE/PATH/TO/zk-smart-search/mcp_server.py"]
    }
  }
}
```

Replace `/YOUR/ABSOLUTE/PATH/TO` with the actual path to your cloned repository.

**Available Tools:**
- `search_notes(query, semantic=False)`: Search for notes using keywords or semantic search.
- `read_note(filename)`: Read the full content of a note.
