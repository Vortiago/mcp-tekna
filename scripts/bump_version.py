"""Sync version from setuptools-scm into all distribution manifest files."""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

MANIFEST_FILES = [
    REPO_ROOT / ".claude-plugin" / "plugin.json",
    REPO_ROOT / "server.json",
    REPO_ROOT / "mcpb" / "manifest.json",
]


def get_version() -> str:
    """Get the current version from setuptools-scm."""
    from setuptools_scm import get_version  # type: ignore[import-untyped]

    return get_version(root=str(REPO_ROOT))


def update_manifest(path: Path, version: str) -> bool:
    """Update the version field in a JSON manifest. Returns True if updated."""
    if not path.exists():
        print(f"  SKIP {path.relative_to(REPO_ROOT)} (not found)")
        return False

    data = json.loads(path.read_text(encoding="utf-8"))
    old = data.get("version")
    data["version"] = version
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"  {path.relative_to(REPO_ROOT)}: {old} -> {version}")
    return True


def main() -> None:
    version = get_version()
    print(f"Version from setuptools-scm: {version}")
    print("Updating manifests:")

    updated = 0
    for path in MANIFEST_FILES:
        if update_manifest(path, version):
            updated += 1

    if updated == 0:
        print("No manifest files found to update.")
        sys.exit(1)

    print(f"Done. Updated {updated} file(s).")


if __name__ == "__main__":
    main()
