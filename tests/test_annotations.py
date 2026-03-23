"""T001 [US1] Verify all MCP tools have readOnlyHint annotation."""

import pytest

import mcp_tekna.benefits  # noqa: F401
import mcp_tekna.events  # noqa: F401
import mcp_tekna.news  # noqa: F401
from mcp_tekna.server import mcp

EXPECTED_TOOLS = {
    "get_member_benefits",
    "search_events",
    "get_event_details",
    "get_news",
}


@pytest.mark.asyncio
async def test_all_tools_have_readonly_annotation() -> None:
    """Every registered tool must have readOnlyHint=True."""
    tools = await mcp.list_tools()
    tool_names = {t.name for t in tools}

    assert EXPECTED_TOOLS.issubset(tool_names), (
        f"Missing tools: {EXPECTED_TOOLS - tool_names}"
    )

    for tool in tools:
        if tool.name in EXPECTED_TOOLS:
            assert tool.annotations is not None, (
                f"Tool '{tool.name}' has no annotations"
            )
            assert tool.annotations.readOnlyHint is True, (
                f"Tool '{tool.name}' readOnlyHint is not True"
            )


@pytest.mark.asyncio
async def test_no_tool_missing_annotations() -> None:
    """No tool should be registered without annotations."""
    tools = await mcp.list_tools()

    for tool in tools:
        assert tool.annotations is not None, (
            f"Tool '{tool.name}' is missing annotations"
        )
