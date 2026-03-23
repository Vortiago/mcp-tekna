"""Tests for news tool (US2)."""

import json
from pathlib import Path
from unittest.mock import AsyncMock, patch

import httpx

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
NEWS_FIXTURE = json.loads(
    (FIXTURES_DIR / "news_response.json").read_text(encoding="utf-8")
)


class TestGetNews:
    """T023-T027: get_news tool tests."""

    async def test_returns_articles_with_fields(self) -> None:
        """T023: No filters returns articles with title, date, summary, type, URL."""
        from mcp_tekna.news import get_news

        with patch(
            "mcp_tekna.news.fetch_news",
            new_callable=AsyncMock,
            return_value=NEWS_FIXTURE,
        ):
            result = await get_news()

        assert "Tekna støtter verktøy" in result
        assert "Lønnsoppgjøret 2026" in result
        assert "Aktuelt" in result
        assert "Politisk" in result

    async def test_content_type_filter(self) -> None:
        """T024: Content type filter is passed correctly."""
        from mcp_tekna.news import get_news

        filtered = {
            "Page": 1,
            "PageSize": 10,
            "Items": [NEWS_FIXTURE["Items"][1]],
            "HasMore": False,
        }

        mock = AsyncMock(return_value=filtered)
        with patch("mcp_tekna.news.fetch_news", mock):
            await get_news(content_type="Politisk")

        mock.assert_called_once_with(content_type="Politisk", page=1, page_size=10)

    async def test_returns_pagination_info(self) -> None:
        """T025: Response includes pagination and HasMore indicator."""
        from mcp_tekna.news import get_news

        with patch(
            "mcp_tekna.news.fetch_news",
            new_callable=AsyncMock,
            return_value=NEWS_FIXTURE,
        ):
            result = await get_news()

        assert "Page 1" in result
        assert "more" in result.lower()  # HasMore indicator

    async def test_upstream_error_returns_mcp_error(self) -> None:
        """T026: Upstream failure returns error."""
        from mcp_tekna.cache import clear_cache
        from mcp_tekna.news import get_news

        clear_cache()
        error = httpx.HTTPStatusError(
            "Error",
            request=httpx.Request("POST", "http://test"),
            response=httpx.Response(500),
        )
        mock = AsyncMock(side_effect=error)
        with patch("mcp_tekna.news._cached_fetch_news", mock):
            result = await get_news()

        assert "error" in result.lower()

    async def test_urls_are_absolute(self) -> None:
        """T027: All URLs start with https://www.tekna.no."""
        from mcp_tekna.news import get_news

        with patch(
            "mcp_tekna.news.fetch_news",
            new_callable=AsyncMock,
            return_value=NEWS_FIXTURE,
        ):
            result = await get_news()

        assert "https://www.tekna.no" in result
        assert "](https://www.tekna.no" in result
