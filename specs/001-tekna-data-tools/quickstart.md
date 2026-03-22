# Quickstart: Tekna Data Tools

## Prerequisites

- Python >=3.10
- `uv` package manager
- mcp-tekna server installed (see 002-plugin-distribution)

## Running

```bash
uv sync
uv run mcp-tekna
```

## MCP Tools

### search_events

Search Tekna's event catalog with optional filters.

```
User: "What AI events does Tekna have?"
→ search_events(query="AI")

User: "Show me free digital events"
→ search_events(region="Digital", price_group="free")

User: "Tekna events in Vestlandet about leadership"
→ search_events(region="Vestlandet", field_of_study="Ledelse")
```

### get_event_details

Get full details for a specific event.

```
User: "Tell me more about event 51691"
→ get_event_details(event_number="51691")
```

### get_news

Fetch recent Tekna news articles.

```
User: "What's the latest news from Tekna?"
→ get_news()

User: "Show me political articles from Tekna"
→ get_news(content_type="Politisk")
```

### get_member_benefits

List all Tekna member benefits.

```
User: "What member benefits does Tekna offer?"
→ get_member_benefits()
```

## Integration Scenarios

### Scenario 1: Event Discovery
1. User asks about upcoming events
2. Agent calls `search_events` with relevant filters
3. User picks an event of interest
4. Agent calls `get_event_details` for full info
5. User clicks the URL to register

### Scenario 2: News + Events
1. User asks "What's happening at Tekna?"
2. Agent calls `get_news(page_size=5)` for latest news
3. Agent calls `search_events(page_size=5)` for upcoming events
4. Agent presents combined overview with URLs

### Scenario 3: Membership Value
1. User asks about Tekna membership
2. Agent calls `get_member_benefits()` for full list
3. User explores specific benefits via URLs
