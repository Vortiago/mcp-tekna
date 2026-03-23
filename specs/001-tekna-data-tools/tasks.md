# Tasks: Tekna Data Tools

**Input**: Design documents from `/specs/001-tekna-data-tools/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Included per constitution principle I (Test-First, NON-NEGOTIABLE). Tests are written first and must fail before implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root

## Phase 1: Setup

**Purpose**: Add new dependencies and create shared infrastructure modules

- [x] T001 Add `cachetools` and `beautifulsoup4` to dependencies and `pytest-httpx` to dev dependencies in pyproject.toml, then run `uv sync`
- [x] T002 [P] Create src/mcp_tekna/cache.py with a TTL cache wrapper using cachetools.TTLCache (15-minute default TTL, configurable via TEKNA_CACHE_TTL env var), exposing a `cached` decorator that keys by function name + serialized args
- [x] T003 [P] Create src/mcp_tekna/tekna_client.py with an async httpx client class for Tekna APIs: base URL `https://www.tekna.no`, configurable timeout via TEKNA_TIMEOUT env var (default 30s), methods for building the events DSL query string (`q=course:key=value:key=value`), POSTing to news feed, and GETting HTML pages. Include `make_absolute_url()` helper to prepend base URL to relative paths
- [x] T004 [P] Create tests/fixtures/ directory with sample API response files: tests/fixtures/events_response.json (subset of real events API response with 2 items, Paging, and Refiners), tests/fixtures/news_response.json (subset of real news API response with 2 items and HasMore), and tests/fixtures/benefits_page.html (minimal HTML matching the member benefits page structure with 1 core and 1 partner benefit)
- [x] T005 Update tests/conftest.py to add shared fixtures for loading test fixture files from tests/fixtures/ and for creating a mock TeknaClient
- [x] T005b [P] Configure structured logging in src/mcp_tekna/server.py: set up Python logging with format including timestamp, level, and message; set default level via LOG_LEVEL env var (default INFO); ensure all upstream HTTP errors are logged before being returned as MCP errors

**Checkpoint**: Dependencies installed, shared client and cache modules ready

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Test infrastructure and response formatting that all user stories depend on

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Create src/mcp_tekna/models.py with response formatting functions: `format_event_summary()` that formats a single event dict from the API into a human-readable text block (title, date, location, region, format, price, URL), `format_event_details()` for full details (adds description, speakers, agenda, pricing tiers, enrollment), `format_news_article()` for a single article (title, date, summary, type, URL), and `format_member_benefit()` for a single benefit (name, description, category, URL)
- [x] T007 [P] Create tests/test_cache.py with tests: cache stores and returns values, cache expires after TTL, different args produce different cache keys, cache can be cleared
- [x] T008 Run `uv run pytest tests/test_cache.py -v` and verify all cache tests pass

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Search Upcoming Events (Priority: P1) MVP

**Goal**: Users can search Tekna events with filters and get event details

**Independent Test**: Call `search_events` with various filters via MCP Inspector; call `get_event_details` with an event number

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T009 [P] [US1] Test that `search_events` with no filters returns a paginated list of events with title, date, location, price, format, and URL in tests/test_events.py (mock httpx to return tests/fixtures/events_response.json)
- [x] T010 [P] [US1] Test that `search_events` with region filter builds correct DSL query string containing `:regiondigital=<value>` in tests/test_events.py
- [x] T011 [P] [US1] Test that `search_events` with query parameter builds DSL containing `:query=<value>` in tests/test_events.py
- [x] T011b [P] [US1] Test that `search_events` with event_format filter ("in-person" or "digital") builds correct DSL query in tests/test_events.py
- [x] T012 [P] [US1] Test that `search_events` returns pagination info (page, total_pages, total_items) in tests/test_events.py
- [x] T013 [P] [US1] Test that `search_events` returns empty list with clear message when no events match filters in tests/test_events.py
- [x] T014 [P] [US1] Test that `search_events` returns MCP error with isError when upstream API fails (HTTP 500) in tests/test_events.py
- [x] T015 [P] [US1] Test that `get_event_details` returns full event details (description, speakers, agenda, prices, enrollment status, URL) for a given event number in tests/test_events.py
- [x] T016 [P] [US1] Test that `get_event_details` returns MCP error when event not found in tests/test_events.py
- [x] T017 [P] [US1] Test that all URLs in event responses are absolute (start with `https://www.tekna.no`) in tests/test_events.py

### Implementation for User Story 1

- [x] T018 [US1] Create src/mcp_tekna/events.py with `search_events` tool: accepts query, region, field_of_study, price_group, language, target_audience, event_format, page, page_size parameters; builds the colon-separated DSL query (`q=course:format=full:pageSize=N:pagenumber=N:...`); calls TeknaClient; maps API filter values (e.g., price_group "free" → `pricegroup=0`, target_audience "student" → `searchtargetgroup=1`, event_format "in-person" → EventFormat=1, "digital" → EventFormat=2); parses response from `Courses.Items` and `Courses.Paging`; formats results using models.py; returns text content with pagination info
- [x] T019 [US1] Add `get_event_details` tool to src/mcp_tekna/events.py: accepts event_number; calls `search_events` API with `query=<event_number>:pageSize=1`; returns full details using `format_event_details()` including speakers, agenda, all pricing tiers, enrollment status, and capacity
- [x] T020 [US1] Register `search_events` and `get_event_details` tools in src/mcp_tekna/server.py by importing from events.py
- [x] T021 [US1] Run `uv run pytest tests/test_events.py -v` and verify all US1 tests pass
- [x] T022 [US1] Test `search_events` and `get_event_details` with MCP Inspector (`npx @modelcontextprotocol/inspector uv run mcp-tekna`) against live Tekna API

