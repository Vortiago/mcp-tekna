# Data Model: Publish to PyPI

**Feature**: 004-pypi-publish | **Date**: 2026-03-23

This feature is CI/CD infrastructure — no application data model changes. The entities below describe the configuration and artifacts involved.

## Entities

### Version Tag

A git annotated tag that triggers the publishing pipeline.

- **Pattern (stable)**: `vX.Y.Z` (e.g., `v1.0.0`, `v0.2.1`)
- **Pattern (RC)**: `vX.Y.Z-rc.N` (e.g., `v1.0.0-rc.1`)
- **Source of truth**: Git repository tags
- **Lifecycle**: Created manually by maintainer → triggers CI → consumed by setuptools-scm for version calculation

### Package Artifact

Built distribution files uploaded to PyPI/TestPyPI.

- **Wheel**: `mcp_tekna-X.Y.Z-py3-none-any.whl` (pure Python, no platform-specific code)
- **Sdist**: `mcp_tekna-X.Y.Z.tar.gz`
- **Built by**: `python -m build` in CI
- **Stored as**: GitHub Actions artifact (ephemeral) → published to PyPI/TestPyPI (permanent)

### GitHub Environment

GitHub Actions deployment environments used for OIDC scoping.

- **`pypi`**: Used by the PyPI publish job. Maps to the trusted publisher configured on pypi.org.
- **`testpypi`**: Used by the TestPyPI publish job. Maps to the trusted publisher configured on test.pypi.org.

### Workflow Files

- **`ci.yml`**: Triggers on push/PR. Runs lint, type check, tests.
- **`publish-pypi.yml`**: Triggers on `v*` tags. Builds, publishes, creates GitHub Release.
