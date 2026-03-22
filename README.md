# mcp-tekna

MCP server for Tekna events and news.

## Installation

### Claude Code (Plugin)

```bash
claude plugin add github:Vortiago/mcp-tekna
```

### Claude Desktop (Manual Config)

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mcp-tekna": {
      "command": "uvx",
      "args": ["mcp-tekna"]
    }
  }
}
```

### Claude Desktop (.mcpb Bundle)

```bash
npm install -g @anthropic-ai/mcpb
cd mcpb
mcpb pack
# Double-click the resulting .mcpb file to install
```

### PyPI

```bash
uvx mcp-tekna
```

### Docker

```bash
docker build -t mcp-tekna .
docker run -p 3000:3000 mcp-tekna
# Connect from claude.ai: http://localhost:3000
```

Or with docker compose:

```bash
docker compose up
```

## Development

```bash
uv sync
uv run mcp-tekna
```

For streamable-http transport:

```bash
MCP_TRANSPORT=streamable-http uv run mcp-tekna
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_TRANSPORT` | `stdio` | Transport protocol (`stdio` or `streamable-http`) |
| `MCP_HOST` | `0.0.0.0` | Host for streamable-http |
| `MCP_PORT` | `3000` | Port for streamable-http |

### Running Tests

```bash
uv run pytest tests/ -v
```

### Version Bumping

```bash
git tag v0.2.0
uv run poe bump-version
```

## License

MIT
