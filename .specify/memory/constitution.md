<!--
Sync Impact Report
===================
- Version change: 0.0.0 → 1.0.0 (initial ratification)
- Added principles:
  - I. Test-First (NON-NEGOTIABLE)
  - II. MCP Protocol Compliance
  - III. Simplicity (YAGNI)
- Added sections:
  - Tech Stack & Constraints
  - Development Workflow
  - Error Handling
  - Governance
- Removed sections: none (initial version)
- Templates requiring updates:
  - .specify/templates/plan-template.md ✅ no changes needed (generic)
  - .specify/templates/spec-template.md ✅ no changes needed (generic)
  - .specify/templates/tasks-template.md ✅ no changes needed (generic)
- Follow-up TODOs: none
-->

# mcp-tekna Constitution

## Core Principles

### I. Test-First (NON-NEGOTIABLE)

All features MUST follow TDD discipline:

- Tests MUST be written before implementation code.
- Tests MUST fail (red) before any production code is written.
- Red-Green-Refactor cycle MUST be strictly enforced.
- Unit tests via `pytest`; integration tests for MCP tool
  contracts and external API interactions.
- Test coverage MUST NOT decrease with new changes.

### II. MCP Protocol Compliance

This server MUST strictly adhere to the Model Context Protocol
specification:

- All tools MUST define proper JSON Schema input schemas.
- Tool responses MUST use structured MCP content types
  (text, image, resource).
- Error responses MUST use MCP's `isError` flag with
  human-readable messages.
- The server MUST use FastMCP as the framework for
  tool/resource registration and transport handling.
- Resources and prompts MUST follow MCP naming conventions.

### III. Simplicity (YAGNI)

Start simple, stay simple:

- No premature abstractions. Three similar lines of code are
  better than a shared helper used once.
- No features beyond current requirements. Build for today,
  not hypothetical tomorrow.
- Minimal dependencies. Every new dependency MUST be justified.
- Flat module structure preferred over deep nesting.
- Configuration via environment variables and `.env` files only.

## Tech Stack & Constraints

- **Language**: Python >=3.10
- **MCP Framework**: FastMCP (`mcp[cli]`)
- **HTTP Client**: `httpx` for async Tekna API requests
- **Environment**: `python-dotenv` for configuration
- **Package Manager**: `uv`
- **Testing**: `pytest`, `pytest-asyncio`, `pytest-cov`
- **Linting/Formatting**: `ruff`
- **Type Checking**: `pyright`
- **Project Layout**: `src/` layout with `pyproject.toml`
- **Build System**: `setuptools` with `setuptools-scm` for
  versioning

## Development Workflow

- **Branching**: Feature branches off `main`; PRs required for
  merge.
- **Pre-commit**: `ruff` linting and formatting checks MUST
  pass before commit.
- **CI Checks**: Tests, type checking, and linting MUST pass
  before merge.
- **Commit Messages**: Conventional commits format
  (`feat:`, `fix:`, `docs:`, `test:`, `chore:`).
- **Task Management**: Use `poe` task runner for common
  operations (test, lint, format).

## Error Handling

- External API errors (Tekna) MUST be caught and returned as
  MCP error responses with `isError: true`.
- HTTP errors MUST include status code and a descriptive
  message in the MCP response.
- Network timeouts MUST use sensible defaults (30s) and
  MUST be configurable via environment variables.
- All errors MUST be logged with structured logging before
  being returned to the MCP client.
- Never expose raw tracebacks or internal details to MCP
  clients.

## Governance

- This constitution supersedes all other development practices
  for this project.
- Amendments require: (1) documented rationale, (2) version
  bump per semver rules, (3) updated `LAST_AMENDED_DATE`.
- Versioning policy: MAJOR for principle removals/redefinitions,
  MINOR for new principles/sections, PATCH for clarifications.
- All code reviews MUST verify compliance with these principles.

**Version**: 1.0.0 | **Ratified**: 2026-03-22 | **Last Amended**: 2026-03-22
