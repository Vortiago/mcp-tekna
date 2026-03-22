# Manifest Contracts

This feature produces configuration files, not APIs. The "contracts"
are the expected file contents that must validate against their
respective schemas.

## Contract 1: plugin.json

Must validate as valid JSON with all required fields from the
Claude Code plugin system. Version must match `pyproject.toml`.

## Contract 2: server.json

Must validate against the MCP server schema at:
`https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json`

Name must follow reverse-DNS format. Package must declare `pypi`
registry type with `uvx` runtime hint and `stdio` transport.

## Contract 3: mcpb/manifest.json

Must validate against `.mcpb` manifest spec v0.3. Server type
must be `python`. Entry point must resolve to the server module.

## Contract 4: .mcp.json / .mcp.dev.json

Must be valid JSON matching MCP client configuration format.
Production config uses `uvx mcp-tekna`. Dev config uses
`uv run mcp-tekna`.

## Contract 5: Dockerfile

Must produce a working container that:
- Starts the MCP server with streamable-http transport
- Listens on port 3000 by default
- Runs as non-root user
- Requires no environment variables
- Responds to health checks

## Validation Strategy

All contracts are verified by `tests/test_manifests.py`:
- JSON schema validation for each manifest
- Version consistency check across all files
- Docker build + connectivity test (integration)
