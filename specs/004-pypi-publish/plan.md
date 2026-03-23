# Implementation Plan: Publish to PyPI

**Branch**: `004-pypi-publish` | **Date**: 2026-03-23 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/004-pypi-publish/spec.md`

## Summary

Automate package publishing to PyPI via GitHub Actions triggered by git tags. Uses setuptools-scm for version derivation, PyPI trusted publishing (OIDC) for authentication, and includes CI quality gates (ruff, pyright, pytest on Python 3.10 + 3.13). Release candidate tags (`v*-rc*`) publish to TestPyPI only. All version tags create a GitHub Release with auto-generated notes.

## Technical Context

**Language/Version**: Python >=3.10
**Primary Dependencies**: `setuptools>=75`, `setuptools-scm>=8`, `build` (CI only)
**Storage**: N/A
**Testing**: `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-httpx` via `uv`
**Target Platform**: GitHub Actions (Ubuntu latest) for CI; PyPI/TestPyPI for distribution
**Project Type**: MCP server (CLI tool distributed via PyPI)
**Performance Goals**: N/A (CI pipeline — publish within 5 minutes of tag push)
**Constraints**: PyPI trusted publishing requires OIDC; setuptools-scm needs full git history
**Scale/Scope**: Single package, single maintainer, ~10 source files

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Test-First (NON-NEGOTIABLE) | PASS | CI workflow enforces tests before publish. No application code changes in this feature — only CI/config files. |
| II. MCP Protocol Compliance | N/A | This feature is infrastructure/CI only — no MCP tool or protocol changes. |
| III. Simplicity (YAGNI) | PASS | Follows proven pattern from mcp-outline. No unnecessary abstractions. Two workflow files + one config change. |

No violations. Gate passes.

## Project Structure

### Documentation (this feature)

```text
specs/004-pypi-publish/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
.github/
└── workflows/
    ├── ci.yml               # NEW: Lint, type check, test on push/PR
    └── publish-pypi.yml     # NEW: Build + publish on tag push

pyproject.toml               # MODIFY: Add local_scheme = "no-local-version"
```

**Structure Decision**: This feature adds only CI/CD configuration files at the repository root. No changes to `src/` or `tests/`. The two GitHub Actions workflows follow the same split pattern used in mcp-outline (separate CI and publish workflows).
