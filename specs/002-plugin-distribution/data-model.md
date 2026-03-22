# Data Model: Plugin & Distribution Packaging

This feature has no runtime data model — it produces static
configuration/manifest files. Below are the file schemas.

## Plugin Manifest (`.claude-plugin/plugin.json`)

| Field       | Type   | Required | Description                    |
|-------------|--------|----------|--------------------------------|
| name        | string | yes      | Package name (`mcp-tekna`)     |
| description | string | yes      | One-line description           |
| version     | string | yes      | Semver (synced with pyproject)  |
| author      | object | yes      | `{ name: string }`             |
| homepage    | string | yes      | GitHub repo URL                |
| repository  | string | yes      | GitHub repo URL                |
| license     | string | yes      | SPDX identifier (`MIT`)        |
| keywords    | array  | yes      | Discovery tags                 |

## Server Manifest (`server.json`)

| Field       | Type   | Required | Description                    |
|-------------|--------|----------|--------------------------------|
| $schema     | string | no       | MCP server schema URL          |
| name        | string | yes      | Reverse-DNS (`io.github.Vortiago/mcp-tekna`) |
| title       | string | no       | Display name                   |
| version     | string | yes      | Semver                         |
| description | string | yes      | Brief description              |
| repository  | object | no       | `{ url, source }`              |
| packages    | array  | no       | Distribution packages          |

### Package Entry

| Field                | Type   | Required | Description              |
|----------------------|--------|----------|--------------------------|
| registryType         | string | yes      | `pypi`                   |
| identifier           | string | yes      | `mcp-tekna`              |
| transport.type       | string | yes      | `stdio`                  |
| runtimeHint          | string | no       | `uvx`                    |
| environmentVariables | array  | no       | Empty (no required vars)  |

## MCPB Manifest (`mcpb/manifest.json`)

| Field             | Type   | Required | Description                |
|-------------------|--------|----------|----------------------------|
| manifest_version  | string | yes      | `0.3`                      |
| name              | string | yes      | `mcp-tekna`                |
| version           | string | yes      | Semver                     |
| description       | string | yes      | One-line description       |
| author            | object | yes      | `{ name, url? }`           |
| server.type       | string | yes      | `python`                   |
| server.entry_point| string | yes      | Path to server module      |
| server.mcp_config | object | yes      | Transport and env config   |
| repository        | string | no       | GitHub URL                 |

## Marketplace Entry (`glama.json`)

| Field       | Type   | Required | Description                    |
|-------------|--------|----------|--------------------------------|
| $schema     | string | yes      | Glama schema URL               |
| maintainers | array  | yes      | GitHub usernames               |

## Client Config (`.mcp.json`)

| Field                    | Type   | Required | Description          |
|--------------------------|--------|----------|----------------------|
| mcpServers               | object | yes      | Server definitions   |
| mcpServers.mcp-tekna     | object | yes      | Server config        |
| .command                 | string | yes      | `uvx`                |
| .args                    | array  | yes      | `["mcp-tekna"]`      |
| .env                     | object | no       | Optional env vars    |

## Relationships

```text
pyproject.toml (version source of truth)
  ├── .claude-plugin/plugin.json (version synced)
  ├── server.json (version synced)
  ├── mcpb/manifest.json (version synced)
  └── bump-version script (updates all)
```
