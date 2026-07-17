# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.17] - 2026-07-17

### Changed
- Raised the `mcp` dependency floor to `>=1.27.2` and added it to `[tool.uv] constraint-dependencies`.

### Fixed
- Refreshed `uv.lock` and re-exported `requirements.txt` to address Dependabot alerts for `mcp` (CVE-2026-52870 / GHSA-hvrp-rf83-w775).

## [0.3.16] - 2026-07-08

### Changed
- Raised `[tool.uv] constraint-dependencies` floor for `pydantic-settings` (>=2.14.2).

### Fixed
- Refreshed `uv.lock` and re-exported `requirements.txt` to address Dependabot alerts for `pydantic-settings` symlink traversal in `NestedSecretsSettingsSource`.

## [0.3.15] - 2026-07-08

### Fixed
- MCP search results now include copy-paste-ready note filenames with the `.md` suffix so agents can pass them directly to `read_note`.
- `read_note` accepts filenames with or without the `.md` suffix.

## [0.3.14] - 2026-07-08

### Changed
- Default semantic search to Hugging Face Hub offline mode so the cached embedding model loads without unauthenticated Hub checks or warnings on every run.

## [0.3.13] - 2026-07-08

### Fixed
- Fixed MCP stdio transport corruption when semantic indexing printed progress output to stdout, which broke JSON-RPC with `Unexpected token 'E', "Embedding."... is not valid JSON`.
- Routed indexer status and embedding progress to stderr, and added an MCP stdout guard so library output cannot pollute the JSON-RPC channel.

## [0.3.12] - 2026-06-19

### Changed
- Raised `[tool.uv] constraint-dependencies` floors for `python-multipart` (>=0.0.30) and `pyjwt` (>=2.13.0).

### Fixed
- Refreshed `uv.lock` and re-exported `requirements.txt` to address Dependabot alerts for `python-multipart` (CVE-2026-53539) and `pyjwt` (CVE-2026-48526).

## [0.3.11] - 2026-06-17

### Changed
- Added `starlette>=1.0.1` to `[tool.uv] constraint-dependencies` and raised the `cryptography` floor to `>=48.0.1`.

### Fixed
- Refreshed `uv.lock` and re-exported `requirements.txt` to address Dependabot alerts for `starlette` (CVE-2026-48710) and `cryptography` 48.0.0.

## [0.3.10] - 2026-05-30

### Added
- Added `SECURITY.md` documenting the impact assessment for CVE-2026-45829 (ChromaDB / ChromaToast): the project uses embedded `PersistentClient` only, so the vulnerable FastAPI server path is not exposed.

## [0.3.9] - 2026-05-13

### Changed
- Bumped resolved transitive versions in `uv.lock` and re-exported `requirements.txt` for the embedding and MCP stack (notably `torch`, `transformers`, `onnxruntime`, `sentence-transformers`, `chromadb`, `huggingface-hub`, `mcp`, `starlette`, `uvicorn`, OpenTelemetry, and `pydantic`-related packages).

## [0.3.8] - 2026-05-12

### Changed
- Added `[tool.uv] constraint-dependencies` in `pyproject.toml` so resolution keeps minimum patched releases for `urllib3`, `python-multipart`, `cryptography`, and `requests`.
- Raised the dev dependency pin for `pytest` to `>=9.0.3`.

### Fixed
- Refreshed `uv.lock` and regenerated `requirements.txt` to address Dependabot alerts affecting those packages (including streaming/decompression handling in `urllib3`, multipart parsing limits in `python-multipart`, `cryptography` buffer handling, temp-file reuse in `requests`, and `pytest` temporary directory handling).

## [0.3.7] - 2026-03-14

### Changed
- Refreshed dependency resolution in `uv.lock` and regenerated `requirements.txt` via `uv` to align pins across the project.
- Updated multiple transitive packages during the refresh (including `chromadb`, `sentence-transformers`, `transformers`, `onnxruntime`, and telemetry-related packages).

### Fixed
- Upgraded `pyjwt` to `2.12.1` (from `2.11.0`) to address the GitHub security alert for CVE-2026-32597.

## [0.3.6] - 2026-02-11

### Changed
- Added `*.egg-info/` to `.gitignore` and removed the existing `zk_smart_search.egg-info/` directory from git tracking to prevent auto-generated build metadata from cluttering the repository.
- Refreshed dependencies in `uv.lock` (including `chromadb`, `cryptography`, `grpcio`, `huggingface-hub`, `numpy`, `onnxruntime`, `orjson`, `pypika`, `rich`, `setuptools`, `tenacity`, `torch`, `tqdm`, `transformers`, and `typer`).
- Updated `zk-smart-search` version to `0.3.5` in `uv.lock`.

## [0.3.5] - 2026-01-31

### Removed
- Removed the temporary security note from `README.md` as `protobuf` has been updated.

## [0.3.4] - 2026-01-31

### Changed
- Refreshed `uv.lock` with dependency updates (including `huggingface-hub`, `orjson`, `protobuf`, `pyjwt`, and `tqdm`).

## [0.3.3] - 2026-01-28

### Changed
- Updated `README.md` security note to reference the current `protobuf` advisory and clarify local-use impact.
- Refined installation guidance to mention `uv` and clarified virtual environment options.
- Refreshed README wording around semantic search and MCP support.

## [0.3.2] - 2026-01-28

### Added
- Added autogenerated `requirements.txt` generated via `uv pip compile`.

### Changed
- Refreshed `uv.lock` with dependency updates (including `cryptography`, `mcp`, `python-multipart`, `rich`, `sentence-transformers`, `setuptools`, and `transformers`) and added `typer-slim`.

## [0.3.1] - 2026-01-02

### Changed
- Added explicit risk assessment to `README.md`.

### Maintenance Notes
- **Dependency Pin**: `urllib3` is pinned to `2.3.0` due to a version conflict in the `kubernetes` client (transitive dependency via `chromadb`).
- **Security Assessment**: Evaluated `urllib3` [GHSA-2xpw-w6gg-jr37](https://github.com/urllib3/urllib3/security/advisories/GHSA-2xpw-w6gg-jr37) and [GHSA-gm62-xv2j-4w53](https://github.com/urllib3/urllib3/security/advisories/GHSA-gm62-xv2j-4w53). Risk is considered negligible for local Zettelkasten use. Upgrade will follow once upstream releases a fix.

## [0.3.0] - 2026-01-02

### Changed
- Migrated dependency management to `pyproject.toml` (PEP 621), removing the redundant `requirements.in`.
- Updated workflow to generate `requirements.txt` directly from `pyproject.toml` using `pip-tools`.
- Upgraded all dependencies to their latest versions during the migration.

## [0.2.0] - 2026-01-02

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

