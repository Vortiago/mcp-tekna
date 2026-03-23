import logging
import os
from typing import Literal

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

host = os.getenv("MCP_HOST", "0.0.0.0")
port = int(os.getenv("MCP_PORT", "3000"))

mcp = FastMCP(
    "mcp-tekna",
    instructions=(
        "Tekna events and news MCP server. "
        "Always include URLs/links from tool results when "
        "presenting information to the user. Format links as "
        "clickable markdown hyperlinks."
    ),
    host=host,
    port=port,
)


def main() -> None:
    import mcp_tekna.benefits  # noqa: F401
    import mcp_tekna.events  # noqa: F401
    import mcp_tekna.news  # noqa: F401

    transport: Literal["stdio", "sse", "streamable-http"] = "stdio"
    env_transport = os.getenv("MCP_TRANSPORT")
    if env_transport in ("stdio", "sse", "streamable-http"):
        transport = env_transport  # type: ignore[assignment]
    mcp.run(transport=transport)
