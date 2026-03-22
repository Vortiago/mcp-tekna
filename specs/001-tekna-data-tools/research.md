# Research: Tekna Data Tools

## R1: Events API Structure

**Decision**: Use `GET /api/typeahead/lists?q=course:...&lang=no` with
the colon-separated DSL for all event queries.

**Rationale**: This is the only public events endpoint. It supports
filtering, pagination, free-text search, and returns full event details
including refiners (facets) for dynamic filter discovery.

**Alternatives considered**:
- Scraping the events HTML page: Fragile, slower, less data.
- Using a different endpoint: None available publicly.

**Key facts**:
- Method: GET
- Query DSL: `q=course:key=value:key=value`
- Pagination: `pagenumber` (1-based), `pageSize` (default 10)
- Response wraps in `{ "Courses": { "Paging": {...}, "Items": [...], "Refiners": [...] } }`
- Sort: `orderby=SearchRating-` (descending popularity)
- Free-text search: `query=<text>`

**Correction from spec**: The spec assumed a simpler query format. The
API uses a colon-separated DSL, not standard query parameters.

## R2: Events API Filters

**Decision**: Expose the following filters as MCP tool parameters:
region, target_audience, price_group, language, fields_of_study, query.

**Key facts (filter parameter mapping)**:

| User-facing | DSL parameter | Values |
|-------------|---------------|--------|
| region | `regiondigital` | Digital, Nord-Norge, Sorlandet, Trondelag, Vestlandet, Ostlandet |
| target_audience | `searchtargetgroup` | 0=Open, 1=Student, 2=Member, 3=Tekna Ung, 4=Tillitsvalgt |
| price_group | `pricegroup` | 0=Free, 1000=Under 1000kr, >1000=Over 1000kr |
| language | `language` | 1=Norsk, 2=Engelsk |
| fields_of_study | `fieldsofstudy` | GUIDs (mapped from refiner labels) |
| query | `query` | Free-text string |

**Correction from spec**: `fieldsofstudy` requires GUIDs, not labels.
The server should fetch refiner data to map labels to GUIDs, or accept
GUIDs directly with label-to-GUID lookup.

## R3: Events API Response Fields

**Decision**: Map the following fields from the API to the MCP event
response model.

**Available fields per event item**:
- Identity: `EventNumber`, `PublicUrl`, `Id` (GUID)
- Content: `Title`, `SubTitle`, `Ingress`, `Description` (HTML)
- Timing: `StartDate`, `EndDate`, `EnrollmentDeadline` (ISO 8601)
- Location: `Region`, `VenueName`, `VenueTown`, `District`, `County`
- Format: `EventFormat` (1=in-person, 2=digital)
- Enrollment: `IsEnrollable`, `RegistrationState`, `TotalEnrolled`, `MaxParticipantsForEvent`, `IsWaitingListEnabled`
- Pricing: `IsFreeOfCharge`, `PriceGroup`, `Prices[]` (with Amount, Name, type)
- People: `CourseLecturers[]` (name, title, workplace)
- Agenda: `CourseAgendas[]` (name, description)
- Organization: `Organizer.Name`, `SubOrganizer.Name`
- Categories: `PrimaryFieldOfStudy.Name`, `SearchTargetGroup`

## R4: News API Structure

**Decision**: Use `POST /api/tagsearch/content/feed?lang=nb-NO` with
JSON body for all news queries.

**Rationale**: This is the only public news endpoint. It requires POST
with a specific body structure including ParentLink and PageTypes.

**Alternatives considered**:
- RSS feed: Not available publicly.
- HTML scraping: Fragile, the API is well-structured.

**Correction from spec**: The spec assumed a GET endpoint. It is POST.

**Key facts**:
- Method: POST with `Content-Type: application/json`
- Required body fields: `ParentLink: "314"`, `PageTypes: "CGI.Delegate.Models.Pages.ArticleFeaturePage,CGI.Delegate.Models.Pages.ArticlePage,CGI.Delegate.Models.Pages.NewsArticlePage,CGI.Delegate.Models.Pages.RestrictedArticleFeaturePage,CGI.Delegate.Models.Pages.TeknaMagArticlePage,CGI.Delegate.Models.Pages.VevDesignScrollyTellPage"`
- Pagination: `Page` (1-based) + `PageSize` in body; `HasMore` in response
- Content type filter: `ContentTypes` field in body
- Available types: Aktuelt, Tekna magasinet, Rad og tips, Politisk, Working in Norway

**Response fields per article**:
- `Title`, `IntroText` (summary), `Url` (relative path)
- `Type` (content type label)
- `StartPublish` (display date), `StartPublishDateTime` (ISO 8601)
- `ListImageUrl`, `HasVideo`, `HasPodcast`
- `Lock` (0=public)
- `Tags[]` (GUID array)

## R5: Member Benefits Page

**Decision**: Parse HTML from `GET /medlemsfordeler/` to extract
benefit data. No API is available.

**Rationale**: Benefits are server-rendered static HTML. No JSON API
exists for this data.

**Key facts**:
- Two sections: Core Benefits (6 items) and Partner Benefits (11 items)
- Each benefit has: title, description, URL, image
- No pagination or filtering needed (single page, ~17 items)
- Content changes infrequently
- HTML structure must be monitored for changes

**Risk**: HTML structure changes will break parsing. Mitigate with
clear error messages and defensive parsing.

## R6: Caching Strategy

**Decision**: Use in-memory TTL cache with 15-minute expiry per the spec.

**Rationale**: Reduces upstream load, improves latency. 15 minutes
balances freshness with performance. Events and news update at most
a few times per day.

**Implementation**: Use `cachetools.TTLCache` or a simple dict-based
cache with timestamps. Key by (tool_name, params_hash).

**Alternatives considered**:
- No cache: Higher latency, more upstream load.
- Disk cache: Unnecessary complexity for this scale.
- Redis: Overkill for a single-instance server.

## R7: URL Construction

**Decision**: All URLs must be absolute (prepend `https://www.tekna.no`
to relative paths from the API).

**Key facts**:
- Events API returns `PublicUrl` as absolute path (e.g., `/kurs/51691`)
- News API returns `Url` as relative path (e.g., `/aktuelt/some-article/`)
- Benefits have relative paths from HTML parsing
- Base URL: `https://www.tekna.no`
