# Feature Specification: Tekna Data Tools

**Feature Branch**: `001-tekna-data-tools`
**Created**: 2026-03-22
**Status**: Draft
**Input**: User description: "A MCP server allows agents to collect data from Tekna.no. Supporting queries like 'What events does tekna have coming up in my area?' where it then searches and returns the list of events from the event list in Tekna. Or queries like 'What news from Tekna' where it returns the news from the news page or 'What member benefits do I have' where it returns data about this parsed from the website. It should always include the URL to the correct pages so users can open it in a browser. Initial goal is a public mcp server that people can connect to so we don't have to think about logging in to Tekna to grab any data."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Search Upcoming Events (Priority: P1)

A user asks their AI agent "What events does Tekna have coming up in my area?" The agent uses the MCP server to search Tekna's event catalog, filtering by region. The server returns a list of upcoming events with titles, dates, locations, prices, and direct URLs to each event page on tekna.no. The user can then click any URL to view full details and register.

**Why this priority**: Events are Tekna's core offering and the most frequently queried data. The events API is well-structured and publicly available, making this the highest-value, lowest-risk starting point.

**Independent Test**: Can be fully tested by requesting events with various filters (region, topic, format) and verifying structured results with valid URLs are returned.

**Acceptance Scenarios**:

1. **Given** the MCP server is running, **When** a user requests upcoming events without filters, **Then** the server returns a paginated list of events with title, date, location, price, format, and URL for each event.
2. **Given** the MCP server is running, **When** a user requests events filtered by region (e.g., "Vestlandet"), **Then** only events in that region are returned.
3. **Given** the MCP server is running, **When** a user requests events filtered by topic (e.g., "IT" or "Ledelse"), **Then** only events matching that field of study are returned.
4. **Given** the MCP server is running, **When** a user requests events filtered by format (e.g., digital only), **Then** only events matching that format are returned.
5. **Given** the MCP server is running, **When** a user requests events and none match the filters, **Then** the server returns an empty list with a clear message.
6. **Given** the MCP server is running, **When** a user requests details for a specific event, **Then** the server returns full event details including description, speakers, agenda, pricing tiers, and enrollment status.

---

### User Story 2 - Browse Tekna News (Priority: P2)

A user asks their AI agent "What's the latest news from Tekna?" The agent uses the MCP server to fetch recent articles from Tekna's news feed. The server returns article titles, publication dates, summaries, content types, and URLs to each article on tekna.no.

**Why this priority**: News is the second most dynamic content type on tekna.no and has a public API available. It complements events by giving users a broader picture of Tekna's activities.

**Independent Test**: Can be fully tested by requesting news articles and verifying structured results with titles, dates, summaries, and valid URLs are returned.

**Acceptance Scenarios**:

1. **Given** the MCP server is running, **When** a user requests recent news, **Then** the server returns a list of articles with title, date, summary, content type, and URL.
2. **Given** the MCP server is running, **When** a user requests news filtered by content type (e.g., "Politisk" or "Tekna magasinet"), **Then** only articles of that type are returned.
3. **Given** the MCP server is running, **When** a user requests more articles beyond the initial results, **Then** the server supports pagination to load additional articles.

---

### User Story 3 - View Member Benefits (Priority: P3)

A user asks their AI agent "What member benefits does Tekna offer?" The agent uses the MCP server to retrieve the list of member benefits. The server returns benefit names, descriptions, partner information, and URLs to detailed benefit pages on tekna.no.

**Why this priority**: Member benefits are relatively static content and don't have a dedicated API (requires HTML parsing). However, this is valuable information for members evaluating their membership. Lower priority because the data changes infrequently and requires more maintenance effort.

**Independent Test**: Can be fully tested by requesting the benefits list and verifying all known benefits are returned with names, descriptions, and valid URLs.

**Acceptance Scenarios**:

