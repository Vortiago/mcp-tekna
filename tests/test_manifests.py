"""Manifest validation tests for all distribution channels.

Tests are organized by user story. All tests load files from repo root
using the conftest helpers.
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def load_json(path: Path) -> dict:
    """Load and parse a JSON file relative to the repo root."""
    full = REPO_ROOT / path
    assert full.exists(), f"File not found: {full}"
    return json.loads(full.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Phase 2: Version consistency (T010)
# ---------------------------------------------------------------------------


class TestVersionConsistency:
    """Version in all manifests must match pyproject.toml."""

    def _get_pyproject_version(self) -> str:
        try:
            import tomllib
        except ModuleNotFoundError:
            import tomli as tomllib  # type: ignore[no-redef]

        data = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        # For setuptools-scm, the fallback_version is used in dev
        return data["tool"]["setuptools_scm"]["fallback_version"]

    def test_plugin_json_version_matches(self) -> None:
        """T016 [US1] plugin.json version matches pyproject.toml."""
        plugin = load_json(Path(".claude-plugin/plugin.json"))
        assert plugin["version"] == self._get_pyproject_version()

    def test_server_json_version_matches(self) -> None:
        """T026 [US2] server.json version matches pyproject.toml."""
        server = load_json(Path("server.json"))
        assert server["version"] == self._get_pyproject_version()

    def test_mcpb_manifest_version_matches(self) -> None:
        """T026 [US2] mcpb/manifest.json version matches pyproject.toml."""
        mcpb = load_json(Path("mcpb/manifest.json"))
        assert mcpb["version"] == self._get_pyproject_version()


# ---------------------------------------------------------------------------
# Phase 3: User Story 1 - Claude Code Plugin (T012-T015)
# ---------------------------------------------------------------------------


class TestPluginJson:
    """T012 [US1] .claude-plugin/plugin.json validation."""

    def test_exists_and_valid_json(self) -> None:
        plugin = load_json(Path(".claude-plugin/plugin.json"))
        assert isinstance(plugin, dict)

    def test_required_fields(self) -> None:
        plugin = load_json(Path(".claude-plugin/plugin.json"))
        required = [
            "name",
            "description",
            "version",
            "author",
            "homepage",
            "repository",
            "license",
            "keywords",
        ]
        for field in required:
            assert field in plugin, f"Missing required field: {field}"

    def test_name(self) -> None:
        plugin = load_json(Path(".claude-plugin/plugin.json"))
        assert plugin["name"] == "mcp-tekna"

    def test_author(self) -> None:
        plugin = load_json(Path(".claude-plugin/plugin.json"))
        assert plugin["author"]["name"] == "Vortiago"

    def test_license(self) -> None:
        plugin = load_json(Path(".claude-plugin/plugin.json"))
        assert plugin["license"] == "MIT"

    def test_keywords(self) -> None:
        plugin = load_json(Path(".claude-plugin/plugin.json"))
        assert isinstance(plugin["keywords"], list)
        assert len(plugin["keywords"]) > 0


class TestMarketplaceJson:
    """T013 [US1] .claude-plugin/marketplace.json validation."""

    def test_exists_and_valid_json(self) -> None:
        marketplace = load_json(Path(".claude-plugin/marketplace.json"))
        assert isinstance(marketplace, dict)

    def test_required_fields(self) -> None:
        marketplace = load_json(Path(".claude-plugin/marketplace.json"))
        assert "owner" in marketplace


class TestMcpJson:
    """T014 [US1] .mcp.json validation."""

    def test_exists_and_valid_json(self) -> None:
        mcp = load_json(Path(".mcp.json"))
        assert isinstance(mcp, dict)

    def test_server_declared(self) -> None:
        mcp = load_json(Path(".mcp.json"))
        assert "mcpServers" in mcp
        assert "mcp-tekna" in mcp["mcpServers"]

    def test_uvx_command(self) -> None:
        mcp = load_json(Path(".mcp.json"))
        server = mcp["mcpServers"]["mcp-tekna"]
        assert server["command"] == "uvx"
        assert server["args"] == ["mcp-tekna"]


class TestMcpDevJson:
    """T015 [US1] .mcp.dev.json validation."""

    def test_exists_and_valid_json(self) -> None:
        mcp = load_json(Path(".mcp.dev.json"))
        assert isinstance(mcp, dict)

    def test_server_declared(self) -> None:
        mcp = load_json(Path(".mcp.dev.json"))
        assert "mcpServers" in mcp
        assert "mcp-tekna" in mcp["mcpServers"]

    def test_uv_run_command(self) -> None:
        mcp = load_json(Path(".mcp.dev.json"))
        server = mcp["mcpServers"]["mcp-tekna"]
        assert server["command"] == "uv"
        assert server["args"] == ["run", "mcp-tekna"]


# ---------------------------------------------------------------------------
# Phase 4: User Story 2 - Claude Desktop (T022-T025)
# ---------------------------------------------------------------------------


class TestServerJson:
    """T022-T024 [US2] server.json validation."""

    def test_exists_and_valid_json(self) -> None:
        server = load_json(Path("server.json"))
        assert isinstance(server, dict)

    def test_required_fields(self) -> None:
        server = load_json(Path("server.json"))
        for field in ("name", "description", "version"):
            assert field in server, f"Missing required field: {field}"

    def test_reverse_dns_name(self) -> None:
        server = load_json(Path("server.json"))
        assert server["name"] == "io.github.Vortiago/mcp-tekna"

    def test_packages_pypi(self) -> None:
        """T023: packages array with pypi registry, uvx runtime, stdio transport."""
        server = load_json(Path("server.json"))
        assert "packages" in server
        pkg = server["packages"][0]
        assert pkg["registryType"] == "pypi"
        assert pkg["runtimeHint"] == "uvx"
        assert pkg["transport"]["type"] == "stdio"

    def test_no_required_env_vars(self) -> None:
        """T024: No required environment variables."""
        server = load_json(Path("server.json"))
        pkg = server["packages"][0]
        env_vars = pkg.get("environmentVariables", [])
        required = [v for v in env_vars if v.get("required", False)]
        assert len(required) == 0


class TestMcpbManifest:
    """T025 [US2] mcpb/manifest.json validation."""

    def test_exists_and_valid_json(self) -> None:
        mcpb = load_json(Path("mcpb/manifest.json"))
        assert isinstance(mcpb, dict)

    def test_required_fields(self) -> None:
        mcpb = load_json(Path("mcpb/manifest.json"))
        for field in (
            "manifest_version",
            "name",
            "version",
            "description",
            "author",
            "server",
        ):
            assert field in mcpb, f"Missing required field: {field}"

    def test_manifest_version(self) -> None:
        mcpb = load_json(Path("mcpb/manifest.json"))
        assert mcpb["manifest_version"] == "0.3"

    def test_server_type_python(self) -> None:
        mcpb = load_json(Path("mcpb/manifest.json"))
        assert mcpb["server"]["type"] == "python"


# ---------------------------------------------------------------------------
# Phase 5: User Story 3 - Docker (T032-T033)
# ---------------------------------------------------------------------------


class TestDockerfile:
    """T032 [US3] Dockerfile validation."""

    def test_exists(self) -> None:
        assert (REPO_ROOT / "Dockerfile").exists()

    def test_has_build_stages(self) -> None:
        content = (REPO_ROOT / "Dockerfile").read_text(encoding="utf-8")
        # Must have at least two FROM instructions (multi-stage)
        from_lines = [
            line for line in content.splitlines() if line.strip().startswith("FROM ")
        ]
        assert len(from_lines) >= 2, "Dockerfile must have multi-stage build"


class TestGlamaJson:
    """T033 [US3] glama.json validation."""

    def test_exists_and_valid_json(self) -> None:
        glama = load_json(Path("glama.json"))
        assert isinstance(glama, dict)

    def test_required_fields(self) -> None:
        glama = load_json(Path("glama.json"))
        assert "$schema" in glama
        assert "maintainers" in glama
        assert "Vortiago" in glama["maintainers"]
