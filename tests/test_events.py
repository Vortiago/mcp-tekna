"""Tests for event search and details tools (US1)."""

import json
from pathlib import Path
from unittest.mock import AsyncMock, patch

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
EVENTS_FIXTURE = json.loads(
    (FIXTURES_DIR / "events_response.json").read_text(encoding="utf-8")
)
EMPTY_RESPONSE = {
    "Courses": {
        "Paging": {
            "PageNumber": 1,
            "NumPages": 0,
            "TotalNumItems": 0,
        },
        "Items": [],
        "Refiners": [],
    }
}


class TestSearchEvents:
    """T009-T014, T017: search_events tool tests."""

    async def test_returns_paginated_list(self) -> None:
        """T009: No filters returns paginated list with expected fields."""
        from mcp_tekna.events import search_events

        with patch(
            "mcp_tekna.events.fetch_events",
            new_callable=AsyncMock,
            return_value=EVENTS_FIXTURE,
        ):
            result = await search_events()

        assert "Introduksjon til kunstig intelligens" in result
        assert "Ledelse i praksis" in result
        assert "Page 1 of 51" in result
        assert "501 total" in result

    async def test_region_filter_builds_correct_dsl(self) -> None:
        """T010: Region filter produces :regiondigital= in DSL."""
        from mcp_tekna.tekna_client import build_events_query

        query = build_events_query(region="Vestlandet")
        assert ":regiondigital=Vestlandet" in query

    async def test_query_param_builds_dsl(self) -> None:
        """T011: Query parameter produces :query= in DSL."""
        from mcp_tekna.tekna_client import build_events_query

        query = build_events_query(query="AI")
        assert ":query=AI" in query

    async def test_event_format_filter_builds_dsl(self) -> None:
        """T011b: Event format filter produces :EventFormat= in DSL."""
        from mcp_tekna.tekna_client import build_events_query

        query_digital = build_events_query(event_format="digital")
        assert ":EventFormat=2" in query_digital

        query_inperson = build_events_query(event_format="in-person")
        assert ":EventFormat=1" in query_inperson

    async def test_returns_pagination_info(self) -> None:
        """T012: Response includes pagination metadata."""
        from mcp_tekna.events import search_events

        with patch(
            "mcp_tekna.events.fetch_events",
            new_callable=AsyncMock,
            return_value=EVENTS_FIXTURE,
        ):
            result = await search_events()

        assert "Page 1" in result
        assert "51" in result  # NumPages
        assert "501" in result  # TotalNumItems

    async def test_empty_results_clear_message(self) -> None:
        """T013: Empty results return clear message."""
        from mcp_tekna.events import search_events

        with patch(
            "mcp_tekna.events.fetch_events",
            new_callable=AsyncMock,
            return_value=EMPTY_RESPONSE,
        ):
            result = await search_events(region="Digital")

        lower = result.lower()
        assert "no events" in lower or "0 total" in lower

    async def test_invalid_region_returns_valid_options(self) -> None:
        """Region validation returns list of valid regions."""
        from mcp_tekna.events import search_events

        result = await search_events(region="Bergen")

        assert "Unknown region" in result
        assert "Valid regions" in result
        assert "Digital" in result
        assert "Vestlandet" in result

    async def test_upstream_error_returns_mcp_error(self) -> None:
        """T014: Upstream API failure returns error string."""
        import httpx

        from mcp_tekna.cache import clear_cache
        from mcp_tekna.events import search_events

        clear_cache()
        error = httpx.HTTPStatusError(
            "Server Error",
            request=httpx.Request("GET", "http://test"),
            response=httpx.Response(500),
        )
        mock = AsyncMock(side_effect=error)
        with patch("mcp_tekna.events._cached_fetch_events", mock):
            result = await search_events()

        assert "error" in result.lower()

    async def test_urls_are_absolute(self) -> None:
        """T017: All URLs start with https://www.tekna.no."""
        from mcp_tekna.events import search_events

        with patch(
            "mcp_tekna.events.fetch_events",
            new_callable=AsyncMock,
            return_value=EVENTS_FIXTURE,
        ):
            result = await search_events()

        # All URLs must be absolute (markdown link format)
        assert "https://www.tekna.no" in result
        assert "](https://www.tekna.no" in result


