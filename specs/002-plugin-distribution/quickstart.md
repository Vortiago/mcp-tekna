# Quickstart: Plugin & Distribution Packaging

## Prerequisites

- Python >=3.10
- `uv` package manager
- Node.js (for `mcpb` CLI only)
- Docker (for container builds only)

## Setup

```bash
# Clone and install
git clone https://github.com/Vortiago/mcp-tekna.git
cd mcp-tekna
uv sync

# Run the server locally (stdio)
uv run mcp-tekna

# Run the server locally (streamable-http)
MCP_TRANSPORT=streamable-http uv run mcp-tekna
```

## Distribution Channels

### Claude Code Plugin

```bash
# Users install with:
claude plugin add mcp-tekna
# Or from repo:
claude plugin add github:Vortiago/mcp-tekna
```

### Claude Desktop (manual config)

Add to `claude_desktop_config.json`:
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

### Claude Desktop (.mcpb bundle)

```bash
# Build the bundle
npm install -g @anthropic-ai/mcpb
cd mcpb
mcpb validate
mcpb pack
# Produces mcp-tekna-<version>.mcpb
# Users double-click to install
```

### Docker

```bash
docker build -t mcp-tekna .
docker run -p 3000:3000 mcp-tekna
# Connect from claude.ai: http://localhost:3000
```

### PyPI

```bash
# After publishing:
uvx mcp-tekna        # Run directly
pip install mcp-tekna # Install globally
```

## Version Bumping

```bash
# Tag a release (setuptools-scm reads tags)
git tag v0.1.0
# Update all manifests
uv run poe bump-version
```

## Verification

```bash
# Run manifest validation tests
uv run pytest tests/test_manifests.py -v

# Validate .mcpb manifest
cd mcpb && mcpb validate

# Test Docker build
docker build -t mcp-tekna . && \
  docker run -d -p 3000:3000 mcp-tekna && \
  curl http://localhost:3000/health
```
