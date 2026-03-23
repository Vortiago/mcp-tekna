# Feature Specification: Publish to PyPI

**Feature Branch**: `004-pypi-publish`
**Created**: 2026-03-23
**Status**: Draft
**Input**: User description: "Let's make a 'publish to pypi' spec and prepare it for this. We can look at mcp-outline to see how I did it there"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Publish a Release to PyPI (Priority: P1)

As a maintainer, I want to publish a new version of mcp-tekna to PyPI by tagging a commit, so that users can install it via `pip install mcp-tekna` or `uvx mcp-tekna` without any manual build or upload steps.

**Why this priority**: This is the core value — making the package installable from PyPI. Without this, no distribution is possible.

**Independent Test**: Can be fully tested by pushing a version tag (e.g., `v0.1.0`) and verifying the package appears on PyPI and is installable via `pip install mcp-tekna`.

**Acceptance Scenarios**:

1. **Given** a commit on main is tagged with `v0.1.0`, **When** the tag is pushed to GitHub, **Then** a CI workflow builds the package and publishes it to PyPI using trusted publishing (OIDC).
2. **Given** a tag push triggers the publish workflow, **When** the build completes, **Then** both a wheel and sdist are uploaded to PyPI.
3. **Given** the package is published, **When** a user runs `pip install mcp-tekna`, **Then** the correct version is installed with all dependencies.

---

### User Story 2 - Test a Release Candidate on TestPyPI (Priority: P2)

As a maintainer, I want to publish release candidates to TestPyPI before making an official release, so I can verify the package installs correctly without polluting the real PyPI index.

**Why this priority**: Prevents broken releases from reaching users. Important for quality but not strictly required for distribution.

**Independent Test**: Can be tested by pushing a tag like `v0.2.0-rc.1` and verifying it appears on TestPyPI and installs correctly.

**Acceptance Scenarios**:

1. **Given** a commit is tagged with a release candidate tag (e.g., `v0.2.0-rc.1`), **When** the tag is pushed, **Then** the package is published to TestPyPI only (not to PyPI).
2. **Given** a package is on TestPyPI, **When** a user installs from TestPyPI, **Then** the package installs and works correctly.

---

### User Story 3 - Version Derived from Git Tags (Priority: P1)

As a maintainer, I want the package version to be automatically derived from git tags using setuptools-scm, so there is a single source of truth for versioning and no manual version bumps in code.

**Why this priority**: Ensures version consistency across the package, PyPI, and git history. Essential for reliable releases.

**Independent Test**: Can be tested by tagging a commit and running `python -m build`, then inspecting the built artifact version.

**Acceptance Scenarios**:

1. **Given** a git tag `v1.2.3` exists, **When** the package is built, **Then** the package version is `1.2.3`.
2. **Given** no git tag exists on the current commit, **When** the package is built locally, **Then** a development version is generated and the fallback version is used appropriately.
3. **Given** a package is built for PyPI, **When** the version is calculated, **Then** no local version identifiers (e.g., `+g<hash>`) are included (PyPI-clean versions only).

---

### User Story 4 - CI Quality Gates Before Publishing (Priority: P2)

As a maintainer, I want the CI pipeline to run linting, type checking, and tests before any release is published, so that broken code never reaches PyPI.

**Why this priority**: Prevents publishing broken packages. Important quality gate but can initially be enforced manually.

**Independent Test**: Can be tested by pushing a tag on a branch with failing tests and verifying the publish step is skipped or blocked.

**Acceptance Scenarios**:

1. **Given** a CI workflow exists, **When** code is pushed or a PR is opened, **Then** ruff linting, pyright type checking, and pytest tests all run.
2. **Given** any CI check fails, **When** the publish workflow runs, **Then** the publish step does not execute.

---

### Edge Cases

- What happens when a tag is pushed that doesn't match the `v*` pattern? The publish workflow should not trigger.
- What happens when a tag is pushed on a non-main branch? The workflow should still trigger (tags are branch-independent in git).
- What happens if PyPI trusted publishing is not configured? The workflow fails with a clear authentication error.
- What happens if the same version tag is pushed twice? PyPI rejects duplicate versions; the workflow should fail gracefully.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The project MUST have a CI workflow that triggers on version tag pushes (`v*`) and publishes the package to PyPI.
- **FR-002**: The publish workflow MUST use PyPI trusted publishing (OIDC) — no API tokens stored as secrets.
- **FR-003**: The build step MUST produce both a wheel (`.whl`) and source distribution (`.tar.gz`).
- **FR-004**: The package version MUST be derived from git tags via setuptools-scm with no hardcoded version in source code.
- **FR-005**: The setuptools-scm configuration MUST produce PyPI-compatible version strings (no local version identifiers).
- **FR-006**: Tags matching a release candidate pattern (e.g., `v*-rc*`) MUST trigger publishing to TestPyPI only (not to PyPI).
- **FR-007**: A CI workflow MUST run linting (ruff), type checking (pyright), and tests (pytest) on pushes and pull requests, testing against Python 3.10 and 3.13 (minimum supported + latest).
- **FR-008**: The project MUST be buildable locally via standard Python build tools.
- **FR-009**: The publish workflow MUST create a GitHub Release with auto-generated release notes when a version tag is pushed.

### Key Entities

- **Version Tag**: A git tag following the pattern `vX.Y.Z` (release) or `vX.Y.Z-rc.N` (release candidate) that triggers the publishing pipeline.
- **Package Artifact**: The built wheel and sdist files uploaded to PyPI/TestPyPI.
- **Trusted Publisher**: The OIDC identity configured on PyPI to allow passwordless publishing from the repository's CI.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A maintainer can publish a new release by creating and pushing a single git tag — no other manual steps required.
- **SC-002**: 100% of published versions are traceable to a specific git tag and commit.
- **SC-003**: Users can install the package via `pip install mcp-tekna` within 5 minutes of a successful tag push.
- **SC-004**: Release candidates can be tested from TestPyPI before promoting to an official release.
- **SC-005**: No release is published without passing all automated quality checks (lint, type check, tests).

## Clarifications

### Session 2026-03-23

- Q: Should RC tags publish to TestPyPI only, or both TestPyPI and PyPI? → A: TestPyPI only (RC tags never go to real PyPI).
- Q: Should the workflow also create a GitHub Release with auto-generated notes? → A: Yes, create a GitHub Release on each version tag.
- Q: Which Python versions should CI test against? → A: 3.10 and 3.13 (min + latest).

## Assumptions

- The GitHub repository is public (or has GitHub Actions enabled).
- PyPI trusted publishing will be configured on pypi.org for this repository (one-time manual setup on PyPI).
- The existing `pyproject.toml` already uses setuptools-scm for dynamic versioning (confirmed — already in place).
- Semantic versioning (semver) is followed for all releases.
- The `uv` tool is available in CI for dependency management and running tasks.
