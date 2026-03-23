# Tasks: Read-Only Tool Annotations

**Input**: Design documents from `/specs/005-readonly-tool-annotations/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, quickstart.md

**Tests**: Included per constitution (Test-First is NON-NEGOTIABLE).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: No setup needed — project structure and dependencies already exist. `mcp.types.ToolAnnotations` is available via the existing `mcp[cli]` dependency.

_(No tasks — skip to Phase 2)_

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: No foundational changes needed — all infrastructure is in place. The `@mcp.tool()` decorator already supports the `annotations` parameter.

_(No tasks — skip to Phase 3)_

---

## Phase 3: User Story 1 - MCP Consumer Auto-Approves Read-Only Tools (Priority: P1) MVP

**Goal**: All 4 tools expose `readOnlyHint: true` in their annotations so MCP consumers can auto-approve them.

**Independent Test**: Connect an MCP client, list tools, verify each has `annotations.readOnlyHint == True`.

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T001 [US1] Write test verifying all tools have readOnlyHint annotation in tests/test_annotations.py

### Implementation for User Story 1

- [x] T002 [P] [US1] Add ToolAnnotations import and readOnlyHint=True annotation to get_member_benefits in src/mcp_tekna/benefits.py
- [x] T003 [P] [US1] Add ToolAnnotations import and readOnlyHint=True annotations to search_events and get_event_details in src/mcp_tekna/events.py
- [x] T004 [P] [US1] Add ToolAnnotations import and readOnlyHint=True annotation to get_news in src/mcp_tekna/news.py
- [x] T005 [US1] Run tests and verify all pass: `uv run pytest tests/test_annotations.py -v`

**Checkpoint**: All 4 tools expose readOnlyHint=True. Test passes green.

---

## Phase 4: User Story 2 - Tool Annotations Visible in Tool Schema (Priority: P2)

**Goal**: Developers can inspect `tools/list` and see annotations on each tool.

**Independent Test**: Query `tools/list` and verify JSON response includes annotations objects.

_(No additional tasks — US2 is automatically satisfied by US1 implementation. The `annotations` parameter on `@mcp.tool()` is serialized in the `tools/list` response by FastMCP. Verified in research.md R1.)_

**Checkpoint**: US2 is satisfied by US1 completion.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and linting

- [x] T006 Run full test suite and linting: `uv run pytest tests/ -v && uv run ruff check .`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: Skipped — nothing to do
- **Phase 2 (Foundational)**: Skipped — nothing to do
- **Phase 3 (US1)**: T001 (test) → T002, T003, T004 (parallel implementation) → T005 (verify)
- **Phase 4 (US2)**: Satisfied by Phase 3 completion
- **Phase 5 (Polish)**: Depends on Phase 3 completion

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies — can start immediately
- **User Story 2 (P2)**: Automatically satisfied by US1

### Parallel Opportunities

- T002, T003, T004 can all run in parallel (different files, no dependencies between them)

---

## Parallel Example: User Story 1

```bash
# Step 1: Write test (must fail first - TDD red phase)
Task: T001 "Write annotation tests in tests/test_annotations.py"

# Step 2: Launch all implementation tasks in parallel (TDD green phase)
Task: T002 "Add annotations to benefits.py"
Task: T003 "Add annotations to events.py"
Task: T004 "Add annotations to news.py"

# Step 3: Verify
Task: T005 "Run tests - all should pass"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Write test (T001) — verify it fails (red)
2. Implement annotations in all 3 files (T002-T004) — in parallel
3. Run tests (T005) — verify all pass (green)
4. Run full suite + lint (T006) — no regressions

### Total: 6 tasks, ~10 lines of code changed

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story
- US2 requires no separate implementation — it's inherently satisfied by FastMCP's `tools/list` serialization
- Constitution mandates TDD: T001 MUST fail before T002-T004 are implemented
- Commit after T005 passes (all annotations in place, tests green)
