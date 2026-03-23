# Quickstart: Publish to PyPI

**Feature**: 004-pypi-publish | **Date**: 2026-03-23

## Prerequisites

1. GitHub repository with Actions enabled
2. PyPI account with trusted publisher configured for this repo
3. TestPyPI account with trusted publisher configured (for RC testing)

## One-Time Setup (Manual on PyPI)

1. Go to https://pypi.org/manage/account/publishing/
2. Add a new pending publisher:
   - **PyPI project name**: `mcp-tekna`
   - **Owner**: `Vortiago`
   - **Repository**: `mcp-tekna`
   - **Workflow name**: `publish-pypi.yml`
   - **Environment name**: `pypi`
3. Repeat on https://test.pypi.org with environment name `testpypi`

## Release Workflow

### Stable Release

```bash
# Ensure you're on main with all changes merged
git checkout main
git pull

# Create and push a version tag
git tag -a v0.1.0 -m "Initial PyPI release"
git push origin v0.1.0
```

CI will automatically:
1. Build the wheel and sdist
2. Publish to PyPI
3. Create a GitHub Release with auto-generated notes

### Release Candidate

```bash
git tag -a v0.2.0-rc.1 -m "Release candidate for 0.2.0"
git push origin v0.2.0-rc.1
```

CI will publish to TestPyPI only. Test with:

```bash
pip install --index-url https://test.pypi.org/simple/ mcp-tekna
```

## Local Build (for verification)

```bash
uv run python -m build
ls dist/
# mcp_tekna-0.1.0.dev1+g<hash>.tar.gz
# mcp_tekna-0.1.0.dev1+g<hash>-py3-none-any.whl
```

## Version Bump Convention

Check commits since last tag to determine version bump:
- `feat!:` or `BREAKING CHANGE:` → **major** bump
- `feat:` → **minor** bump
- `fix:` only → **patch** bump
