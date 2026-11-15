# Opportunities & Careers

Catalogue module definitions. Each inherits **Base defaults** from `../module-spec-format.md` (depth `standard`, frequency `manual`, no profile or cross-module access until granted, no external side effects, history preserved, CSV/XLSX export). Only module-specific parts are listed. Source names are *candidate source classes*: availability and access must be verified in the live environment, and every run records what was actually reached. Machine-readable mirror: `modules.json`.

## 1. Job Finder  (`job-finder`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Find current roles that fit the owner's skills, seniority and location or remote preferences. |
| Needs web access | yes (discovery mode) |
| Source classes | job boards; employer career pages; startup hiring signals; recently funded-company hiring pages |
| Data fields | role, employer, location_remote, posted_at, salary_if_disclosed, requirements, seniority, eligibility, application_deadline, source_url |
| Method / framework | Screen by role fit, location/remote status and seniority; open the employer's own page to confirm the listing is live; compare requirements with approved profile fields only if permitted; label stale, expired, uncertain or unverified listings. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Cannot confirm a role is still open beyond the check made; salary is often undisclosed; some boards block automated access. |

## 2. Freelance & Contract Opportunities  (`freelance-contract-opportunities`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Find freelance, contract and gig opportunities matching the owner's skills and availability. |
| Needs web access | yes (discovery mode) |
| Source classes | freelance marketplaces; contract job boards; company project calls; professional communities |
| Data fields | title, client_or_platform, scope, rate_or_budget_if_disclosed, duration, skills_required, posted_at, proposal_deadline, source_url |
| Method / framework | Screen by skill match, rate transparency and client credibility signals; flag unclear scope or advance-fee requests as risks; verify the posting is open. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Client legitimacy cannot be fully verified; rates are often not disclosed. |

## 3. Internship Finder  (`internship-finder`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Find internships fitting the owner's field, level and location. |
| Needs web access | yes (discovery mode) |
| Source classes | employer internship pages; university career portals; internship boards; programme directories |
| Data fields | title, organisation, paid_status_if_disclosed, location_remote, start_date, eligibility, application_deadline, source_url |
| Method / framework | Screen by field, eligibility (student status, year, nationality) and dates; confirm on the organisation's page; flag unpaid status and eligibility limits explicitly. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Eligibility wording can be ambiguous; closing dates change. |

## 4. Apprenticeship Finder  (`apprenticeship-finder`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Find apprenticeship and trainee programmes with clear entry requirements and pathways. |
| Needs web access | yes (discovery mode) |
| Source classes | government apprenticeship portals; employer programme pages; training-provider listings |
| Data fields | programme, employer, trade_or_field, qualification_awarded, entry_requirements, stipend_if_disclosed, intake_dates, application_deadline, source_url |
| Method / framework | Prefer official portals; verify qualification level and funding claims on the source; record country-specific eligibility. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Rules differ by country; some programmes are advertised only through intermediaries. |

## 5. Scholarship Finder  (`scholarship-finder`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Find scholarships the owner may qualify for, with eligibility and deadlines checked against the source. |
| Needs web access | yes (discovery mode) |
| Source classes | scholarship databases; university funding pages; government and foundation award pages |
| Data fields | award, provider, level_of_study, countries_eligible, amount_or_coverage, eligibility_criteria, application_deadline, required_documents, source_url |
| Method / framework | Screen against approved profile fields (level, field, nationality, age) only if permitted; always verify on the provider's own page; mark aggregator-only listings as unverified. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Aggregators lag behind providers; competitiveness cannot be estimated reliably. |

## 6. Fellowship Finder  (`fellowship-finder`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Find fellowships (research, policy, technology, leadership) matching the owner's background. |
| Needs web access | yes (discovery mode) |
| Source classes | foundation and institute fellowship pages; university programmes; professional-body announcements |
| Data fields | fellowship, host, focus_area, stipend_if_disclosed, duration, eligibility, selection_process, application_deadline, source_url |
| Method / framework | Confirm eligibility and selection criteria on the host page; note commitments (location, duration); label unclear terms. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Funding and terms often change by cycle; prior cycle info may be outdated. |

## 7. Volunteer Opportunities  (`volunteer-opportunities`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Find volunteering roles that match the owner's interests, skills and availability. |
| Needs web access | yes (discovery mode) |
| Source classes | non-profit sites; volunteer platforms; community and civic organisation pages |
| Data fields | role, organisation, cause, time_commitment, location_remote, skills_needed, start_date, contact_route, source_url |
| Method / framework | Verify the organisation exists and the role is current; note commitment and any fees (flag paid-to-volunteer schemes as a risk). |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Organisation legitimacy checks are limited to public information. |

## 8. Hackathon Finder  (`hackathon-finder`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Find hackathons and build competitions by theme, format and prize. |
| Needs web access | yes (discovery mode) |
| Source classes | hackathon platforms; developer community pages; sponsor announcements |
| Data fields | event, organiser, theme, format_online_in_person, dates, prizes_if_disclosed, eligibility, registration_deadline, source_url |
| Method / framework | Confirm dates and rules on the organiser's page; separate announced prizes from claimed ones; flag unclear IP terms. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Prize payouts and judging cannot be verified. |

## 9. Research Openings  (`research-openings`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Find research positions, studentships and calls aligned with the owner's research interests. |
| Needs web access | yes (discovery mode) |
| Source classes | university vacancy pages; research institute sites; academic job boards; lab pages |
| Data fields | position, institution, field, funding_status, supervisor_or_lab, requirements, application_deadline, source_url |
| Method / framework | Prefer institution pages; record funding status explicitly; match to research interests supplied by the owner. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Funding may be conditional; lab pages are often stale. |

## 10. Career Path Intelligence  (`career-path-intelligence`)

| Item | Definition |
|---|---|
| Type / modes | discovery, analysis (hybrid) |
| Objective | Map plausible career paths from the owner's background: roles, skills, typical transitions and market signals. |
| Needs web access | yes (discovery mode) |
| Source classes | job market data pages; professional-body publications; role descriptions; salary surveys with disclosed methodology |
| Data fields | path, target_role, required_skills, typical_entry_routes, demand_signals, compensation_range_with_source, evidence_notes |
| Method / framework | Use multiple sources for each claim; separate observed postings from published reports; present paths as options, not predictions. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Career outcomes are uncertain; salary data is often self-reported. |
