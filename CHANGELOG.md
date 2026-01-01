# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Semantic Search using `sentence-transformers` and `chromadb`.
- MCP Server integration (`mcp_server.py`) to expose search tools to AI assistants.
- Configurable search result limit:
  - Added `-n` / `--limit` CLI argument.
  - Added `DEFAULT_RESULTS` setting in `settings.py` (default: 10).

### Fixed
- Fixed incremental indexing bug where files were re-indexed unnecessarily due to floating-point precision issues with `mtime`.

### Changed
- Updated project description in `pyproject.toml`.
- Comprehensive updates to `README.md` including setup instructions for Semantic Search and MCP.

### Removed
- Redundant `ROADMAP.md` (consolidated into `development-plan.md`).
