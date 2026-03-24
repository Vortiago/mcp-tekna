"""Response formatting helpers for Tekna data."""

from typing import Any

from mcp_tekna.tekna_client import make_absolute_url

FORMAT_MAP = {1: "In-person", 2: "Digital"}
LANG_MAP = {1: "Norsk", 2: "Engelsk"}
AUDIENCE_MAP = {
    0: "Åpen for alle",
    1: "Kun studenter",
    2: "Kun medlemmer",
    3: "Tekna Ung",
    4: "Tillitsvalgte",
}


def format_event_summary(event: dict[str, Any]) -> str:
    """Format an event dict into a concise human-readable text block."""
    title = event.get("Title", "Unknown")
    start = event.get("StartDate", "TBD")
    end = event.get("EndDate", "")
    region = event.get("Region", "Unknown")
    venue = event.get("VenueName", "")
    town = event.get("VenueTown", "")
    fmt = FORMAT_MAP.get(event.get("EventFormat", 0), "Unknown")
    url = make_absolute_url(event.get("PublicUrl", ""))

    location = ", ".join(filter(None, [venue, town])) or region

    enrolled = event.get("TotalEnrolled", 0)
    max_p = event.get("MaxParticipantsForEvent")
    capacity = f"{enrolled}/{max_p}" if max_p else str(enrolled)

    enrollable = "Open" if event.get("IsEnrollable") else "Closed"

    date_str = start[:10]
    if end and end[:10] != start[:10]:
        date_str += f" to {end[:10]}"

    organizer = event.get("Organizer", {})
    organizer_name = organizer.get("Name", "") if organizer else ""

    audience_label = AUDIENCE_MAP.get(event.get("SearchTargetGroup"))

    lines = [
        f"[{title}]({url})",
        f"  Dato: {date_str}",
        f"  Sted: {location}",
        f"  Format: {fmt} | Region: {region}",
        f"  Påmelding: {enrollable} ({capacity} påmeldt)",
    ]
    if organizer_name:
        lines.append(f"  Arrangør: {organizer_name}")
    if audience_label:
        lines.append(f"  Målgruppe: {audience_label}")
    return "\n".join(lines)


def format_event_details(event: dict[str, Any]) -> str:
    """Format full event details including speakers, agenda, prices."""
    summary = format_event_summary(event)

    parts = [summary, ""]

    description = event.get("Ingress", "")
    if description:
        parts.append(f"**Description**: {description}")
        parts.append("")

    field = event.get("PrimaryFieldOfStudy", {})
    if field and field.get("Name"):
        parts.append(f"**Field of Study**: {field['Name']}")

    organizer = event.get("Organizer", {})
    if organizer and organizer.get("Name"):
        parts.append(f"**Organizer**: {organizer['Name']}")

    sub_organizer = event.get("SubOrganizer")
    if sub_organizer and sub_organizer.get("Name"):
        parts.append(f"**Sub-Organizer**: {sub_organizer['Name']}")

    audience_label = AUDIENCE_MAP.get(event.get("SearchTargetGroup"))
    if audience_label:
        parts.append(f"**Målgruppe**: {audience_label}")

    lang = LANG_MAP.get(event.get("Language", 0), "")
    if lang:
        parts.append(f"**Language**: {lang}")

    deadline = event.get("EnrollmentDeadline")
    if deadline:
        parts.append(f"**Enrollment Deadline**: {deadline[:10]}")

    prices = event.get("Prices", [])
    if prices:
        parts.append("")
        parts.append("**Pricing**:")
        for p in prices:
            available = p.get("IsAvailable")
            avail = " (available)" if available else " (unavailable)"
            name = p.get("Name", "N/A")
            amount = p.get("Amount", 0)
            parts.append(f"  - {name}: {amount:.0f} NOK{avail}")

    speakers = event.get("CourseLecturers", [])
    if speakers:
        parts.append("")
        parts.append("**Speakers**:")
        for s in speakers:
            first = s.get("FirstName", "")
            last = s.get("LastName", "")
            name = " ".join(filter(None, [first, last]))
            title = s.get("JobTitle", "")
            workplace = s.get("Workplace", "")
            info = ", ".join(filter(None, [title, workplace]))
            suffix = f" ({info})" if info else ""
            parts.append(f"  - {name}{suffix}")

    agenda = event.get("CourseAgendas", [])
    if agenda:
        parts.append("")
        parts.append("**Agenda**:")
        for a in agenda:
            parts.append(f"  - {a.get('Name', 'N/A')}")
            if a.get("Description"):
                parts.append(f"    {a['Description']}")

    return "\n".join(parts)


def format_news_article(article: dict[str, Any]) -> str:
    """Format a news article into a human-readable text block."""
    title = article.get("Title", "Unknown")
    date = article.get("StartPublish", "Unknown date")
    summary = article.get("IntroText", "")
    content_type = article.get("Type", "")
    url = make_absolute_url(article.get("Url", ""))

    lines = [
        f"[{title}]({url})",
        f"  Dato: {date}",
        f"  Type: {content_type}",
    ]
    if summary:
        lines.append(f"  {summary}")
    return "\n".join(lines)


def format_member_benefit(benefit: dict[str, Any]) -> str:
    """Format a member benefit into a human-readable text block."""
    name = benefit.get("name", "Unknown")
    description = benefit.get("description", "")
    category = benefit.get("category", "")
    url = make_absolute_url(benefit.get("url", ""))

    lines = [
        f"[{name}]({url}) [{category}]",
    ]
    if description:
        lines.append(f"  {description}")
    return "\n".join(lines)


def _format_price_range(event: dict[str, Any]) -> str:
    """Format price range from prices array."""
    prices = event.get("Prices", [])
    if not prices:
        return "Contact organizer"
    amounts = [p.get("Amount", 0) for p in prices if p.get("IsAvailable")]
    if not amounts:
        return "Contact organizer"
    if len(amounts) == 1:
        return f"{amounts[0]:.0f} NOK"
    return f"{min(amounts):.0f}-{max(amounts):.0f} NOK"
