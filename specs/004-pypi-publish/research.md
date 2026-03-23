# Research: Publish to PyPI

**Feature**: 004-pypi-publish | **Date**: 2026-03-23

## R1: PyPI Trusted Publishing (OIDC)

**Decision**: Use GitHub OIDC trusted publishing — no API tokens.

**Rationale**: PyPI's recommended approach since 2023. Eliminates secret management, rotation, and leak risk. The `pypa/gh-action-pypi-publish` action handles the OIDC token exchange automatically.

**Alternatives considered**:
- API token in GitHub secrets: Works but requires manual token creation, rotation, and carries leak risk.
- Manual `twine upload`: Defeats the automation goal entirely.

**Setup requirement**: One-time manual configuration on pypi.org — add a "trusted publisher" for the GitHub repository, workflow file, and environment name.

## R2: setuptools-scm Version Strategy

**Decision**: Use `setuptools-scm>=8` with `local_scheme = "no-local-version"` for PyPI-clean versions.

**Rationale**: Already configured in `pyproject.toml` (setuptools-scm is a build dependency). Adding `local_scheme = "no-local-version"` prevents `+g<hash>` suffixes that PyPI rejects. The `fallback_version = "0.1.0"` is already set for builds without git history.

**Alternatives considered**:
- Manual version in `__init__.py`: Requires remembering to bump; error-prone. Against single-source-of-truth principle.
- `hatch-vcs` / `pdm-backend`: Would require migrating build system. Unnecessary since setuptools-scm is already in place.

## R3: CI Workflow Structure

**Decision**: Two separate workflow files — `ci.yml` (quality gates) and `publish-pypi.yml` (build + publish).

**Rationale**: Separation of concerns. CI runs on every push/PR. Publish runs only on tags. Matches mcp-outline's proven pattern. The publish workflow does NOT depend on the CI workflow completing (they trigger on different events), but branch protection rules ensure CI must pass before merging to main, which is where tags are created.

**Alternatives considered**:
- Single workflow with conditional jobs: More complex, harder to maintain, mixes concerns.
- Reusable workflow: Overkill for a single project.

## R4: TestPyPI for Release Candidates

**Decision**: RC tags (`v*-rc*`) publish to TestPyPI only; stable tags publish to PyPI only.

**Rationale**: TestPyPI serves as a staging environment. RC packages can be tested with `pip install --index-url https://test.pypi.org/simple/ mcp-tekna`. Keeps the real PyPI index clean.

**Implementation**: The publish workflow uses an `if` condition on the job: `contains(github.ref, '-rc')` for TestPyPI, negated for PyPI.

## R5: GitHub Release Creation

**Decision**: Create a GitHub Release with auto-generated notes on every version tag push.

**Rationale**: Provides a changelog page, notification to watchers, and a canonical place to document what changed. Uses `gh release create` with `--generate-notes` which produces a diff-based changelog from conventional commits.

**Implementation**: Can be a separate job in `publish-pypi.yml` or a third workflow file. Including it in `publish-pypi.yml` keeps tag-triggered actions together.

## R6: GitHub Actions Action Versions

**Decision**: Pin actions to full commit SHAs for security, with version comments.

**Rationale**: Tag-based references (e.g., `@v6`) can be force-pushed by action maintainers. SHA pinning prevents supply chain attacks. Matches mcp-outline's practice.

**Key actions and their current SHAs** (from mcp-outline, to be verified at implementation time):
- `actions/checkout` — v6
- `actions/setup-python` — v6
- `actions/upload-artifact` — v7
- `actions/download-artifact` — v8
- `pypa/gh-action-pypi-publish` — release/v1
- `astral-sh/setup-uv` — v7
