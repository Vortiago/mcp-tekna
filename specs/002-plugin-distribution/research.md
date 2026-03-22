# Research: Plugin & Distribution Packaging

## R1: .mcpb Bundle Format

**Decision**: Use `.mcpb` (MCP Bundle) format v0.3 for Claude Desktop
distribution.

**Rationale**: `.mcpb` is the current open standard maintained at
`modelcontextprotocol/mcpb` on GitHub. It replaced the older `.dxt`
format in September 2025. It supports Python servers (traditional and
UV-based), has a CLI for init/validate/pack/sign, and enables one-click
installation in Claude Desktop.

**Alternatives considered**:
- `.dxt`: Deprecated, redirects to `.mcpb`. Not viable.
- Manual JSON config only: Works but poor UX for non-developers.

**Key facts**:
- ZIP archive containing `manifest.json` + server code
- `manifest_version: "0.3"` is current
- CLI: `npm install -g @anthropic-ai/mcpb`
- Commands: `mcpb init`, `mcpb validate`, `mcpb pack`, `mcpb sign`
- Supports Python server type with UV runtime
- Template variables: `${__dirname}`, `${user_config.*}`, `${HOME}`
- Sensitive user config stored in OS keychain

## R2: MCP Server Registry Manifest (server.json)

**Decision**: Use the 2025-12-11 server schema for `server.json`.

**Rationale**: This is the latest official schema from
modelcontextprotocol.io. It supports PyPI packages with `uvx` runtime
hint and both stdio and streamable-http transports.

**Alternatives considered**:
- Older schema versions: Outdated, missing `mcpb` registry type.
- No server.json: Would lose discoverability in MCP registries.

**Key facts**:
- Name format: reverse-DNS with `/` separator
  (e.g., `io.github.Vortiago/mcp-tekna`)
- Required fields: `name`, `description`, `version`
- Package: `registryType: "pypi"`, `runtimeHint: "uvx"`
- No required environment variables for mcp-tekna
- Supports `fileSha256` for integrity verification

## R3: Claude Code Plugin Manifest

**Decision**: Use `.claude-plugin/plugin.json` format matching
mcp-outline's established pattern.

**Rationale**: This format is used by existing Claude Code plugins and
is recognized by the plugin system for auto-discovery and marketplace
indexing.

**Key facts**:
- Location: `.claude-plugin/plugin.json`
- Fields: name, description, version, author, homepage, repository,
  license, keywords
- Marketplace metadata in `.claude-plugin/marketplace.json`

## R4: Glama.ai Marketplace

**Decision**: Include `glama.json` at repository root.

**Rationale**: Glama.ai is a primary MCP server marketplace. The
format is minimal (schema URL + maintainers array).

## R5: Docker / Streamable-HTTP

**Decision**: Multi-stage Dockerfile with `uv` base image, defaulting
to streamable-http transport on port 3000.

**Rationale**: Matches mcp-outline pattern. Enables claude.ai web
connectors and shared hosted instances. UV-based image keeps the
container lean.

**Key facts**:
- Base: `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`
- Final: `python:3.12-slim-bookworm`
- Default env: `MCP_TRANSPORT=streamable-http`, `MCP_PORT=3000`
- Non-root user (appuid 1000)
- Health check endpoint via FastMCP

## R6: Version Synchronization

**Decision**: Use `setuptools-scm` for automatic versioning from git
tags. All manifests reference the version from `pyproject.toml` or
are updated via a bump script.

**Rationale**: Single source of truth prevents version drift. The
`poe bump-version` task updates all manifest files atomically.
