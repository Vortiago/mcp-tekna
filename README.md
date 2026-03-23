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

## Tools

### search_events

Search Tekna's event catalog with optional filters for region, topic, format, price, language, and audience.

```
search_events(query="AI", region="Vestlandet")
```

### get_event_details

Get full details for a specific event including speakers, agenda, and pricing.

```
get_event_details(event_number="51691")
```

### get_news

Fetch recent news articles with optional content type filtering.

```
get_news(content_type="Politisk", page=1)
```

### get_member_benefits

List all Tekna member benefits organized by category.

```
get_member_benefits()
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
| `TEKNA_TIMEOUT` | `30` | Tekna API timeout in seconds |
| `TEKNA_CACHE_TTL` | `900` | Cache TTL in seconds (15 min) |
| `LOG_LEVEL` | `INFO` | Logging level |

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
