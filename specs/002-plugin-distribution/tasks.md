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

- [x] T001 Create pyproject.toml with project metadata, dependencies (mcp[cli], httpx, python-dotenv), dev dependencies (pytest, pytest-asyncio, pytest-cov, ruff, pyright, pre-commit, poethepoet), setuptools-scm config, ruff config, pytest config, and poe tasks in pyproject.toml
- [x] T002 [P] Create src/mcp_tekna/__init__.py with empty module init
- [x] T003 [P] Create src/mcp_tekna/__main__.py with `from mcp_tekna.server import main; main()` entry point
- [x] T004 Create src/mcp_tekna/server.py with minimal FastMCP server that registers one placeholder tool, supports stdio (default) and streamable-http transport via MCP_TRANSPORT env var, and defines a main() entry point
- [x] T005 [P] Create .env.example documenting all optional environment variables (MCP_TRANSPORT, MCP_HOST, MCP_PORT) in .env.example
- [x] T006 Run `uv sync` and verify `uv run mcp-tekna` starts the server without errors

**Checkpoint**: Minimal working MCP server with package metadata established

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Test infrastructure and version management that all user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 Create tests/__init__.py and tests/conftest.py with shared fixtures for loading JSON files from repo root
- [x] T008 Create scripts/bump_version.py that reads version from setuptools-scm and updates version field in .claude-plugin/plugin.json, server.json, and mcpb/manifest.json atomically in scripts/bump_version.py
- [x] T009 [P] Add poe task `bump-version` to pyproject.toml pointing to scripts/bump_version.py
- [x] T010 [P] Test that bump_version.py updates version in all manifest files consistently in tests/test_manifests.py
- [x] T011 [P] Configure pre-commit hooks for ruff format and ruff check in .pre-commit-config.yaml

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Install via Claude Code Plugin (Priority: P1) 🎯 MVP

**Goal**: Users can install mcp-tekna as a Claude Code plugin with zero configuration

**Independent Test**: Run `claude plugin add` from the repo and verify Tekna tools appear in session

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T012 [P] [US1] Test that .claude-plugin/plugin.json exists, is valid JSON, and contains all required fields (name, description, version, author, homepage, repository, license, keywords) in tests/test_manifests.py
- [x] T013 [P] [US1] Test that .claude-plugin/marketplace.json exists, is valid JSON, and contains required fields in tests/test_manifests.py
- [x] T014 [P] [US1] Test that .mcp.json exists, is valid JSON, and declares mcp-tekna server with uvx command in tests/test_manifests.py
- [x] T015 [P] [US1] Test that .mcp.dev.json exists, is valid JSON, and declares mcp-tekna server with uv run command in tests/test_manifests.py
- [x] T016 [P] [US1] Test version consistency: plugin.json version matches pyproject.toml version in tests/test_manifests.py

### Implementation for User Story 1

- [x] T017 [P] [US1] Create .claude-plugin/plugin.json with name, description, version, author (Vortiago), homepage, repository (github.com/Vortiago/mcp-tekna), license (MIT), and keywords (tekna, events, news, mcp) in .claude-plugin/plugin.json
- [x] T018 [P] [US1] Create .claude-plugin/marketplace.json with owner info and plugin metadata in .claude-plugin/marketplace.json
- [x] T019 [P] [US1] Create .mcp.json with production config: command=uvx, args=["mcp-tekna"] in .mcp.json
- [x] T020 [P] [US1] Create .mcp.dev.json with dev config: command=uv, args=["run", "mcp-tekna"] in .mcp.dev.json
- [x] T021 [US1] Run tests/test_manifests.py and verify all US1 tests pass

**Checkpoint**: Plugin manifest files complete, Claude Code installation works

---

## Phase 4: User Story 2 - Install via Claude Desktop (Priority: P2)

**Goal**: Users can install mcp-tekna in Claude Desktop via server.json config or .mcpb bundle

**Independent Test**: Add server to Claude Desktop config and verify tools appear; build .mcpb and verify it validates

