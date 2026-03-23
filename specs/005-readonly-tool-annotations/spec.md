# Feature Specification: Read-Only Tool Annotations

**Feature Branch**: `005-readonly-tool-annotations`
**Created**: 2026-03-23
**Status**: Draft
**Input**: User description: "We should have read only annotation on all the tool calls since they are read only. That way it's easier for consumers to specify allow and know that it's read only. This is a MCP spec and FastMCP feature"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - MCP Consumer Auto-Approves Read-Only Tools (Priority: P1)

A consumer (e.g., Claude Desktop, an MCP client application) connects to the mcp-tekna server and inspects the tool listing. Each tool is annotated as read-only, so the consumer can automatically allow all tool calls without prompting the user for confirmation, since the tools only read data and have no side effects.

**Why this priority**: This is the core value of the feature. Read-only annotations let consumers distinguish safe, side-effect-free tools from destructive ones, enabling frictionless auto-approval workflows.

**Independent Test**: Can be tested by connecting an MCP client, listing available tools, and verifying each tool's annotations include `readOnlyHint: true`.

**Acceptance Scenarios**:

1. **Given** the mcp-tekna server is running, **When** a consumer lists tools via the MCP protocol, **Then** every tool (`get_member_benefits`, `search_events`, `get_event_details`, `get_news`) includes annotation metadata indicating it is read-only.
2. **Given** a consumer configured to auto-approve read-only tools, **When** a tool call is made to any mcp-tekna tool, **Then** the consumer does not prompt the user for approval because the tool is annotated as read-only.

---

### User Story 2 - Tool Annotations Visible in Tool Schema (Priority: P2)

A developer integrating with the mcp-tekna server inspects the tool schema (e.g., via `tools/list` MCP method) and sees the annotations object on each tool, confirming that the tools are non-destructive.

**Why this priority**: Supports developer confidence and discoverability of the read-only property during integration.

**Independent Test**: Can be tested by calling `tools/list` on the server and inspecting the JSON response for annotation fields on each tool.

**Acceptance Scenarios**:

1. **Given** a developer queries the `tools/list` endpoint, **When** the response is returned, **Then** each tool definition includes an `annotations` object with `readOnlyHint` set to `true`.

---

### Edge Cases

- What happens if a new tool with write capabilities is added in the future? Developers must explicitly decide whether to annotate it as read-only or not; the annotation should be a conscious per-tool decision.
- What if an MCP client does not support annotations? The tools continue to function normally; annotations are supplementary metadata and do not affect tool execution.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Every tool exposed by the mcp-tekna server MUST include an MCP-compliant `annotations` object with `readOnlyHint` set to `true`.
- **FR-002**: The annotations MUST conform to the MCP specification's tool annotations schema, ensuring interoperability with any MCP-compliant consumer.
- **FR-003**: Existing tool behavior (parameters, return values, descriptions) MUST remain unchanged.
- **FR-004**: The annotations MUST be visible when a consumer calls the `tools/list` MCP method.

### Key Entities

- **Tool Annotation**: Metadata attached to an MCP tool definition that describes its behavior characteristics (e.g., read-only, destructive, idempotent). Used by consumers to make automated decisions about tool approval.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of tools (4 out of 4) report `readOnlyHint: true` in their annotations when queried via `tools/list`.
- **SC-002**: MCP consumers configured to auto-approve read-only tools can invoke all mcp-tekna tools without user confirmation prompts.
- **SC-003**: All existing tool functionality continues to work identically after annotations are added (no regressions).

## Assumptions

- The project uses FastMCP, which supports the MCP tool annotations specification including `readOnlyHint`.
- All four current tools (`get_member_benefits`, `search_events`, `get_event_details`, `get_news`) are purely read-only (they only fetch and return data, with no side effects).
- Future tools added to this server may or may not be read-only; annotations should be set per-tool at the time of creation.
