# Data Model: Tekna Data Tools

## Event (from Events API)

| Field | Type | Source Field | Description |
|-------|------|-------------|-------------|
| event_number | string | EventNumber | Unique event identifier (e.g., "51691") |
| title | string | Title | Event name |
| subtitle | string | SubTitle | Secondary title |
| description | string | Ingress | Short description text |
| url | string | PublicUrl | Full URL to event page on tekna.no |
| start_date | datetime | StartDate | ISO 8601 start datetime |
| end_date | datetime | EndDate | ISO 8601 end datetime |
| enrollment_deadline | datetime? | EnrollmentDeadline | Registration deadline |
| region | string | Region | Geographic region (Digitalt, Vestlandet, etc.) |
| venue_name | string? | VenueName | Venue name |
| venue_town | string? | VenueTown | Venue city |
| format | string | EventFormat | "in-person" (1) or "digital" (2) |
| is_enrollable | bool | IsEnrollable | Whether registration is open |
| registration_state | int | RegistrationState | Registration status code |
| total_enrolled | int | TotalEnrolled | Current enrollment count |
| max_participants | int? | MaxParticipantsForEvent | Capacity (null if unlimited) |
| is_free | bool | IsFreeOfCharge | Whether event is free |
| prices | Price[] | Prices | Pricing tiers |
| speakers | Speaker[] | CourseLecturers | Event speakers |
| agenda | AgendaItem[] | CourseAgendas | Session agenda |
| organizer | string | Organizer.Name | Organizing body |
| field_of_study | string? | PrimaryFieldOfStudy.Name | Primary topic category |
| language | string | Language | "Norsk" (1) or "Engelsk" (2) |
| target_audience | string | SearchTargetGroup | Target audience code |

### Price

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| amount | float | Amount | Price in NOK |
| name | string | Name | Price tier label |
| is_available | bool | IsAvailable | Whether this tier is bookable |

### Speaker

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| name | string | FirstName + LastName | Full name |
| job_title | string? | JobTitle | Professional title |
| workplace | string? | Workplace | Employer |

### AgendaItem

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| name | string | Name | Session title |
| description | string? | Description | Session description |

## NewsArticle (from News API)

| Field | Type | Source Field | Description |
|-------|------|-------------|-------------|
| title | string | Title | Article headline |
| summary | string | IntroText | Article summary/intro text |
| url | string | Url | Full URL to article on tekna.no |
| content_type | string | Type | Category: Aktuelt, Politisk, etc. |
| published_date | datetime | StartPublishDateTime | ISO 8601 publication date |
| published_display | string | StartPublish | Norwegian formatted date |
| image_url | string? | ListImageUrl | Thumbnail image URL |
| has_video | bool | HasVideo | Whether article contains video |
| has_podcast | bool? | HasPodcast | Whether article contains podcast |

## MemberBenefit (from HTML parsing)

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| name | string | HTML title | Benefit name |
| description | string | HTML text | Benefit description |
| url | string | HTML link | Full URL to detail page |
| image_url | string? | HTML img | Benefit/partner logo URL |
| category | string | Section | "core" or "partner" |

## Filter Enums

### EventRegion
Digital, Nord-Norge, Sorlandet, Trondelag, Vestlandet, Ostlandet

### ContentType
Aktuelt, Tekna magasinet, Rad og tips, Politisk, Working in Norway

### TargetAudience
0=Open, 1=Student, 2=Member, 3=Tekna Ung, 4=Tillitsvalgt

### PriceGroup
0=Free, 1000=Under 1000kr, >1000=Over 1000kr

### EventLanguage
1=Norsk, 2=Engelsk

## Relationships

```text
Event 1──* Price
Event 1──* Speaker
Event 1──* AgendaItem

NewsArticle (standalone)
MemberBenefit (standalone)
```

## Caching

All entities are cached in-memory with 15-minute TTL.
Cache key: (tool_name, serialized_params).