### Tests for User Story 2 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T022 [P] [US2] Test that server.json exists, is valid JSON, and contains required fields (name in reverse-DNS format, description, version) in tests/test_manifests.py
- [x] T023 [P] [US2] Test that server.json packages array declares pypi registry type with uvx runtime hint and stdio transport in tests/test_manifests.py
- [x] T024 [P] [US2] Test that server.json has no required environment variables in tests/test_manifests.py
- [x] T025 [P] [US2] Test that mcpb/manifest.json exists, is valid JSON, and contains required fields (manifest_version=0.3, name, version, description, author, server) in tests/test_manifests.py
- [x] T026 [P] [US2] Test version consistency: server.json and mcpb/manifest.json versions match pyproject.toml in tests/test_manifests.py

### Implementation for User Story 2

- [x] T027 [P] [US2] Create server.json with $schema, name (io.github.Vortiago/mcp-tekna), title, version, description, repository, and packages array with pypi/uvx/stdio config in server.json
- [x] T028 [P] [US2] Create mcpb/manifest.json with manifest_version=0.3, name, version, description, author, server type=python with uv runtime, entry_point, and mcp_config in mcpb/manifest.json
- [x] T029 [P] [US2] Create mcpb/.mcpbignore excluding .git, __pycache__, .pytest_cache, .ruff_cache, tests/, specs/, .specify/, .claude/ in mcpb/.mcpbignore
- [x] T030 [US2] Run tests/test_manifests.py and verify all US2 tests pass
- [x] T031 [US2] Run `npx @anthropic-ai/mcpb validate` in mcpb/ directory and verify manifest validates

**Checkpoint**: Claude Desktop distribution files complete, .mcpb validates

---

## Phase 5: User Story 3 - Install via Docker or Remote URL (Priority: P3)

**Goal**: Users can run mcp-tekna as a Docker container with streamable-http for claude.ai connectors

**Independent Test**: Build Docker image, run container, verify streamable-http responds on port 3000

### Tests for User Story 3 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T032 [P] [US3] Test that Dockerfile exists and contains required stages (build, final) in tests/test_manifests.py
- [x] T033 [P] [US3] Test that glama.json exists, is valid JSON, and contains $schema and maintainers in tests/test_manifests.py
- [x] T034 [P] [US3] Test that server starts with MCP_TRANSPORT=streamable-http and responds on configured port in tests/test_server.py

### Implementation for User Story 3

- [x] T035 [P] [US3] Create glama.json with $schema (glama.ai schema URL) and maintainers=["Vortiago"] in glama.json
- [x] T036 [US3] Create Dockerfile with multi-stage build: base ghcr.io/astral-sh/uv:python3.12-bookworm-slim, final python:3.12-slim-bookworm, non-root user (uid 1000), default MCP_TRANSPORT=streamable-http, MCP_PORT=3000, health check in Dockerfile
- [x] T037 [US3] Create docker-compose.yml with mcp-tekna service, port 3000 mapping, health check, and restart policy in docker-compose.yml
- [x] T038 [US3] Build Docker image and verify container starts and responds to health check on port 3000
- [x] T039 [US3] Run tests/test_manifests.py and verify all US3 tests pass

**Checkpoint**: All distribution channels functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, version sync verification, and final validation

- [x] T040 [P] Add installation instructions to README.md covering all channels: Claude Code plugin, Claude Desktop (manual + .mcpb), PyPI (uvx/pip), and Docker
- [x] T041 [P] Run full test suite: `uv run pytest tests/ -v` and verify all tests pass
- [x] T042 Run version bump script and verify all manifests update atomically: `uv run poe bump-version`
- [x] T043 Verify each install command from README.md works: uvx mcp-tekna starts server, docker build succeeds, .mcp.json config is valid, mcpb validate passes

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
- T009, T010, T011 can run in parallel (Foundational phase)
- T012-T016 can all run in parallel (US1 tests)
- T017-T020 can all run in parallel (US1 implementation)
- T022-T026 can all run in parallel (US2 tests)
- T027-T029 can all run in parallel (US2 implementation)
- T032-T034 can run in parallel (US3 tests)
- T035 can run in parallel with T036 (US3 implementation)
- T040, T041 can run in parallel (Polish phase)

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T011)
3. Complete Phase 3: User Story 1 (T012-T021)
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
