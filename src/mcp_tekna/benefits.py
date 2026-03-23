"""Member benefits MCP tool."""

import logging

import httpx
from bs4 import BeautifulSoup

from mcp_tekna.cache import cached
from mcp_tekna.models import format_member_benefit
from mcp_tekna.server import mcp
from mcp_tekna.tekna_client import fetch_benefits_html

logger = logging.getLogger(__name__)


@mcp.tool()
async def get_member_benefits() -> str:
    """List all Tekna member benefits with descriptions and URLs.

    Always include benefit links when presenting results.
    Format as clickable markdown: [Benefit Name](url)
    """
    try:
        html = await _cached_fetch_benefits()
    except httpx.HTTPStatusError as e:
        logger.error("Benefits page error: %s", e)
        return f"Error fetching member benefits: HTTP {e.response.status_code}"
    except httpx.HTTPError as e:
        logger.error("Benefits page error: %s", e)
        return f"Error fetching member benefits: {e}"

    benefits = _parse_benefits(html)
    if not benefits:
        return (
            "Could not find any benefits on the page."
            " The page structure may have changed."
        )

    lines = ["# Tekna Member Benefits", ""]

    core = [b for b in benefits if b["category"] == "core"]
    partner = [b for b in benefits if b["category"] == "partner"]

    if core:
        lines.append("## Core Benefits")
        lines.append("")
        for b in core:
            lines.append(format_member_benefit(b))
            lines.append("")

    if partner:
        lines.append("## Partner Benefits")
        lines.append("")
        for b in partner:
            lines.append(format_member_benefit(b))
            lines.append("")

    return "\n".join(lines)


def _parse_benefits(html: str) -> list[dict]:
    """Parse member benefits from HTML page."""
    soup = BeautifulSoup(html, "html.parser")
    benefits = []

    # Partner benefits: <a class="t-article-card"> with h3 + excerpt
    for card in soup.find_all("a", class_="t-article-card"):
        h3 = card.find("h3")
        excerpt = card.find(class_="t-article-card__excerpt")
        if not h3:
            continue
        benefits.append(
            {
                "name": h3.get_text(strip=True),
                "description": (excerpt.get_text(strip=True) if excerpt else ""),
                "url": card.get("href", ""),
                "category": "partner",
            }
        )

    # Fallback: legacy structure with benefit-card divs
    if not benefits:
        for section_cls, cat in [
            ("member-benefits-core", "core"),
            ("member-benefits-partner", "partner"),
        ]:
            section = soup.find("section", class_=section_cls)
            if not section:
                continue
            for card in section.find_all("div", class_="benefit-card"):
                link = card.find("a")
                if not link:
                    continue
                h3 = link.find("h3")
                p = link.find("p")
                if not h3:
                    continue
                benefits.append(
                    {
                        "name": h3.get_text(strip=True),
                        "description": (p.get_text(strip=True) if p else ""),
                        "url": link.get("href", ""),
                        "category": cat,
                    }
                )

    return benefits


@cached
async def _cached_fetch_benefits() -> str:
    return await fetch_benefits_html()
