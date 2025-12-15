# Development Plan: zk-smart-search (configurable-limit)

*Generated on 2025-12-14 by Vibe Feature MCP*
*Workflow: [minor](https://mrsimpson.github.io/responsible-vibe-mcp/workflows/minor)*

## Goal
Make the number of search results configurable via a setting and a CLI argument, changing the default from hardcoded 15 to 10.

## Explore
### Tasks
- [x] Analyze current implementation in `indexer.py` and `zkss.py`.
- [x] Design the changes:
    - `settings.py`: Add `DEFAULT_RESULTS = 10`.
    - `indexer.py`: Import default, update method signature.
    - `zkss.py`: Add argparse argument, pass to search.

### Completed
- [x] Analysis complete (done in conversation).
- [x] Design agreed upon with user.

## Implement

### Phase Entrance Criteria:
- [x] Design is clear and tasks are defined.
- [x] User has approved the approach.

### Tasks
- [x] Add `DEFAULT_RESULTS = 10` to `settings.py`.
- [x] Update `indexer.py` to use `DEFAULT_RESULTS` as default for `search()`.
- [x] Update `zkss.py` to add `-n` / `--limit` argument to `argparse`.
- [x] Pass the limit argument to `indexer.search()` calls in `zkss.py`.
- [x] Verify functionality with manual test.
- [x] Add tests for CLI argument parsing in `tests/test_zkss.py`.

## Finalize

### Phase Entrance Criteria:
- [x] Implementation is complete and verified.
- [x] No regressions in existing search behavior.

### Tasks
- [x] Review code for cleanliness.
- [x] Commit changes.

### Completed
- [x] Code reviewed and committed.

## Key Decisions
- Default limit set to 10 (industry standard).
- CLI flag will be `-n` or `--limit`.

## Notes
- "More Like This" feature is next, but this minor change was requested first.

---
*This plan is maintained by the LLM. Tool responses provide guidance on which section to focus on and what tasks to work on.*
