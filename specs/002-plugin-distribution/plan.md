# Implementation Plan: Plugin & Distribution Packaging

**Branch**: `002-plugin-distribution` | **Date**: 2026-03-22 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-plugin-distribution/spec.md`

## Summary

Package the mcp-tekna MCP server for distribution across multiple
channels: Claude Code plugin (`.claude-plugin/plugin.json`), Claude
Desktop (`.mcpb` bundle + `server.json`), package registry (PyPI via
`uvx`), marketplace (Glama.ai), and Docker (streamable-http). All
channels use the same server codebase with zero mandatory configuration.

## Technical Context

**Language/Version**: Python >=3.10
**Primary Dependencies**: `mcp[cli]` (FastMCP), `httpx`, `python-dotenv`
**Storage**: N/A (no persistent storage)
**Testing**: `pytest`, `pytest-asyncio`
**Target Platform**: Cross-platform (Windows, macOS, Linux)
**Project Type**: MCP server with multi-channel distribution
**Performance Goals**: Container startup <10s, tool response <5s
**Constraints**: Zero mandatory env vars, public data only
**Scale/Scope**: Single server, multiple distribution manifests

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Test-First (NON-NEGOTIABLE) | PASS | Manifest validation tests will verify JSON schemas and file structure. `.mcpb` build verified via CLI. |
| II. MCP Protocol Compliance | PASS | `server.json` follows official MCP server schema. `.mcpb` manifest follows `manifest_version: 0.3`. Tools use proper JSON Schema input schemas. |
| III. Simplicity (YAGNI) | PASS | Only required distribution files are created. No custom build tooling — uses standard `mcpb` CLI, `setuptools-scm`, and Docker. |

No violations. Gate passed.

## Project Structure

### Documentation (this feature)

```text
specs/002-plugin-distribution/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (repository root)

```text
.claude-plugin/
├── plugin.json              # Claude Code plugin manifest
└── marketplace.json         # Marketplace registry metadata

server.json                  # MCP server registry manifest
glama.json                   # Glama.ai marketplace entry

.mcp.json                    # Production MCP client config
.mcp.dev.json                # Development MCP client config

mcpb/
├── manifest.json            # .mcpb bundle manifest
└── .mcpbignore              # Files to exclude from bundle

Dockerfile                   # Multi-stage container build
docker-compose.yml           # Local development stack

pyproject.toml               # Package metadata (version source of truth)

src/mcp_tekna/
├── __init__.py
├── __main__.py
└── server.py                # Entry point (stdio + streamable-http)

tests/
└── test_manifests.py        # Manifest validation tests
```

**Structure Decision**: Single project layout following mcp-outline
patterns. Distribution manifests live at repository root or in
dedicated directories (`.claude-plugin/`, `mcpb/`). The server code
under `src/` is shared across all channels — transport mode is
selected at runtime.

## Complexity Tracking

No violations to justify.
