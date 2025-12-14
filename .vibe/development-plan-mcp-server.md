# Development Plan: zk-smart-search (mcp-server feature)

*Generated on 2025-12-14 by Vibe Feature MCP*
*Workflow: [epcc](https://mrsimpson.github.io/responsible-vibe-mcp/workflows/epcc)*

## Goal
Create a Model Context Protocol (MCP) server that exposes the Zettelkasten search functionality (both keyword and semantic) to AI assistants like Claude Desktop and Cursor.

## Explore
### Tasks
- [ ] Research `mcp` Python SDK usage and requirements.
- [ ] Determine the tools to expose (e.g., `search_notes`, `get_note_content`).
- [ ] Decide on transport mechanism (Stdio vs SSE) - likely Stdio for local use.
- [ ] Prototype a basic MCP server script.

### Completed
- [x] Created development plan file

## Plan
### Phase Entrance Criteria
- [ ] MCP SDK dependencies identified.
- [ ] List of tools and their schemas defined.
- [ ] Integration strategy with `zkss` code (reuse `ZKSearcher` vs direct import) defined.

### Tasks
- [ ] Design `server.py` structure.
- [ ] Define the `search_notes` tool schema (arguments: query, semantic_mode).
- [ ] Define the `read_note` tool schema (arguments: filename).

### Completed
*None yet*

## Code
### Phase Entrance Criteria
- [ ] Tool schemas are finalized.
- [ ] Server architecture is documented.

### Tasks
- [ ] Add `mcp` to requirements.
- [ ] Implement `server.py` using `FastMCP` or low-level SDK.
- [ ] Implement `search_notes` handler (integrating with `ZKSearcher` and `IndexManager`).
- [ ] Implement `read_note` handler.
- [ ] Add configuration for Claude Desktop (json snippet).

### Completed
*None yet*

## Commit
### Phase Entrance Criteria
- [ ] Server is functional and tested with an MCP client (inspector).
- [ ] Code is clean and documented.

### Tasks
- [ ] Test with `npx @modelcontextprotocol/inspector`.
- [ ] Update README with MCP configuration instructions.

### Completed
*None yet*

## Key Decisions
*Important decisions will be documented here as they are made*

## Notes
*Additional context and observations*

---
*This plan is maintained by the LLM. Tool responses provide guidance on which section to focus on and what tasks to work on.*
