# Events & Communities

Catalogue module definitions. Each inherits **Base defaults** from `../module-spec-format.md` (depth `standard`, frequency `manual`, no profile or cross-module access until granted, no external side effects, history preserved, CSV/XLSX export). Only module-specific parts are listed. Source names are *candidate source classes*: availability and access must be verified in the live environment, and every run records what was actually reached. Machine-readable mirror: `modules.json`.

## 1. Conference Finder  (`conference-finder`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Find conferences by topic, location and date. |
| Needs web access | yes (discovery mode) |
| Source classes | organiser sites; event directories |
| Data fields | event, dates, location_or_online, topics, ticket_price_if_public, cfp_deadline, source_url |
| Method / framework | Confirm dates on the organiser site; flag cancelled or unverified events. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Events change; pricing may be partial. |

## 2. Webinar Finder  (`webinar-finder`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Find webinars on chosen topics. |
| Needs web access | yes (discovery mode) |
| Source classes | platform listings; organiser pages |
| Data fields | title, host, datetime_with_timezone, registration_url, cost, source_url |
| Method / framework | Record time zone clearly. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Time and access may change. |

## 3. Meetup Finder  (`meetup-finder`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Find meetups near the owner or online. |
| Needs web access | yes (discovery mode) |
| Source classes | meetup platforms; community pages |
| Data fields | group, next_event, location, frequency, source_url |
| Method / framework | Use the owner's approved location preference. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Location precision depends on supplied preference. |

## 4. Community Discovery  (`community-discovery`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Discover online and local communities aligned with the owner's interests. |
| Needs web access | yes (discovery mode) |
| Source classes | platform directories; forums; community lists |
| Data fields | community, platform, size_as_displayed, activity_signal, rules_note, source_url |
| Method / framework | Assess activity from visible recency; avoid joining on the owner's behalf. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Activity is approximate. |

## 5. Hackathon Calendar  (`hackathon-calendar`)

| Item | Definition |
|---|---|
| Type / modes | tracking, discovery (hybrid) |
| Objective | Maintain a calendar of hackathons the owner follows. |
| Needs web access | yes (discovery mode) |
| Source classes | hackathon platforms; owner-entered |
| Data fields | event, dates, status, team, source_url |
| Method / framework | Merge discovered and owner-added; keep user edits. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Dates may change. |

## 6. Industry Exhibition Finder  (`industry-exhibition-finder`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Find trade shows and exhibitions. |
| Needs web access | yes (discovery mode) |
| Source classes | exhibition organiser pages; trade bodies |
| Data fields | event, venue, dates, sector, visitor_registration_terms, source_url |
| Method / framework | Confirm with organiser; note costs. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Prices vary. |

## 7. Competition Calendar  (`competition-calendar`)

| Item | Definition |
|---|---|
| Type / modes | tracking, discovery (hybrid) |
| Objective | Calendar of competitions the owner follows. |
| Needs web access | yes (discovery mode) |
| Source classes | organiser pages; owner-entered |
| Data fields | competition, deadline, status, materials, source_url |
| Method / framework | As Hackathon Calendar. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Dates may change. |

## 8. Event Deadline Tracker  (`event-deadline-tracker`)

| Item | Definition |
|---|---|
| Type / modes | tracking |
| Objective | Track event registration and submission deadlines. |
| Needs web access | no |
| Source classes | (none; user-entered or from discovery records) |
| Data fields | event, deadline_type, deadline, status |
| Method / framework | Compute days left at session time. |
| Output & evidence | Standard tracking record (value, unit/currency, occurred_at, captured_at, capture_source, edit_history) |
| Limitations | No reminders without a real scheduler. |

## 9. Event Participation Tracker  (`event-participation-tracker`)

| Item | Definition |
|---|---|
| Type / modes | tracking, analysis (hybrid) |
| Objective | Log events attended and outcomes. |
| Needs web access | no |
| Source classes | (none; user-entered) |
| Data fields | event, date, role, outcomes, contacts_made_ref, notes |
| Method / framework | Summarise participation over time. |
| Output & evidence | Standard tracking record (value, unit/currency, occurred_at, captured_at, capture_source, edit_history) |
| Limitations | Only recorded events. |

## 10. Community Activity Monitor  (`community-activity-monitor`)

| Item | Definition |
|---|---|
| Type / modes | discovery, analysis (hybrid) |
| Objective | Observe public activity of chosen communities. |
| Needs web access | yes (discovery mode) |
| Source classes | public community pages and feeds |
| Data fields | community, period, activity_observed, notable_threads, source_url |
| Method / framework | Report observations from public pages only; cite recency. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | No private-channel access. |
