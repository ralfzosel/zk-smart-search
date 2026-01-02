# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Rich-to-Markdown conversion for MCP server output to improve AI assistant readability.
- `zkss_markdown.py` helper utility to handle the conversion logic.
- Comprehensive tests for MCP output formatting in `tests/test_mcp_output.py`.

### Changed
- MCP `search_notes` tool now bolds filenames and content locations while stripping color tags.
- Updated `mcp_server.py` to use markdown conversion for both keyword and semantic search results.

## [0.1.0] - 2026-01-01

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
- Updated `.cursor/mcp.json` configuration.

### Removed
- Redundant `ROADMAP.md` (consolidated into `development-plan.md`).

