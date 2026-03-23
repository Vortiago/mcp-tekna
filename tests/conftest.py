import json
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture()
def repo_root() -> Path:
    return REPO_ROOT


def load_json(path: Path) -> dict:
    """Load and parse a JSON file relative to the repo root."""
    full = REPO_ROOT / path
    assert full.exists(), f"File not found: {full}"
    return json.loads(full.read_text(encoding="utf-8"))


@pytest.fixture()
def pyproject() -> dict:
    """Load pyproject.toml as a dict."""
    try:
        import tomllib
    except ModuleNotFoundError:
        import tomli as tomllib  # type: ignore[no-redef]

    path = REPO_ROOT / "pyproject.toml"
    return tomllib.loads(path.read_text(encoding="utf-8"))


def load_fixture(name: str) -> str:
    """Load a test fixture file as text."""
    path = FIXTURES_DIR / name
    assert path.exists(), f"Fixture not found: {path}"
    return path.read_text(encoding="utf-8")


def load_fixture_json(name: str) -> dict[str, Any]:
    """Load a test fixture file as parsed JSON."""
    return json.loads(load_fixture(name))


@pytest.fixture()
def events_response() -> dict[str, Any]:
    """Sample events API response."""
    return load_fixture_json("events_response.json")


@pytest.fixture()
def news_response() -> dict[str, Any]:
    """Sample news API response."""
    return load_fixture_json("news_response.json")


@pytest.fixture()
def benefits_html() -> str:
    """Sample member benefits page HTML."""
    return load_fixture("benefits_page.html")
