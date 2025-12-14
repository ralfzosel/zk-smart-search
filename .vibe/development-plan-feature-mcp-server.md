# Development Plan: zk-smart-search (feature/mcp-server branch)

*Generated on 2025-12-14 by Vibe Feature MCP*
*Workflow: [epcc](https://mrsimpson.github.io/responsible-vibe-mcp/workflows/epcc)*

## Goal
Create a Model Context Protocol (MCP) server that exposes the Zettelkasten search functionality (both keyword and semantic) to AI assistants like Claude Desktop and Cursor.

## Explore
### Tasks
- [x] Research `mcp` Python SDK usage and requirements.
- [x] Analyze reference implementation (`mcp_email/main.py`).
- [x] Determine the tools to expose (`search_notes`, `read_note`).
- [x] Decide on transport mechanism: `stdio` (matching reference).

### Completed
- [x] Created development plan file

## Plan
### Phase Entrance Criteria
- [x] MCP SDK dependencies identified (`mcp`).
- [x] List of tools and their schemas defined.
- [x] Integration strategy with `zkss` code defined (separate `mcp_server.py`).

### Tasks
- [x] Design `mcp_server.py` structure (based on `mcp_email`).
- [x] Define the `search_notes` tool schema.
- [x] Define the `read_note` tool schema.
- [x] Define Console handling strategy: Mock/Silence `rich.console`.

### Completed
*None yet*

## Code
### Phase Entrance Criteria
- [x] Tool schemas are finalized.
- [x] Server architecture is documented.

### Tasks
- [x] Add `mcp` to requirements.
- [x] Implement `mcp_server.py`.
    - [x] Setup `Server("zk-smart-search")`.
    - [x] Initialize `ZKSearcher` with a dummy console.
    - [x] Implement `list_tools`.
    - [x] Implement `call_tool`.
    - [x] Handler: `search_notes` (switch between keyword/semantic logic).
    - [x] Handler: `read_note`.
- [x] Test locally by running the script (checked imports).
- [x] Added `tests/test_mcp_integration.py` for logic testing.

### Completed
*None yet*

## Commit
### Phase Entrance Criteria
- [x] Server is functional and tested (Verified imports and tests).
- [x] Code is clean and documented.

### Tasks
- [x] Test with integration test suite.
- [x] Update README with MCP configuration instructions (JSON snippet).

### Completed
- [x] Updated README.
- [x] Verified tests pass.

## Key Decisions
- **Architecture**: Use `mcp.server.Server` with `stdio` transport.
- **IO Handling**: Must suppress `rich` output from `zkss` modules to avoid breaking JSON-RPC.
- **Tools**: `search_notes` and `read_note`.

## Notes
*Additional context and observations*

---
*This plan is maintained by the LLM. Tool responses provide guidance on which section to focus on and what tasks to work on.*
