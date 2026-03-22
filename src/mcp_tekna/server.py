import os

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

host = os.getenv("MCP_HOST", "0.0.0.0")
port = int(os.getenv("MCP_PORT", "3000"))

mcp = FastMCP(
    "mcp-tekna",
    instructions="Tekna events and news MCP server",
    host=host,
    port=port,
)


@mcp.tool()
async def ping() -> str:
    """Check if the Tekna MCP server is running."""
    return "pong"


def main() -> None:
    transport = os.getenv("MCP_TRANSPORT", "stdio")
    mcp.run(transport=transport)
