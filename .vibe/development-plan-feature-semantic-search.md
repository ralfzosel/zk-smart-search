# Development Plan: zk-smart-search (feature/semantic-search branch)

*Generated on 2025-12-14 by Vibe Feature MCP*
*Workflow: [epcc](https://mrsimpson.github.io/responsible-vibe-mcp/workflows/epcc)*

## Goal
Implement Semantic Search functionality to allow finding notes based on meaning rather than just keywords. This involves integrating embedding generation (using `sentence-transformers`) and vector storage (`chromadb` or similar).

## Explore
### Tasks
- [x] Research and select specific embedding model (Selected: `all-MiniLM-L6-v2` via `sentence-transformers`).
- [x] Determine storage strategy for the vector index (Selected: `chromadb` for local persistence).
- [x] Verify `chromadb` compatibility and requirements.
- [ ] Prototype basic embedding generation and retrieval script.

### Completed
- [x] Created development plan file

## Plan
### Phase Entrance Criteria
- [x] Embedding model and vector store libraries are selected and verified.
- [x] Strategy for handling index updates (incremental vs full rebuild) is defined.
- [x] Integration point with existing `ZKSearcher` class is identified.

### Tasks
- [x] Design the `Indexer` class or module (Separate `indexer.py` module).
- [x] Define the API for `semantic_search` method in `ZKSearcher` (Delegates to `Indexer`).
- [x] Plan the CLI command structure (New flags: `-s/--semantic` and `--reindex`).
- [x] Define storage location logic (Default: `~/.zkss_index`, configurable).

### Completed
*None yet*

## Code
### Phase Entrance Criteria
- [x] Implementation plan is documented.
- [x] Architecture for storing/loading index is defined.
- [x] CLI user interface design is settled.

### Tasks
- [x] Add `sentence-transformers` and `chromadb` to requirements.
- [x] Create `indexer.py` with `IndexManager` class.
    - [x] Implement initialization (load chromadb).
    - [x] Implement `update_index()`: Scan files, check mtime, upsert changed, remove deleted.
    - [x] Implement `search(query, n_results)`: Return list of filenames.
- [x] Update `zkss.py`:
    - [x] Import `IndexManager`.
    - [x] Add CLI arguments (`-s`, `--reindex`).
    - [x] Integrate into `run()` loop (if semantic, skip standard filters or combine?).
- [x] Add integration tests for semantic search (mocking the heavy ML parts).

### Completed
*None yet*

## Commit
### Phase Entrance Criteria
- [ ] Semantic search is functional and tested.
- [ ] Code is linted and clean.
- [ ] Documentation is updated with new features.

### Tasks
- [ ] Remove any prototype/debug code.
- [ ] Ensure all tests pass.
- [ ] Update README with semantic search usage instructions.

### Completed
*None yet*

## Key Decisions
- **Stack**: `sentence-transformers` (Model: `all-MiniLM-L6-v2`) + `chromadb` for storage.
- **Reasoning**: Best balance of local ease-of-use and scalability for >5,000 notes. `chromadb` handles incremental updates well.
- **Architecture**: Separate `indexer.py` module to keep `zkss.py` clean.
- **CLI**: `-s` flag triggers semantic search.

## Notes
*Additional context and observations*

---
*This plan is maintained by the LLM. Tool responses provide guidance on which section to focus on and what tasks to work on.*
