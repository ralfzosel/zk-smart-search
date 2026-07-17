# Security

## CVE-2026-52870 (MCP Python SDK / experimental tasks)

**Advisory:** [GHSA-hvrp-rf83-w775](https://github.com/advisories/GHSA-hvrp-rf83-w775)  
**Severity:** High  
**Affected package:** `mcp` 1.23.0–1.27.1

### Impact on zk-smart-search

This project runs the MCP server over **stdio** and does **not** enable the experimental tasks feature. The advisory concerns cross-client access to task handlers on multi-session servers.

**Practical risk for this deployment: low.**

### Mitigation

- Upgraded to `mcp>=1.27.2` (resolved to 1.28.1).

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

## CVE-2025-3000 (PyTorch / `torch.jit.script`)

**Advisory:** [GHSA-rrmf-rvhw-rf47](https://github.com/advisories/GHSA-rrmf-rvhw-rf47)  
**Severity:** Low (GitHub-reviewed)  
**Affected package:** `torch` through 2.12.0

### Impact on zk-smart-search

`torch` is a **transitive dependency** of `sentence-transformers`, used only for local embedding inference. This project does **not** call `torch.jit.script` or otherwise use TorchScript.

**Practical risk for this deployment: low.**

### Mitigation

- No patched `torch` release is available yet (Dependabot lists no fixed version).
- Upgrade `torch` as soon as a fixed release is published and re-validate the Dependabot alert.
- Re-check by 2026-12-08 whether a patched `torch` release has landed.

### Reporting vulnerabilities in zk-smart-search

Open an issue or contact the repository owner directly.
