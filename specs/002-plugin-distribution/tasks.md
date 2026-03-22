# Tasks: Plugin & Distribution Packaging

**Input**: Design documents from `/specs/002-plugin-distribution/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Included per constitution principle I (Test-First). Manifest validation tests verify JSON schemas and version consistency.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, package metadata, and minimal server entry point

- [ ] T001 Create pyproject.toml with project metadata, dependencies (mcp[cli], httpx, python-dotenv), dev dependencies (pytest, pytest-asyncio, pytest-cov, ruff, pyright, pre-commit, poethepoet), setuptools-scm config, ruff config, pytest config, and poe tasks in pyproject.toml
- [ ] T002 [P] Create src/mcp_tekna/__init__.py with empty module init
- [ ] T003 [P] Create src/mcp_tekna/__main__.py with `from mcp_tekna.server import main; main()` entry point
- [ ] T004 Create src/mcp_tekna/server.py with minimal FastMCP server that registers one placeholder tool, supports stdio (default) and streamable-http transport via MCP_TRANSPORT env var, and defines a main() entry point
- [ ] T005 [P] Create .env.example documenting all optional environment variables (MCP_TRANSPORT, MCP_HOST, MCP_PORT) in .env.example
- [ ] T006 Run `uv sync` and verify `uv run mcp-tekna` starts the server without errors

**Checkpoint**: Minimal working MCP server with package metadata established

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Test infrastructure and version management that all user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T007 Create tests/__init__.py and tests/conftest.py with shared fixtures for loading JSON files from repo root
- [ ] T008 Create scripts/bump_version.py that reads version from setuptools-scm and updates version field in .claude-plugin/plugin.json, server.json, and mcpb/manifest.json atomically in scripts/bump_version.py
- [ ] T009 [P] Add poe task `bump-version` to pyproject.toml pointing to scripts/bump_version.py
- [ ] T010 [P] Configure pre-commit hooks for ruff format and ruff check in .pre-commit-config.yaml

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Install via Claude Code Plugin (Priority: P1) 🎯 MVP

**Goal**: Users can install mcp-tekna as a Claude Code plugin with zero configuration

**Independent Test**: Run `claude plugin add` from the repo and verify Tekna tools appear in session

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T011 [P] [US1] Test that .claude-plugin/plugin.json exists, is valid JSON, and contains all required fields (name, description, version, author, homepage, repository, license, keywords) in tests/test_manifests.py
- [ ] T012 [P] [US1] Test that .claude-plugin/marketplace.json exists, is valid JSON, and contains required fields in tests/test_manifests.py
- [ ] T013 [P] [US1] Test that .mcp.json exists, is valid JSON, and declares mcp-tekna server with uvx command in tests/test_manifests.py
- [ ] T014 [P] [US1] Test that .mcp.dev.json exists, is valid JSON, and declares mcp-tekna server with uv run command in tests/test_manifests.py
- [ ] T015 [P] [US1] Test version consistency: plugin.json version matches pyproject.toml version in tests/test_manifests.py

### Implementation for User Story 1

- [ ] T016 [P] [US1] Create .claude-plugin/plugin.json with name, description, version, author (Vortiago), homepage, repository (github.com/Vortiago/mcp-tekna), license (MIT), and keywords (tekna, events, news, mcp) in .claude-plugin/plugin.json
- [ ] T017 [P] [US1] Create .claude-plugin/marketplace.json with owner info and plugin metadata in .claude-plugin/marketplace.json
- [ ] T018 [P] [US1] Create .mcp.json with production config: command=uvx, args=["mcp-tekna"] in .mcp.json
- [ ] T019 [P] [US1] Create .mcp.dev.json with dev config: command=uv, args=["run", "mcp-tekna"] in .mcp.dev.json
- [ ] T020 [US1] Run tests/test_manifests.py and verify all US1 tests pass

**Checkpoint**: Plugin manifest files complete, Claude Code installation works

---

## Phase 4: User Story 2 - Install via Claude Desktop (Priority: P2)

**Goal**: Users can install mcp-tekna in Claude Desktop via server.json config or .mcpb bundle

**Independent Test**: Add server to Claude Desktop config and verify tools appear; build .mcpb and verify it validates

### Tests for User Story 2 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T021 [P] [US2] Test that server.json exists, is valid JSON, and contains required fields (name in reverse-DNS format, description, version) in tests/test_manifests.py
- [ ] T022 [P] [US2] Test that server.json packages array declares pypi registry type with uvx runtime hint and stdio transport in tests/test_manifests.py
- [ ] T023 [P] [US2] Test that server.json has no required environment variables in tests/test_manifests.py
- [ ] T024 [P] [US2] Test that mcpb/manifest.json exists, is valid JSON, and contains required fields (manifest_version=0.3, name, version, description, author, server) in tests/test_manifests.py
- [ ] T025 [P] [US2] Test version consistency: server.json and mcpb/manifest.json versions match pyproject.toml in tests/test_manifests.py

### Implementation for User Story 2

- [ ] T026 [P] [US2] Create server.json with $schema, name (io.github.Vortiago/mcp-tekna), title, version, description, repository, and packages array with pypi/uvx/stdio config in server.json
- [ ] T027 [P] [US2] Create mcpb/manifest.json with manifest_version=0.3, name, version, description, author, server type=python with uv runtime, entry_point, and mcp_config in mcpb/manifest.json
- [ ] T028 [P] [US2] Create mcpb/.mcpbignore excluding .git, __pycache__, .pytest_cache, .ruff_cache, tests/, specs/, .specify/, .claude/ in mcpb/.mcpbignore
- [ ] T029 [US2] Run tests/test_manifests.py and verify all US2 tests pass
- [ ] T030 [US2] Run `npx @anthropic-ai/mcpb validate` in mcpb/ directory and verify manifest validates

**Checkpoint**: Claude Desktop distribution files complete, .mcpb validates

---

## Phase 5: User Story 3 - Install via Docker or Remote URL (Priority: P3)

**Goal**: Users can run mcp-tekna as a Docker container with streamable-http for claude.ai connectors

**Independent Test**: Build Docker image, run container, verify streamable-http responds on port 3000

### Tests for User Story 3 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T031 [P] [US3] Test that Dockerfile exists and contains required stages (build, final) in tests/test_manifests.py
- [ ] T032 [P] [US3] Test that glama.json exists, is valid JSON, and contains $schema and maintainers in tests/test_manifests.py

### Implementation for User Story 3

- [ ] T033 [P] [US3] Create glama.json with $schema (glama.ai schema URL) and maintainers=["Vortiago"] in glama.json
- [ ] T034 [US3] Create Dockerfile with multi-stage build: base ghcr.io/astral-sh/uv:python3.12-bookworm-slim, final python:3.12-slim-bookworm, non-root user (uid 1000), default MCP_TRANSPORT=streamable-http, MCP_PORT=3000, health check in Dockerfile
- [ ] T035 [US3] Create docker-compose.yml with mcp-tekna service, port 3000 mapping, health check, and restart policy in docker-compose.yml
- [ ] T036 [US3] Build Docker image and verify container starts and responds to health check on port 3000
- [ ] T037 [US3] Run tests/test_manifests.py and verify all US3 tests pass

**Checkpoint**: All distribution channels functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, version sync verification, and final validation

- [ ] T038 [P] Add installation instructions to README.md covering all channels: Claude Code plugin, Claude Desktop (manual + .mcpb), PyPI (uvx/pip), and Docker
- [ ] T039 [P] Run full test suite: `uv run pytest tests/ -v` and verify all tests pass
- [ ] T040 Run version bump script and verify all manifests update atomically: `uv run poe bump-version`
- [ ] T041 Run quickstart.md validation: verify each documented command works

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on US1
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on US1/US2

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- All test tasks marked [P] can run in parallel
- All implementation tasks creating independent files marked [P] can run in parallel
- Verification task runs last in each story

### Parallel Opportunities

- T002, T003, T005 can run in parallel (Setup phase)
- T009, T010 can run in parallel (Foundational phase)
- T011-T015 can all run in parallel (US1 tests)
- T016-T019 can all run in parallel (US1 implementation)
- T021-T025 can all run in parallel (US2 tests)
- T026-T028 can all run in parallel (US2 implementation)
- T031-T032 can run in parallel (US3 tests)
- T033 can run in parallel with T034 (US3 implementation)
- T038, T039 can run in parallel (Polish phase)

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T010)
3. Complete Phase 3: User Story 1 (T011-T020)
4. **STOP and VALIDATE**: Install plugin in Claude Code, verify tools work
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test plugin install → MVP!
3. Add User Story 2 → Test Claude Desktop → server.json + .mcpb ready
4. Add User Story 3 → Test Docker → All channels complete
5. Polish → Documentation + final validation

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Tests MUST fail before implementing (constitution principle I)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
