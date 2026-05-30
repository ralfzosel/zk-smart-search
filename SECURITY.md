# Security

## CVE-2026-45829 (ChromaDB / ChromaToast)

**Advisory:** [GHSA-f4j7-r4q5-qw2c](https://github.com/advisories/GHSA-f4j7-r4q5-qw2c)  
**Severity:** Critical (CVSS 10.0)  
**Affected package:** `chromadb` 1.0.0–1.5.9 (Python FastAPI server)

### Impact on zk-smart-search

This project uses ChromaDB only as an **embedded local store** via `PersistentClient` (index at `~/.zkss_index`). It does **not** start or expose ChromaDB's HTTP API server, which is the affected component.

The MCP server uses stdio transport and is unrelated to ChromaDB's network API.

**Practical risk for this deployment: low.**

### Mitigation

- No patched `chromadb` release is available yet (latest: 1.5.9).
- Do not expose ChromaDB's FastAPI server if deploying ChromaDB separately in the future; prefer the Rust-based `chroma run` frontend.
- Upgrade `chromadb` as soon as a fixed version is published.

### Reporting vulnerabilities in zk-smart-search

Open an issue or contact the repository owner directly.
