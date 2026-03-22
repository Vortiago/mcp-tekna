# Implementation Plan: Tekna Data Tools

**Branch**: `001-tekna-data-tools` | **Date**: 2026-03-22 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-tekna-data-tools/spec.md`

## Summary

Implement four MCP tools for the mcp-tekna server: `search_events`,
`get_event_details`, `get_news`, and `get_member_benefits`. These
tools fetch data from Tekna's public APIs and website, returning
structured results with URLs for each item. All responses are cached
with a 15-minute TTL. The events API uses a colon-separated DSL, news
uses a POST JSON API, and member benefits require HTML parsing.

## Technical Context

**Language/Version**: Python >=3.10
**Primary Dependencies**: `mcp[cli]` (FastMCP), `httpx`, `python-dotenv`, `cachetools`, `beautifulsoup4`
**Storage**: In-memory TTL cache (cachetools)
**Testing**: `pytest`, `pytest-asyncio`, `pytest-httpx` (for mocking httpx)
**Target Platform**: Cross-platform (Windows, macOS, Linux)
**Project Type**: MCP server tools
**Performance Goals**: Tool response <5s, cached response <100ms
**Constraints**: No authentication required, public data only, 30s upstream timeout
**Scale/Scope**: 4 tools, ~17 member benefits, hundreds of events/articles

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Test-First (NON-NEGOTIABLE) | PASS | Tests written first for each tool: unit tests for response parsing, integration tests against mocked APIs, contract tests for MCP tool schemas. |
| II. MCP Protocol Compliance | PASS | All tools define JSON Schema input schemas. Responses use text content. Errors use `isError` flag. FastMCP handles tool registration. |
| III. Simplicity (YAGNI) | PASS | Flat module structure. One service module per data source. In-memory cache (no Redis/disk). Direct httpx calls (no abstraction layer). |

No violations. Gate passed.

## Project Structure

### Documentation (this feature)

```text
specs/001-tekna-data-tools/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── mcp-tools.md     # Tool input/output contracts
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (repository root)

```text
src/mcp_tekna/
├── __init__.py
├── __main__.py
├── server.py            # FastMCP server + tool registration
├── tekna_client.py      # httpx client for Tekna APIs
├── events.py            # Event search + details tools
├── news.py              # News tool
├── benefits.py          # Member benefits tool (HTML parsing)
├── cache.py             # TTL cache wrapper
└── models.py            # Response formatting helpers

tests/
├── conftest.py          # Shared fixtures, mock responses
├── test_manifests.py    # Distribution manifest tests (existing)
├── test_server.py       # Server transport tests (existing)
├── test_events.py       # Event tool tests
├── test_news.py         # News tool tests
├── test_benefits.py     # Benefits tool tests
├── test_cache.py        # Cache behavior tests
└── fixtures/            # Sample API response JSON files
    ├── events_response.json
    ├── news_response.json
    └── benefits_page.html
```

**Structure Decision**: Flat module layout within `src/mcp_tekna/`.
One module per data source (events, news, benefits) plus shared
client and cache. No sub-packages — follows YAGNI principle.

## New Dependencies

- `cachetools` — TTL cache implementation (lightweight, well-maintained)
- `beautifulsoup4` — HTML parsing for member benefits page
- `pytest-httpx` — Mock httpx requests in tests (dev only)

## Complexity Tracking

No violations to justify.
