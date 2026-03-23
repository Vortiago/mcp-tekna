# Tasks: Publish to PyPI

**Input**: Design documents from `/specs/004-pypi-publish/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: Not applicable — this feature creates CI/CD workflow files (YAML) and config changes. The workflows themselves ARE the test infrastructure. Verification is done by building locally and validating workflow syntax.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: Create directory structure for GitHub Actions workflows

- [x] T001 Create `.github/workflows/` directory structure

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Configure setuptools-scm for PyPI-compatible versioning — required by US1 and US3

- [x] T002 Add `local_scheme = "no-local-version"` to `[tool.setuptools_scm]` in `pyproject.toml`
- [x] T003 Verify local build produces clean version by running `uv run python -m build` and inspecting dist/ artifact names

**Checkpoint**: `pyproject.toml` produces PyPI-compatible versions. Build artifacts have no `+g<hash>` suffix.

---

## Phase 3: User Story 3 - Version Derived from Git Tags (Priority: P1) 🎯 MVP

**Goal**: Package version is automatically derived from git tags via setuptools-scm with no hardcoded version in source code.

**Independent Test**: Tag a commit locally, run `python -m build`, verify the artifact version matches the tag.

### Implementation for User Story 3

- [x] T004 [US3] Verify `pyproject.toml` has `dynamic = ["version"]` and `setuptools-scm>=8` in build-requires (already present — confirm no regressions)
- [x] T005 [US3] Verify `fallback_version` is set in `[tool.setuptools_scm]` in `pyproject.toml` for builds without git history
- [x] T006 [US3] Test version derivation: create a local tag, run `uv run python -m build`, confirm artifact version matches tag

**Checkpoint**: Version derivation from git tags works locally. setuptools-scm config is complete and verified.

---

## Phase 4: User Story 1 - Publish a Release to PyPI (Priority: P1)

**Goal**: Pushing a `v*` tag triggers a GitHub Actions workflow that builds and publishes the package to PyPI using trusted publishing (OIDC), and creates a GitHub Release.

**Independent Test**: Push a version tag and verify the workflow runs, publishes to PyPI, and creates a GitHub Release.

### Implementation for User Story 1

- [x] T007 [US1] Create build job in `.github/workflows/publish-pypi.yml`: checkout with full history, setup Python 3.10, install build, run `python -m build`, upload artifacts
- [x] T008 [US1] Create publish-to-pypi job in `.github/workflows/publish-pypi.yml`: download artifacts, use `pypa/gh-action-pypi-publish` with trusted publishing (OIDC), configure `pypi` environment
- [x] T009 [US1] Create create-release job in `.github/workflows/publish-pypi.yml`: use `gh release create` with `--generate-notes` to auto-generate release notes
- [x] T010 [US1] Configure workflow trigger on `push: tags: ['v*']` and set top-level `permissions: {}` with per-job permissions in `.github/workflows/publish-pypi.yml`
- [x] T011 [US1] Add condition to publish-to-pypi job to skip RC tags: `if: "!contains(github.ref, '-rc')"` in `.github/workflows/publish-pypi.yml`
- [x] T012 [US1] Validate workflow YAML syntax by running `python -c "import yaml; yaml.safe_load(open('.github/workflows/publish-pypi.yml'))"` or equivalent

**Checkpoint**: `publish-pypi.yml` is complete with build, publish, and release jobs. RC tags are excluded from PyPI publish.

---

## Phase 5: User Story 4 - CI Quality Gates (Priority: P2)

**Goal**: Every push and PR runs linting (ruff), type checking (pyright), and tests (pytest) against Python 3.10 and 3.13.

**Independent Test**: Push a commit or open a PR and verify all checks run and report status.

### Implementation for User Story 4

- [x] T013 [P] [US4] Create `.github/workflows/ci.yml` with trigger on `push: branches: ['**']` and `pull_request: branches: [main]`
- [x] T014 [US4] Add Python version matrix (`["3.10", "3.13"]`) with `fail-fast: false` strategy in `.github/workflows/ci.yml`
- [x] T015 [US4] Add job steps: checkout, setup-python, setup-uv with cache, `uv sync --group dev` in `.github/workflows/ci.yml`
- [x] T016 [US4] Add quality check steps: `uv run ruff format --check .`, `uv run ruff check .`, `uv run pyright src/` in `.github/workflows/ci.yml`
- [x] T017 [US4] Add test step: `uv run pytest tests/ -v --cov=src/mcp_tekna --cov-report=term` in `.github/workflows/ci.yml`
- [x] T018 [US4] Validate workflow YAML syntax for `.github/workflows/ci.yml`

**Checkpoint**: `ci.yml` runs lint, type check, and tests on Python 3.10 + 3.13 for every push/PR.

---

## Phase 6: User Story 2 - TestPyPI for Release Candidates (Priority: P2)

**Goal**: RC tags (`v*-rc*`) publish to TestPyPI only, allowing pre-release testing before promoting to a stable release.

**Independent Test**: Push an RC tag and verify the package appears on TestPyPI and is installable.

### Implementation for User Story 2

- [x] T019 [US2] Add publish-to-testpypi job in `.github/workflows/publish-pypi.yml`: condition `if: contains(github.ref, '-rc')`, `testpypi` environment, `repository-url: https://test.pypi.org/legacy/`
- [x] T020 [US2] Verify RC tag condition is mutually exclusive with PyPI publish job (RC → TestPyPI only, stable → PyPI only) in `.github/workflows/publish-pypi.yml`

