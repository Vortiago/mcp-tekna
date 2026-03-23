# Implementation Plan: Read-Only Tool Annotations

**Branch**: `005-readonly-tool-annotations` | **Date**: 2026-03-23 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/005-readonly-tool-annotations/spec.md`

## Summary

Add MCP-compliant `readOnlyHint` annotations to all 4 tools (`get_member_benefits`, `search_events`, `get_event_details`, `get_news`) using FastMCP's `annotations` parameter on `@mcp.tool()`. This enables MCP consumers to auto-approve tool calls as read-only.

## Technical Context

**Language/Version**: Python >=3.10
**Primary Dependencies**: FastMCP (`mcp[cli]` v1.26.0), `mcp.types.ToolAnnotations`
**Storage**: N/A
**Testing**: pytest, pytest-asyncio, pytest-httpx
**Target Platform**: MCP server (cross-platform)
**Project Type**: MCP server (library/service)
**Performance Goals**: N/A (metadata-only change)
**Constraints**: None — annotations are protocol-level metadata with zero runtime impact
**Scale/Scope**: 4 tool decorators to update, 3 source files

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Test-First (NON-NEGOTIABLE) | PASS | Tests will verify annotations appear in `tools/list` response |
| II. MCP Protocol Compliance | PASS | `ToolAnnotations(readOnlyHint=True)` is MCP spec compliant |
| III. Simplicity (YAGNI) | PASS | No new dependencies, no abstractions — direct decorator parameter |

No violations. No complexity tracking needed.

## Project Structure

### Documentation (this feature)

```text
specs/005-readonly-tool-annotations/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (repository root)

```text
src/mcp_tekna/
├── benefits.py          # MODIFY: add annotations to get_member_benefits
├── events.py            # MODIFY: add annotations to search_events, get_event_details
└── news.py              # MODIFY: add annotations to get_news

tests/
└── test_annotations.py  # NEW: verify all tools expose readOnlyHint
```

**Structure Decision**: Existing flat module structure. Changes are limited to adding an `annotations` parameter to each `@mcp.tool()` decorator in 3 existing files, plus one new test file.

## Implementation Approach

### Change per tool file

Each tool file requires two changes:
1. Add import: `from mcp.types import ToolAnnotations`
2. Update each `@mcp.tool()` to `@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))`

### Files to modify

| File | Tools | Change |
|------|-------|--------|
| `src/mcp_tekna/benefits.py` | `get_member_benefits` | Add `annotations` param to decorator |
| `src/mcp_tekna/events.py` | `search_events`, `get_event_details` | Add `annotations` param to both decorators |
| `src/mcp_tekna/news.py` | `get_news` | Add `annotations` param to decorator |

### Test strategy

Create `tests/test_annotations.py` that:
1. Instantiates the FastMCP server
2. Calls `list_tools()` to get all registered tools
3. Asserts each tool has `annotations.readOnlyHint == True`
4. Asserts no tools are missing annotations

This follows TDD: write the test first (red), then modify the decorators (green).
