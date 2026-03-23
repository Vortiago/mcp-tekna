# mcp-tekna Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-03-23

## Active Technologies
- Python >=3.10 + `setuptools>=75`, `setuptools-scm>=8`, `build` (CI only) (004-pypi-publish)

- Python >=3.10 + `mcp[cli]` (FastMCP), `httpx`, `python-dotenv` (002-plugin-distribution)
- Python >=3.10 + `cachetools`, `beautifulsoup4`, `pytest-httpx` (001-tekna-data-tools)

## Project Structure

```text
src/
tests/
```

## Commands

uv run pytest tests/ -v; uv run ruff check .

## Code Style

Python >=3.10: Follow standard conventions

## Recent Changes
- 004-pypi-publish: Added Python >=3.10 + `setuptools>=75`, `setuptools-scm>=8`, `build` (CI only)

- 002-plugin-distribution: Added Python >=3.10 + `mcp[cli]` (FastMCP), `httpx`, `python-dotenv`
- 001-tekna-data-tools: Adding `cachetools`, `beautifulsoup4` for data tools

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