**Checkpoint**: Event search and details tools functional. MVP complete.

---

## Phase 4: User Story 2 - Browse Tekna News (Priority: P2)

**Goal**: Users can fetch recent Tekna news articles with optional content type filtering

**Independent Test**: Call `get_news` via MCP Inspector with and without content_type filter

### Tests for User Story 2

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T023 [P] [US2] Test that `get_news` with no filters returns a list of articles with title, date, summary, content_type, and URL in tests/test_news.py (mock httpx to return tests/fixtures/news_response.json)
- [x] T024 [P] [US2] Test that `get_news` with content_type filter sends correct ContentTypes value in POST body in tests/test_news.py
- [x] T025 [P] [US2] Test that `get_news` returns pagination info and HasMore indicator in tests/test_news.py
- [x] T026 [P] [US2] Test that `get_news` returns MCP error with isError when upstream API fails in tests/test_news.py
- [x] T027 [P] [US2] Test that all URLs in news responses are absolute (start with `https://www.tekna.no`) in tests/test_news.py

### Implementation for User Story 2

- [x] T028 [US2] Create src/mcp_tekna/news.py with `get_news` tool: accepts content_type, page, page_size parameters; builds POST body with ParentLink="314", PageTypes string, Page, PageSize, ContentTypes; calls TeknaClient POST method; parses response Items and HasMore; formats results using models.py; returns text content with pagination info
- [x] T029 [US2] Register `get_news` tool in src/mcp_tekna/server.py by importing from news.py
- [x] T030 [US2] Run `uv run pytest tests/test_news.py -v` and verify all US2 tests pass
- [x] T031 [US2] Test `get_news` with MCP Inspector against live Tekna API

**Checkpoint**: News tool functional. Events + News available.

---

## Phase 5: User Story 3 - View Member Benefits (Priority: P3)

**Goal**: Users can list all Tekna member benefits with categories

**Independent Test**: Call `get_member_benefits` via MCP Inspector and verify all known benefits are returned

### Tests for User Story 3

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T032 [P] [US3] Test that `get_member_benefits` returns benefits organized by category (core and partner) with name, description, and URL in tests/test_benefits.py (mock httpx to return tests/fixtures/benefits_page.html)
- [x] T033 [P] [US3] Test that `get_member_benefits` returns MCP error when upstream request fails in tests/test_benefits.py
- [x] T034 [P] [US3] Test that `get_member_benefits` returns clear error when HTML structure is unrecognizable (empty/malformed HTML) in tests/test_benefits.py
- [x] T035 [P] [US3] Test that all URLs in benefits responses are absolute (start with `https://www.tekna.no`) in tests/test_benefits.py

### Implementation for User Story 3

- [x] T036 [US3] Create src/mcp_tekna/benefits.py with `get_member_benefits` tool: fetches HTML from `/medlemsfordeler/`; parses with BeautifulSoup; extracts core benefits and partner benefits sections; returns each benefit with name, description, category, and absolute URL using models.py formatting
- [x] T037 [US3] Register `get_member_benefits` tool in src/mcp_tekna/server.py by importing from benefits.py
- [x] T038 [US3] Run `uv run pytest tests/test_benefits.py -v` and verify all US3 tests pass
- [x] T039 [US3] Test `get_member_benefits` with MCP Inspector against live Tekna website

**Checkpoint**: All three data tools functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Full validation, error handling verification, and documentation

- [x] T040 [P] Remove the placeholder `ping` tool from src/mcp_tekna/server.py (replaced by real tools)
- [x] T041 [P] Update .env.example to document TEKNA_TIMEOUT and TEKNA_CACHE_TTL environment variables
- [x] T042 [P] Update README.md to document the 4 MCP tools with usage examples
- [x] T043 Run full test suite with coverage: `uv run pytest tests/ -v --cov=mcp_tekna --cov-fail-under=80` and verify all tests pass with >=80% coverage
- [x] T044 Run `uv run ruff check . && uv run ruff format --check .` and fix any issues
- [x] T045 Validate all 4 tools end-to-end via MCP Inspector against live Tekna API: search_events (with and without filters), get_event_details, get_news, get_member_benefits

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can proceed sequentially in priority order (P1 → P2 → P3)
  - Or in parallel since they touch different files (events.py, news.py, benefits.py)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational - No dependencies on US1
- **User Story 3 (P3)**: Can start after Foundational - No dependencies on US1/US2

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Implementation uses shared tekna_client.py and models.py from Foundational
- Tool registration in server.py is last step (depends on tool implementation)
- MCP Inspector validation is final verification per story

### Parallel Opportunities

- T002, T003, T004 can run in parallel (Setup phase - different files)
- T007 can run in parallel with T006 (different files)
- T009-T017 can all run in parallel (US1 tests - same file but independent test classes)
- T023-T027 can all run in parallel (US2 tests)
- T032-T035 can all run in parallel (US3 tests)
- T040, T041, T042 can run in parallel (Polish phase - different files)

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T008)
3. Complete Phase 3: User Story 1 (T009-T022)
4. **STOP and VALIDATE**: Test event tools via MCP Inspector
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test event tools → MVP!
3. Add User Story 2 → Test news tool → Events + News
4. Add User Story 3 → Test benefits tool → All tools complete
5. Polish → Full validation + documentation

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Tests MUST fail before implementing (constitution principle I)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- The events API uses a colon-separated DSL (q=course:key=value), NOT standard query params
- The news API is POST (not GET), requires specific body with ParentLink and PageTypes
- Member benefits require HTML parsing (no API available)
