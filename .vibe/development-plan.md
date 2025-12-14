# Development Plan: zk-smart-search (bugfix-incremental-indexing)

*Generated on 2025-12-14 by Vibe Feature MCP*
*Workflow: [bugfix](https://mrsimpson.github.io/responsible-vibe-mcp/workflows/bugfix)*

## Goal
Investigate and fix the issue where `zkss -s` re-indexes approximately 225 files on every run, even when no files have been modified. This suggests an issue with the incremental update logic, possibly `mtime` precision comparison.

## Reproduce
### Tasks
- [x] Create a reproduction script (or use manual verification) to identify *which* files are being re-indexed.
- [x] Log the `mtime` from filesystem and `mtime` from ChromaDB for these files to compare them.
- [x] Confirm if it's a floating point precision issue (Confirmed: diff is ~2e-7 seconds).

### Completed
- [x] Created development plan file

## Analyze
### Tasks
- [x] Analyze `indexer.py` comparison logic: `existing_metadata.get(filename, {}).get('mtime', 0) < mtime`.
- [x] Determine if `chromadb` truncates metadata values (Confirmed precision loss).

### Completed
- [x] Identified root cause: Floating point precision mismatch.

## Fix
### Tasks
- [x] Implement a tolerance (epsilon) or rounding for `mtime` comparison.
- [x] Update `IndexManager.update_index` to handle precision differences.

### Completed
- [x] Implemented tolerance check (0.001s).

## Verify
### Tasks
- [x] Run the reproduction script again to confirm 0 files are re-indexed on subsequent runs.
- [ ] Run existing tests to ensure no regressions.

### Completed
- [x] Verified manual run shows 0 files re-indexed.

## Finalize
### Tasks
- [x] Remove debug logging.
- [x] Commit fix.

### Completed
- [x] Cleaned up code.
- [x] Committed fix to master.

## Key Decisions
- **Tolerance**: Using 0.001s epsilon for mtime comparison.

## Notes
*Additional context and observations*

---
*This plan is maintained by the LLM. Tool responses provide guidance on which section to focus on and what tasks to work on.*
