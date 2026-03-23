"""Tests for member benefits tool (US3)."""

from pathlib import Path
from unittest.mock import AsyncMock, patch

import httpx

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
BENEFITS_HTML = (FIXTURES_DIR / "benefits_page.html").read_text(encoding="utf-8")


class TestGetMemberBenefits:
    """T032-T035: get_member_benefits tool tests."""

    async def test_returns_benefits_by_category(self) -> None:
        """T032: Returns benefits organized by core and partner categories."""
        from mcp_tekna.benefits import get_member_benefits

        with patch(
            "mcp_tekna.benefits.fetch_benefits_html",
            new_callable=AsyncMock,
            return_value=BENEFITS_HTML,
        ):
            result = await get_member_benefits()

        assert "Fondssparing og pensjon" in result
        assert "SATS" in result
        assert "partner" in result.lower()

    async def test_upstream_error_returns_mcp_error(self) -> None:
        """T033: Upstream failure returns error."""
        from mcp_tekna.benefits import get_member_benefits
        from mcp_tekna.cache import clear_cache

        clear_cache()
        error = httpx.HTTPStatusError(
            "Error",
            request=httpx.Request("GET", "http://test"),
            response=httpx.Response(500),
        )
        mock = AsyncMock(side_effect=error)
        with patch(
            "mcp_tekna.benefits._cached_fetch_benefits",
            mock,
        ):
            result = await get_member_benefits()

        assert "error" in result.lower()

    async def test_malformed_html_returns_error(self) -> None:
        """T034: Unrecognizable HTML returns clear error."""
        from mcp_tekna.benefits import get_member_benefits
        from mcp_tekna.cache import clear_cache

        clear_cache()
        with patch(
            "mcp_tekna.benefits._cached_fetch_benefits",
            new_callable=AsyncMock,
            return_value="<html><body></body></html>",
        ):
            result = await get_member_benefits()

        lower = result.lower()
        assert "no benefits" in lower or "could not" in lower or "error" in lower

    async def test_urls_are_absolute(self) -> None:
        """T035: All URLs start with https://www.tekna.no."""
        from mcp_tekna.benefits import get_member_benefits

        with patch(
            "mcp_tekna.benefits.fetch_benefits_html",
            new_callable=AsyncMock,
            return_value=BENEFITS_HTML,
        ):
            result = await get_member_benefits()

        assert "https://www.tekna.no" in result
        assert "](https://www.tekna.no" in result
