# Quickstart: Read-Only Tool Annotations

## What changes

Each `@mcp.tool()` decorator gets an `annotations` parameter with `readOnlyHint=True`.

## Before

```python
@mcp.tool()
async def get_member_benefits() -> str:
```

## After

```python
from mcp.types import ToolAnnotations

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def get_member_benefits() -> str:
```

## Files to change

1. `src/mcp_tekna/benefits.py` — 1 tool
2. `src/mcp_tekna/events.py` — 2 tools
3. `src/mcp_tekna/news.py` — 1 tool

## Verification

```bash
uv run pytest tests/test_annotations.py -v
```
