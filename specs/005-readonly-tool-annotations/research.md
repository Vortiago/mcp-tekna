# Research: Read-Only Tool Annotations

## R1: FastMCP Annotation API

**Decision**: Use `@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))` decorator parameter.

**Rationale**: FastMCP v1.26.0 (installed in project) natively supports the `annotations` parameter on `@mcp.tool()`. The `ToolAnnotations` class from `mcp.types` is a Pydantic BaseModel that maps directly to the MCP specification's tool annotations schema. Annotations are automatically serialized in the `tools/list` MCP response.

**Alternatives considered**:
- Manual tool registration via `mcp.add_tool()` — unnecessary complexity when decorator parameter exists.
- Post-registration patching of tool metadata — fragile and non-idiomatic.

## R2: ToolAnnotations Fields Available

**Decision**: Set only `readOnlyHint=True`. Leave other fields (`destructiveHint`, `idempotentHint`, `openWorldHint`) at defaults.

**Rationale**: All 4 tools are read-only (fetch data from Tekna APIs). The `readOnlyHint=True` is sufficient and accurate. Setting `destructiveHint` or `idempotentHint` is meaningful only when `readOnlyHint=False` per MCP spec. `openWorldHint` defaults to `True` which is correct since tools interact with external Tekna APIs.

**Alternatives considered**:
- Setting `openWorldHint=True` explicitly — unnecessary since it's the default, and adds noise per YAGNI principle.
- Setting `idempotentHint=True` alongside — not meaningful when readOnlyHint is True per MCP spec.

## R3: Import Location

**Decision**: Import `ToolAnnotations` from `mcp.types` in each tool module.

**Rationale**: Direct import from the canonical location. No wrapper or re-export needed. Each tool module is self-contained.

**Alternatives considered**:
- Creating a shared constant `READONLY_ANNOTATIONS = ToolAnnotations(readOnlyHint=True)` in `server.py` — premature abstraction for a one-liner used 4 times across 3 files.
