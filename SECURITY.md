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

## ChromaDB Python FastAPI server (CVE-2026-45829, CVE-2026-45830, CVE-2026-45831, CVE-2026-45833)

These advisories all apply to ChromaDB's **networked Python FastAPI server** (auth, multi-tenant RBAC, and HTTP collection-update APIs). There is still **no patched `chromadb` release** (latest: 1.5.9).

| CVE | Advisory | Severity | Issue |
|---|---|---|---|
| CVE-2026-45829 | [GHSA-f4j7-r4q5-qw2c](https://github.com/advisories/GHSA-f4j7-r4q5-qw2c) | Critical | ChromaToast on the FastAPI server |
| CVE-2026-45830 | [GHSA-2wm9-hf6c-p5cr](https://github.com/advisories/GHSA-2wm9-hf6c-p5cr) | High | Authenticated users can read/write any tenant's collection |
| CVE-2026-45831 | [GHSA-xph7-9rjv-w5fr](https://github.com/advisories/GHSA-xph7-9rjv-w5fr) | High | `SimpleRBACAuthorizationProvider` ignores tenant/database/collection scope |
| CVE-2026-45833 | [GHSA-36p7-vc44-83pf](https://github.com/advisories/GHSA-36p7-vc44-83pf) | Critical | Code injection via collection update + `trust_remote_code` on `/api/v2/.../collections/{id}` |

**Affected package:** `chromadb` 0.4.17–1.5.9 (RBAC issue from 0.5.0)

### Impact on zk-smart-search

This project uses ChromaDB only as an **embedded local store** via `PersistentClient` (index at `~/.zkss_index`). It does **not** start or expose ChromaDB's HTTP API, enable SimpleRBAC, or accept remote collection-update payloads.

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