class TestGetEventDetails:
    """T015-T016: get_event_details tool tests."""

    async def test_returns_full_details(self) -> None:
        """T015: Full event details include speakers, agenda, prices."""
        from mcp_tekna.events import get_event_details

        single_response = {
            "Courses": {
                "Paging": {"PageNumber": 1, "NumPages": 1, "TotalNumItems": 1},
                "Items": [EVENTS_FIXTURE["Courses"]["Items"][0]],
                "Refiners": [],
            }
        }

        with patch(
            "mcp_tekna.events.fetch_events",
            new_callable=AsyncMock,
            return_value=single_response,
        ):
            result = await get_event_details(event_number="51691")

        assert "Introduksjon til kunstig intelligens" in result
        assert "Ola Nordmann" in result  # Speaker
        assert "Velkommen og introduksjon" in result  # Agenda
        assert "500" in result  # Price
        assert "https://www.tekna.no/kurs/51691" in result

    async def test_summary_includes_organizer_and_audience(self) -> None:
        """Summary output includes Arrangør and Målgruppe lines."""
        from mcp_tekna.events import search_events

        with patch(
            "mcp_tekna.events.fetch_events",
            new_callable=AsyncMock,
            return_value=EVENTS_FIXTURE,
        ):
            result = await search_events()

        # First event: Organizer "Tekna", price name "Medlem" used as audience
        assert "Arrangør: Tekna" in result
        assert "Målgruppe: Medlem" in result
        # Second event: Tekna Vestland, price name "Medlem"
        assert "Arrangør: Tekna Vestland" in result

    async def test_details_include_audience_and_sub_organizer(self) -> None:
        """Details output includes Målgruppe and Sub-Organizer when present."""
        from mcp_tekna.events import get_event_details

        # Use second event which has SubOrganizer and SearchTargetGroup 2
        single_response = {
            "Courses": {
                "Paging": {"PageNumber": 1, "NumPages": 1, "TotalNumItems": 1},
                "Items": [EVENTS_FIXTURE["Courses"]["Items"][1]],
                "Refiners": [],
            }
        }

        with patch(
            "mcp_tekna.events.fetch_events",
            new_callable=AsyncMock,
            return_value=single_response,
        ):
            result = await get_event_details(event_number="51700")

        assert "**Målgruppe**: Medlem" in result
        assert "**Sub-Organizer**: Tekna Bergen" in result

    async def test_details_omit_sub_organizer_when_null(self) -> None:
        """Details output omits Sub-Organizer when SubOrganizer is null."""
        from mcp_tekna.events import get_event_details

        # First event has SubOrganizer: null
        single_response = {
            "Courses": {
                "Paging": {"PageNumber": 1, "NumPages": 1, "TotalNumItems": 1},
                "Items": [EVENTS_FIXTURE["Courses"]["Items"][0]],
                "Refiners": [],
            }
        }

        with patch(
            "mcp_tekna.events.fetch_events",
            new_callable=AsyncMock,
            return_value=single_response,
        ):
            result = await get_event_details(event_number="51691")

        assert "Sub-Organizer" not in result

    async def test_audience_from_price_name(self) -> None:
        """Audience uses first price tier name, ignoring SearchTargetGroup."""
        from mcp_tekna.models import format_event_details, format_event_summary

        event = {
            "Title": "Biobasert webinar",
            "SearchTargetGroup": 2,
            "Prices": [
                {
                    "Name": "Gratis - åpent for alle",
                    "Amount": 0,
                    "IsAvailable": True,
                }
            ],
        }
        summary = format_event_summary(event)
        assert "Målgruppe: Gratis - åpent for alle" in summary
        assert "Kun medlemmer" not in summary

        details = format_event_details(event)
        assert "**Målgruppe**: Gratis - åpent for alle" in details
        assert "Kun medlemmer" not in details

    async def test_audience_falls_back_to_search_target_group(self) -> None:
        """Falls back to AUDIENCE_MAP when no prices exist."""
        from mcp_tekna.models import format_event_summary

        event = {
            "Title": "Test event",
            "SearchTargetGroup": 2,
            "Prices": [],
        }
        result = format_event_summary(event)
        assert "Målgruppe: Kun medlemmer" in result

    async def test_audience_omitted_when_unknown(self) -> None:
        """Audience label is omitted when SearchTargetGroup is not in map."""
        from mcp_tekna.models import format_event_summary

        event = {"Title": "Test", "SearchTargetGroup": 99}
        result = format_event_summary(event)
        assert "Målgruppe" not in result

    async def test_event_not_found_returns_error(self) -> None:
        """T016: Event not found returns error."""
        from mcp_tekna.events import get_event_details

        with patch(
            "mcp_tekna.events.fetch_events",
            new_callable=AsyncMock,
            return_value=EMPTY_RESPONSE,
        ):
            result = await get_event_details(event_number="99999")

        lower = result.lower()
        assert "not found" in lower or "no event" in lower
