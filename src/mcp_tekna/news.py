"""News MCP tool."""

import logging
from typing import Any

import httpx
from mcp.types import ToolAnnotations

from mcp_tekna.cache import cached
from mcp_tekna.models import format_news_article
from mcp_tekna.server import mcp
from mcp_tekna.tekna_client import fetch_news

logger = logging.getLogger(__name__)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def get_news(
    content_type: str | None = None,
    page: int = 1,
    page_size: int = 10,
) -> str:
    """Fetch recent news articles from Tekna.

    Always include article links when presenting results.
    Format as clickable markdown: [Article Title](url)

    Args:
        content_type: Filter by type (Aktuelt,
            Tekna magasinet, Rad og tips, Politisk,
            Working in Norway)
        page: Page number (1-based, default 1)
        page_size: Items per page (default 10, max 50)
    """
    try:
        data = await _cached_fetch_news(
            content_type=content_type,
            page=page,
            page_size=min(page_size, 50),
        )
    except httpx.HTTPStatusError as e:
        logger.error("News API error: %s", e)
        return f"Error fetching news: HTTP {e.response.status_code}"
    except httpx.HTTPError as e:
        logger.error("News API error: %s", e)
        return f"Error fetching news: {e}"

    items = data.get("Items", [])
    has_more = data.get("HasMore", False)
    page_num = data.get("Page", page)

    if not items:
        return "No news articles found."

    lines = []
    for article in items:
        lines.append(format_news_article(article))
        lines.append("")

    more_msg = "More articles available" if has_more else "No more articles"
    lines.append(f"Page {page_num} | {more_msg}")

    return "\n".join(lines)


@cached
async def _cached_fetch_news(
    content_type: str | None = None,
    page: int = 1,
    page_size: int = 10,
) -> dict[str, Any]:
    return await fetch_news(content_type=content_type, page=page, page_size=page_size)
