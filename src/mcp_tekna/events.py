"""Event search and details MCP tools."""

import logging
from typing import Any

import httpx

from mcp_tekna.cache import cached
from mcp_tekna.models import format_event_details, format_event_summary
from mcp_tekna.server import mcp
from mcp_tekna.tekna_client import (
    VALID_REGIONS,
    build_events_query,
    fetch_events,
    resolve_region,
)

logger = logging.getLogger(__name__)


@mcp.tool()
async def search_events(
    query: str | None = None,
    region: str | None = None,
    field_of_study: str | None = None,
    price_group: str | None = None,
    language: str | None = None,
    target_audience: str | None = None,
    event_format: str | None = None,
    page: int = 1,
    page_size: int = 10,
) -> str:
    """Search Tekna's event catalog with optional filters.

    Always include the event links when presenting results.
    Format as clickable markdown: [Event Title](url)

    Args:
        query: Free-text search (e.g., 'AI', 'ledelse')
        region: Filter by region (Digital, Nord-Norge,
            Sørlandet, Trøndelag, Vestlandet, Østlandet)
        field_of_study: Filter by topic
            (e.g., 'Informasjonsteknologi', 'Ledelse')
        price_group: Filter by price
            (free, under_1000, over_1000)
        language: Filter by language (norsk, engelsk)
        target_audience: Filter by audience
            (open, student, member, tekna_ung, tillitsvalgt)
        event_format: Filter by format (in-person, digital)
        page: Page number (1-based, default 1)
        page_size: Items per page (default 10, max 50)
    """
    if region and not resolve_region(region):
        valid = ", ".join(VALID_REGIONS)
        return f"Unknown region: '{region}'. Valid regions are: {valid}"

    try:
        dsl = build_events_query(
            query=query,
            region=region,
            field_of_study=field_of_study,
            price_group=price_group,
            language=language,
            target_audience=target_audience,
            event_format=event_format,
            page=page,
            page_size=min(page_size, 50),
        )
        data = await _cached_fetch_events(dsl)
    except httpx.HTTPStatusError as e:
        logger.error("Events API error: %s", e)
        return f"Error fetching events: HTTP {e.response.status_code}"
    except httpx.HTTPError as e:
        logger.error("Events API error: %s", e)
        return f"Error fetching events: {e}"

    courses = data.get("Courses", {})
    items = courses.get("Items", [])
    paging = courses.get("Paging", {})

    if not items:
        total = paging.get("TotalNumItems", 0)
        return "No events found matching your filters. (0 total)"

    lines = []
    for event in items:
        lines.append(format_event_summary(event))
        lines.append("")

    page_num = paging.get("PageNumber", 1)
    num_pages = paging.get("NumPages", 1)
    total = paging.get("TotalNumItems", len(items))
    lines.append(f"Page {page_num} of {num_pages} ({total} total events)")

    return "\n".join(lines)


@mcp.tool()
async def get_event_details(event_number: str) -> str:
    """Get full details for a specific Tekna event.

    Always include the event link when presenting results.
    Format as clickable markdown: [Event Title](url)

    Args:
        event_number: The event number (e.g., '51691')
    """
    try:
        dsl = build_events_query(query=event_number, page_size=1)
        data = await _cached_fetch_events(dsl)
    except httpx.HTTPStatusError as e:
        logger.error("Event details API error: %s", e)
        return f"Error fetching event details: HTTP {e.response.status_code}"
    except httpx.HTTPError as e:
        logger.error("Event details API error: %s", e)
        return f"Error fetching event details: {e}"

    items = data.get("Courses", {}).get("Items", [])
    if not items:
        return f"No event found with number {event_number}."

    return format_event_details(items[0])


@cached
async def _cached_fetch_events(dsl: str) -> dict[str, Any]:
    return await fetch_events(dsl)