1. **Given** the MCP server is running, **When** a user requests member benefits, **Then** the server returns a list of all benefits with name, description, category (core benefit vs. partner benefit), and URL to the detail page.
2. **Given** the MCP server is running, **When** the benefits page structure on tekna.no changes unexpectedly, **Then** the server returns a clear error message rather than malformed data.

---

### Edge Cases

- What happens when Tekna's website is temporarily unavailable or returns errors?
- How does the system handle when the events API changes its response structure?
- What happens when a user requests events for a region that doesn't exist in Tekna's system?
- How does the system handle events with missing or incomplete data fields (e.g., no price, no location)?
- What happens when HTML structure of the member benefits page changes?
- How does the system handle rate limiting if Tekna imposes request limits?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST expose MCP tools for searching Tekna events with optional free-text keyword search and optional filters for region, field of study, event format, price range, and target audience.
- **FR-002**: System MUST expose an MCP tool for retrieving detailed information about a specific event by event number or URL.
- **FR-003**: System MUST expose an MCP tool for fetching recent news articles from Tekna with optional content type filtering and pagination.
- **FR-004**: System MUST expose an MCP tool for listing all Tekna member benefits with names, descriptions, and URLs.
- **FR-005**: Every response MUST include the full tekna.no URL for each item so users can open it directly in a browser.
- **FR-006**: System MUST return structured, human-readable responses suitable for AI agent consumption.
- **FR-007**: System MUST operate without requiring Tekna login credentials — all data MUST be sourced from publicly accessible endpoints.
- **FR-008**: System MUST handle pagination for events and news, returning 10 items per call by default, allowing callers to request specific pages or page sizes.
- **FR-009**: System MUST return meaningful error messages when upstream requests to tekna.no fail.
- **FR-010**: System MUST include event metadata: title, date/time, location, region, format (in-person/digital/hybrid), price, enrollment status, and number of available spots when provided.
- **FR-011**: System MUST cache responses from Tekna with a 15-minute TTL to reduce upstream load and improve latency. Callers MUST NOT receive data older than 15 minutes.

### Key Entities

- **Event**: A course or arrangement on Tekna with title, dates, location, region, format, pricing, speakers, agenda, enrollment status, and public URL. Identified by event number.
- **News Article**: A published article on Tekna with title, publication date, summary text, content type (Aktuelt, Politisk, Tekna magasinet, Rad og tips, Working in Norway), and public URL.
- **Member Benefit**: A benefit offered to Tekna members with name, description, category (core benefit or partner benefit), partner name, and URL to detail page.

## Clarifications

### Session 2026-03-22

- Q: Should events support free-text keyword search in addition to filter-based search? → A: Yes, add optional free-text keyword search alongside existing filters.
- Q: How many items should be returned per tool call by default? → A: 10 items per call (balanced, matches Tekna's default).
- Q: Should the server cache responses from Tekna? → A: Yes, cache with 15-minute TTL.

## Assumptions

- Tekna's public APIs at `/api/typeahead/lists` (events) and `/api/tagsearch/content/feed` (news) will remain publicly accessible without authentication.
- The member benefits page at `/medlemsfordeler/` maintains a stable enough HTML structure for reliable parsing.
- The MCP server will be deployed as a publicly accessible service (no authentication on the MCP server itself for this initial version).
- Event regions follow Tekna's established categories: Digital, Nord-Norge, Sorlandet, Trondelag, Vestlandet, Ostlandet.
- Norwegian language (`lang=no`) is the default for all requests, with English as an optional parameter where supported.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can search for upcoming Tekna events by region, topic, or format and receive results within 5 seconds.
- **SC-002**: Every returned item (event, article, benefit) includes a clickable URL that resolves to the correct page on tekna.no.
- **SC-003**: The server correctly returns at least 95% of the events available on tekna.no when queried without filters.
- **SC-004**: News articles are returned in reverse chronological order with accurate publication dates.
- **SC-005**: The server operates reliably without requiring any user credentials or login tokens.
- **SC-006**: When tekna.no is unreachable, the server returns a clear error within 30 seconds rather than hanging indefinitely.