**Checkpoint**: RC tags publish to TestPyPI only. Stable tags publish to PyPI only. No overlap.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final verification and documentation

- [x] T021 Pin all GitHub Actions to commit SHAs (not tags) with version comments in `.github/workflows/publish-pypi.yml` and `.github/workflows/ci.yml`
- [x] T022 Run full local build (`uv run python -m build`) and verify wheel + sdist are produced in `dist/`
- [x] T023 Run existing test suite (`uv run pytest tests/ -v`) to verify no regressions from `pyproject.toml` changes
- [x] T024 Validate quickstart.md instructions match the implemented workflow

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup — BLOCKS all user stories
- **US3 (Phase 3)**: Depends on Foundational — verifies version config
- **US1 (Phase 4)**: Depends on Foundational — can run in parallel with US3 after T002-T003
- **US4 (Phase 5)**: Depends on Setup only — can run in parallel with US1/US3
- **US2 (Phase 6)**: Depends on US1 (extends the same workflow file)
- **Polish (Phase 7)**: Depends on all user stories complete

### User Story Dependencies

- **US3 (P1)**: After Foundational — no dependencies on other stories
- **US1 (P1)**: After Foundational — no dependencies on other stories (but benefits from US3 verification)
- **US4 (P2)**: After Setup — independent of all other stories (different workflow file)
- **US2 (P2)**: After US1 — adds a job to the same `publish-pypi.yml` workflow

### Parallel Opportunities

- **US1 and US4** can be implemented in parallel (different workflow files)
- **US3 verification** can happen while US1 is being built
- **T013-T018 (US4)** are in a separate file from T007-T012 (US1)

---

## Parallel Example: US1 + US4

```text
# These can run in parallel (different files):
Task: "Create publish workflow in .github/workflows/publish-pypi.yml" (US1)
Task: "Create CI workflow in .github/workflows/ci.yml" (US4)
```

---

## Implementation Strategy

### MVP First (US3 + US1)

1. Complete Phase 1: Setup (create directory)
2. Complete Phase 2: Foundational (pyproject.toml fix + verify build)
3. Complete Phase 3: US3 (verify version derivation)
4. Complete Phase 4: US1 (publish workflow)
5. **STOP and VALIDATE**: Push a tag and verify PyPI publish + GitHub Release
6. Deploy MVP — package is now installable from PyPI

### Incremental Delivery

1. Setup + Foundational + US3 + US1 → MVP: publish to PyPI works
2. Add US4 → CI quality gates on every push/PR
3. Add US2 → RC testing via TestPyPI
4. Polish → SHA pinning, final verification

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- This feature has no application code changes — only CI/CD config and one `pyproject.toml` tweak
- One-time manual setup required on pypi.org and test.pypi.org (trusted publisher config) — not a task, documented in quickstart.md
- Action SHAs should be sourced from the mcp-outline reference implementation at implementation time
