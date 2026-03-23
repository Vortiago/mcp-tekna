# MCP Tool Contracts: Tekna Data Tools

## Tool 1: `search_events`

Search Tekna's event catalog with optional filters.

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "Free-text search query (e.g., 'AI', 'ledelse')"
    },
    "region": {
      "type": "string",
      "enum": ["Digital", "Nord-Norge", "Sørlandet", "Trøndelag", "Vestlandet", "Østlandet"],
      "description": "Filter by geographic region"
    },
    "field_of_study": {
      "type": "string",
      "description": "Filter by topic category name (e.g., 'Informasjonsteknologi', 'Ledelse')"
    },
    "price_group": {
      "type": "string",
      "enum": ["free", "under_1000", "over_1000"],
      "description": "Filter by price range"
    },
    "language": {
      "type": "string",
      "enum": ["norsk", "engelsk"],
      "description": "Filter by event language"
    },
    "target_audience": {
      "type": "string",
      "enum": ["open", "student", "member", "tekna_ung", "tillitsvalgt"],
      "description": "Filter by target audience"
    },
    "event_format": {
      "type": "string",
      "enum": ["in-person", "digital"],
      "description": "Filter by event format"
    },
    "page": {
      "type": "integer",
      "default": 1,
      "description": "Page number (1-based)"
    },
    "page_size": {
      "type": "integer",
      "default": 10,
      "description": "Items per page (max 50)"
    }
  },
  "required": []
}
```

### Response

Returns a text content block with structured event list including
pagination info. Each event includes: title, date, location, region,
format, price summary, enrollment status, and URL.

### Error Handling

- Upstream API failure → MCP error with `isError: true`, message
  describing the HTTP status or timeout
- Invalid filter value → MCP error explaining valid options

---

## Tool 2: `get_event_details`

Get full details for a specific Tekna event.

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "event_number": {
      "type": "string",
      "description": "Event number (e.g., '51691')"
    }
  },
  "required": ["event_number"]
}
```

### Response

Returns a text content block with full event details: title, dates,
location, description, speakers, agenda, pricing tiers, enrollment
status, capacity, and URL.

### Error Handling

- Event not found → MCP error with `isError: true`
- Upstream failure → MCP error with status description

---

## Tool 3: `get_news`

Fetch recent news articles from Tekna.

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "content_type": {
      "type": "string",
      "enum": ["Aktuelt", "Tekna magasinet", "Rad og tips", "Politisk", "Working in Norway"],
      "description": "Filter by article content type"
    },
    "page": {
      "type": "integer",
      "default": 1,
      "description": "Page number (1-based)"
    },
    "page_size": {
      "type": "integer",
      "default": 10,
      "description": "Items per page (max 50)"
    }
  },
  "required": []
}
```

### Response

Returns a text content block with article list: title, date, summary,
content type, and URL for each article. Includes pagination info.

### Error Handling

- Upstream failure → MCP error with status/timeout description
- Invalid content type → MCP error listing valid options

---

## Tool 4: `get_member_benefits`

List all Tekna member benefits.

### Input Schema

```json
{
  "type": "object",
  "properties": {},
  "required": []
}
```

### Response

Returns a text content block listing all benefits organized by
category (core benefits and partner benefits). Each benefit includes
name, description, and URL.

### Error Handling

- HTML parsing failure → MCP error with `isError: true`, message
  indicating the page structure may have changed
- Upstream failure → MCP error with status description

---

## Cross-Cutting Contracts

### URL Format

All URLs in responses MUST be absolute: `https://www.tekna.no/...`

### Caching

All tools use a 15-minute in-memory TTL cache. Responses MUST NOT
be older than 15 minutes.

### Timeouts

All upstream HTTP requests use a 30-second timeout (configurable
via `TEKNA_TIMEOUT` env var).
