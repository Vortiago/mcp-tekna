"""Async HTTP client for Tekna public APIs."""

import logging
import os
from typing import Any

import httpx

logger = logging.getLogger(__name__)

BASE_URL = "https://www.tekna.no"
_TIMEOUT = int(os.getenv("TEKNA_TIMEOUT", "30"))

# News API constants
NEWS_PARENT_LINK = "314"
NEWS_PAGE_TYPES = (
    "CGI.Delegate.Models.Pages.ArticleFeaturePage,"
    "CGI.Delegate.Models.Pages.ArticlePage,"
    "CGI.Delegate.Models.Pages.NewsArticlePage,"
    "CGI.Delegate.Models.Pages.RestrictedArticleFeaturePage,"
    "CGI.Delegate.Models.Pages.TeknaMagArticlePage,"
    "CGI.Delegate.Models.Pages.VevDesignScrollyTellPage"
)

ALL_CONTENT_TYPES = "Aktuelt,Tekna magasinet,Råd og tips,Politisk,Working in Norway"


def make_absolute_url(path: str) -> str:
    """Prepend base URL to a relative path if needed."""
    if path.startswith("http"):
        return path
    return f"{BASE_URL}{path}"


# Region name mapping: accepted input → API value
# Accepts both ASCII-friendly and Norwegian-character variants
REGION_MAP: dict[str, str] = {
    "digital": "Digital",
    "nord-norge": "Nord-Norge",
    "sorlandet": "Sørlandet",
    "sørlandet": "Sørlandet",
    "trondelag": "Trøndelag",
    "trøndelag": "Trøndelag",
    "vestlandet": "Vestlandet",
    "ostlandet": "Østlandet",
    "østlandet": "Østlandet",
}

VALID_REGIONS = [
    "Digital",
    "Nord-Norge",
    "Sørlandet",
    "Trøndelag",
    "Vestlandet",
    "Østlandet",
]


def resolve_region(region: str) -> str | None:
    """Resolve a region input to the API-expected value.

    Returns the resolved region name, or None if not found.
    """
    return REGION_MAP.get(region.lower())


def build_events_query(
    *,
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
    """Build the colon-separated DSL query string for the events API."""
    parts = [
        "course",
        "format=full",
        f"pageSize={page_size}",
        f"pagenumber={page}",
    ]

    if query:
        parts.append(f"query={query}")

    if region:
        resolved = resolve_region(region)
        if resolved:
            parts.append(f"regiondigital={resolved}")

    if field_of_study:
        parts.append(f"fieldsofstudy={field_of_study}")

    price_map = {"free": "0", "under_1000": "1000", "over_1000": ">1000"}
    if price_group and price_group in price_map:
        parts.append(f"pricegroup={price_map[price_group]}")

    lang_map = {"norsk": "1", "engelsk": "2"}
    if language and language in lang_map:
        parts.append(f"language={lang_map[language]}")

    audience_map = {
        "open": "0",
        "student": "1",
        "member": "2",
        "tekna_ung": "3",
        "tillitsvalgt": "4",
    }
    if target_audience and target_audience in audience_map:
        parts.append(f"searchtargetgroup={audience_map[target_audience]}")

    format_map = {"in-person": "1", "digital": "2"}
    if event_format and event_format in format_map:
        parts.append(f"EventFormat={format_map[event_format]}")

    return ":".join(parts)


async def fetch_events(query_string: str) -> dict[str, Any]:
    """Fetch events from the Tekna typeahead API."""
    url = f"{BASE_URL}/api/typeahead/lists"
    params = {"q": query_string, "lang": "no"}

    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        logger.info("Fetching events: %s", params)
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()


async def fetch_news(
    *,
    content_type: str | None = None,
    page: int = 1,
    page_size: int = 10,
) -> dict[str, Any]:
    """Fetch news articles from the Tekna content feed API."""
    url = f"{BASE_URL}/api/tagsearch/content/feed"
    params = {"lang": "nb-NO"}

    body = {
        "ParentLink": NEWS_PARENT_LINK,
        "PageTypes": NEWS_PAGE_TYPES,
        "Tags": None,
        "AllowedTags": [],
        "PreselectedIds": [],
        "PreselectedContentListItems": [],
        "Page": page,
        "PageSize": page_size,
        "NewsListLandingPage": True,
        "HasStreaming": False,
        "ContentTypes": content_type if content_type else ALL_CONTENT_TYPES,
    }

    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        logger.info("Fetching news: page=%d, type=%s", page, content_type)
        resp = await client.post(url, params=params, json=body)
        resp.raise_for_status()
        return resp.json()


async def fetch_benefits_html() -> str:
    """Fetch the member benefits page HTML."""
    url = f"{BASE_URL}/medlemsfordeler/"

    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        logger.info("Fetching member benefits page")
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.text
