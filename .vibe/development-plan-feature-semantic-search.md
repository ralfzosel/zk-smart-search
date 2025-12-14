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
- [ ] Strategy for handling index updates (incremental vs full rebuild) is defined.
- [ ] Integration point with existing `ZKSearcher` class is identified.

### Tasks
- [ ] Design the `Indexer` class or module (must support incremental updates for 5k+ notes).
- [ ] Define the API for `semantic_search` method in `ZKSearcher`.
- [ ] Plan the CLI command structure (e.g., `zkss --semantic "query"`).

### Completed
*None yet*

## Code
### Phase Entrance Criteria
- [ ] Implementation plan is documented.
- [ ] Architecture for storing/loading index is defined.
- [ ] CLI user interface design is settled.

### Tasks
- [x] Add `sentence-transformers` and `chromadb` to requirements.
- [ ] Implement `IndexManager` to handle embedding generation and storage.
- [ ] Implement `semantic_search` method in `ZKSearcher`.
- [ ] Add integration tests for semantic search.
- [ ] Update `main` to expose semantic search option.

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

## Notes
*Additional context and observations*

---
*This plan is maintained by the LLM. Tool responses provide guidance on which section to focus on and what tasks to work on.*
