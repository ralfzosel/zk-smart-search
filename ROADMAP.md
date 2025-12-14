# Roadmap

## Phase 1: Refactoring (Completed)
- [x] Refactor `zkss.py` to improve code structure.
- [x] Introduce `ZKSearcher` class for better modularity.
- [x] Fix list iteration bug.
- [x] Initialize Responsible Vibe MCP configuration.

## Phase 2: Testing & Stability (Current Focus)
- [x] Set up `pytest` environment.
- [x] Create `tests/test_zkss.py`.
- [x] Add unit tests for `ZKSearcher` methods (`strip_ending`, `filter_and_print`).
- [x] Mock file system operations to test sorting and reading without actual files.

## Phase 3: Semantic Search
- [ ] Research embedding libraries (e.g., `sentence-transformers`, `chromadb`).
- [ ] Implement index generation for Zettelkasten notes.
- [ ] Add `semantic_search` method to `ZKSearcher`.

## Phase 4: MCP Server
- [ ] Create a Model Context Protocol (MCP) server wrapper.
- [ ] Expose search functionality via MCP tools.
- [ ] Integrate with AI assistants (like Claude/Cursor).
