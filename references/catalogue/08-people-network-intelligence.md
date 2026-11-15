# People & Network Intelligence

Catalogue module definitions. Each inherits **Base defaults** from `../module-spec-format.md` (depth `standard`, frequency `manual`, no profile or cross-module access until granted, no external side effects, history preserved, CSV/XLSX export). Only module-specific parts are listed. Source names are *candidate source classes*: availability and access must be verified in the live environment, and every run records what was actually reached. Machine-readable mirror: `modules.json`.

## 1. Expert Finder  (`expert-finder`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Find experts on a topic from public professional information. |
| Needs web access | yes (discovery mode) |
| Source classes | publications; conference speaker lists; institutional profiles |
| Data fields | name, affiliation, expertise_evidence, public_contact_route, source_url |
| Method / framework | Use public professional information only; no scraping of private details; verify affiliation. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Public information only; no endorsement. |

## 2. Founder & Investor Monitor  (`founder-investor-monitor`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Track public announcements of founders and investors of interest. |
| Needs web access | yes (discovery mode) |
| Source classes | press; company blogs; official social accounts |
| Data fields | person_or_org, announcement, date, source_url |
| Method / framework | Public statements only; avoid speculation on private matters. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Excludes private personal information. |

## 3. Professional Network Opportunities  (`professional-network-opportunities`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Find communities, groups and introductions routes for professional networking. |
| Needs web access | yes (discovery mode) |
| Source classes | professional associations; community directories; events |
| Data fields | group, focus, membership_terms, location_remote, source_url |
| Method / framework | Verify the group exists and terms; no unsolicited messaging. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Does not send messages. |

## 4. Mentor Finder  (`mentor-finder`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Find mentorship programmes and potential mentors via public routes. |
| Needs web access | yes (discovery mode) |
| Source classes | mentorship platforms; programme pages; alumni networks |
| Data fields | programme_or_person, focus, terms, how_to_apply, source_url |
| Method / framework | Prefer structured programmes; note fees; avoid contacting individuals without owner approval. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Fit and availability unknowable. |

## 5. Speaker & Contributor Opportunities  (`speaker-contributor-opportunities`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Find calls for speakers, authors and contributors. |
| Needs web access | yes (discovery mode) |
| Source classes | conference CFP pages; publication submission pages |
| Data fields | venue, topic_fit, deadline, compensation_if_disclosed, requirements, source_url |
| Method / framework | Confirm CFP deadline on the organiser page. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Acceptance not predictable. |

## 6. Organisation People Tracker  (`organisation-people-tracker`)

| Item | Definition |
|---|---|
| Type / modes | tracking |
| Objective | Track people within an organisation: roles, teams, responsibilities (owner-entered). |
| Needs web access | no |
| Source classes | (none; user-entered) |
| Data fields | person_ref, role, team, start, notes |
| Method / framework | Restrict access; minimise personal data; follow permissions. |
| Output & evidence | Standard tracking record (value, unit/currency, occurred_at, captured_at, capture_source, edit_history) |
| Limitations | Handle personal data carefully; not HR advice. |

## 7. Influencer/Creator Intelligence  (`influencer-creator-intelligence`)

| Item | Definition |
|---|---|
| Type / modes | discovery, analysis (hybrid) |
| Objective | Research creators relevant to the owner's niche from public data. |
| Needs web access | yes (discovery mode) |
| Source classes | public creator profiles; platform pages |
| Data fields | creator, platform, niche, audience_size_as_displayed, content_themes, source_url |
| Method / framework | Label audience numbers as displayed, unaudited; no fraud accusations without evidence. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Metrics can be inflated. |

## 8. Community Member Directory  (`community-member-directory`)

| Item | Definition |
|---|---|
| Type / modes | tracking |
| Objective | Maintain a directory of community members the owner supplies. |
| Needs web access | no |
| Source classes | (none; user-entered) |
| Data fields | member_ref, role, interests, joined_on, consent_note |
| Method / framework | Store only consented, necessary data. |
| Output & evidence | Standard tracking record (value, unit/currency, occurred_at, captured_at, capture_source, edit_history) |
| Limitations | Privacy obligations on the owner. |

## 9. Relationship Follow-up Tracker  (`relationship-follow-up-tracker`)

| Item | Definition |
|---|---|
| Type / modes | tracking |
| Objective | Track follow-ups with contacts. |
| Needs web access | no |
| Source classes | (none; user-entered) |
| Data fields | contact_ref, last_contact, next_step, due, notes |
| Method / framework | Compute overdue follow-ups at session time. |
| Output & evidence | Standard tracking record (value, unit/currency, occurred_at, captured_at, capture_source, edit_history) |
| Limitations | No reminders unless a real mechanism exists; does not send messages. |

## 10. Talent Intelligence  (`talent-intelligence`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Research talent pools and hiring signals for the owner's roles. |
| Needs web access | yes (discovery mode) |
| Source classes | job and talent market data; professional communities; publications |
| Data fields | role, market_signal, skills_trend, location, source_url |
| Method / framework | Use aggregate public signals; avoid profiling individuals. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Aggregate data only. |
