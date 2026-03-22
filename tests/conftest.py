import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


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
