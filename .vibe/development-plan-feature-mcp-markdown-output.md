# Development Plan: zk-smart-search (feature/mcp-markdown-output branch)

*Generated on 2026-01-01 by Vibe Feature MCP*
*Workflow: [epcc](https://mrsimpson.github.io/responsible-vibe-mcp/workflows/epcc)*

## Goal
Improving MCP Server output by stripping Rich tags and using Markdown formatting for better AI assistant readability.
- Keywords (`[green]`) -> Stripped (plain text)
- Filenames / Content (`[yellow]`) -> **bold**
- Remove all other Rich tags/ANSI codes.
- Add pytest tests for verification.

## Explore
### Phase Entrance Criteria:
- [x] Initial development plan created.

### Tasks
- [x] Identify where `Rich` tags are generated in `zkss.py` or `indexer.py`.
- [x] Locate the MCP tool implementation in `mcp_server.py`.
- [x] Research how to strip Rich tags using `rich` built-ins or regex.

### Completed
- [x] Created development plan file
- [x] Identified Rich tag usage and MCP server integration.
- [x] Verified `rich.markup.render` and `Text.spans` as a robust way to convert tags.

## Plan
### Phase Entrance Criteria:
- [x] Current implementation of `Rich` output in `mcp_server.py` and `indexer.py` is understood.
- [x] Transformation logic: [green] tags are stripped, [yellow] tags are converted to **bold**.
- [x] Dependencies: Only `rich` is required for parsing tags.

### Tasks
- [x] Define implementation strategy (use `zkss_markdown.py` helper).
- [x] Identify if `requirements.in` needs updating (unlikely, but double check).

### Completed
- [x] Implementation strategy defined.

## Code
### Phase Entrance Criteria:
- [x] Implementation strategy is documented.
- [x] Test cases are defined.

### Tasks
- [x] Create `zkss_markdown.py` with `convert_rich_to_markdown` utility.
- [x] Modify `mcp_server.py` to use `convert_rich_to_markdown` in `perform_keyword_search`.
- [x] Update `perform_semantic_search` in `mcp_server.py` to use bold for filenames.
- [x] Create `tests/test_mcp_output.py` with exhaustive test cases for Rich-to-Markdown mapping.
- [x] Run `pytest` to verify all search tools return valid Markdown.

### Completed
- [x] `zkss_markdown.py` implemented.
- [x] `mcp_server.py` updated to use markdown conversion.
- [x] Semantic search updated to bold filenames.
- [x] Unit and integration tests passed.

## Commit
### Phase Entrance Criteria:
- [x] All code changes are implemented.
- [x] All tests pass.
- [x] Linter errors are resolved.

### Tasks
- [x] Clean up development artifacts.
- [x] Verify final test state.
- [x] Update `CHANGELOG.md`.

### Completed
- [x] All tasks completed.

## Key Decisions
1. **[2026-01-01] Strip [green] tags**: Originally planned to use backticks for keywords, but decided to simply strip the tags for cleaner output as the assistant can already identify keywords in context.
2. **[2026-01-01] Bold [yellow] tags**: Retained bolding for filenames and content locations to provide clear structural hierarchy.

## Notes
*Additional context and observations*

---
*This plan is maintained by the LLM. Tool responses provide guidance on which section to focus on and what tasks to work on.*
