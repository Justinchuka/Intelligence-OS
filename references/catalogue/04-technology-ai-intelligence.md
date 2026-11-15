# Technology & AI Intelligence

Catalogue module definitions. Each inherits **Base defaults** from `../module-spec-format.md` (depth `standard`, frequency `manual`, no profile or cross-module access until granted, no external side effects, history preserved, CSV/XLSX export). Only module-specific parts are listed. Source names are *candidate source classes*: availability and access must be verified in the live environment, and every run records what was actually reached. Machine-readable mirror: `modules.json`.

## 1. AI Developments Monitor  (`ai-developments-monitor`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Track notable AI research, model, policy and product developments. |
| Needs web access | yes (discovery mode) |
| Source classes | lab and company blogs; research repositories; reputable news; regulator pages |
| Data fields | development, organisation, date, summary, significance_rationale, source_url |
| Method / framework | Prefer primary announcements; mark claims as reported vs demonstrated; avoid benchmark claims without sources. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Fast-moving; benchmark comparisons can be misleading. |

## 2. AI Tool Finder  (`ai-tool-finder`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Find AI tools for a stated task and compare them. |
| Needs web access | yes (discovery mode) |
| Source classes | tool directories; vendor sites; documentation; independent reviews |
| Data fields | tool, use_case, pricing_if_public, data_handling_notes, integrations, limitations, source_url |
| Method / framework | Verify pricing and terms on vendor pages; record privacy terms; do not endorse without evidence. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Tools change quickly; hands-on testing is not performed. |

## 3. Open-Source Technology Monitor  (`open-source-technology-monitor`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Monitor releases and trends in chosen open-source technologies. |
| Needs web access | yes (discovery mode) |
| Source classes | project repositories; release notes; maintainer blogs |
| Data fields | project, version, release_date, notable_changes, breaking_changes, source_url |
| Method / framework | Read release notes at the source; flag breaking changes; do not assert adoption without data. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Not a security audit. |

## 4. Developer Ecosystem Monitor  (`developer-ecosystem-monitor`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Track developer tooling, frameworks, communities and platform changes. |
| Needs web access | yes (discovery mode) |
| Source classes | platform changelogs; developer surveys; community discussions |
| Data fields | item, ecosystem, change, date, impact_note, source_url |
| Method / framework | Distinguish official announcements from community opinion; cite survey methodology where used. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Survey results reflect their respondents. |

## 5. Emerging Technology Radar  (`emerging-technology-radar`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Track emerging technologies and classify them by readiness for the owner's context. |
| Needs web access | yes (discovery mode) |
| Source classes | research news; standards bodies; industry reports |
| Data fields | technology, readiness_estimate, use_cases, risks, evidence, source_url |
| Method / framework | Label readiness as an estimate with rationale; avoid hype. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Estimates are subjective. |

## 6. AI Workflow Research  (`ai-workflow-research`)

| Item | Definition |
|---|---|
| Type / modes | discovery, analysis (hybrid) |
| Objective | Research and document practical AI workflows for a given job. |
| Needs web access | yes (discovery mode) |
| Source classes | practitioner write-ups; tool docs; case studies |
| Data fields | workflow, steps, tools_involved, reported_results, limitations, source_url |
| Method / framework | Separate reported results from tested ones; note data-privacy considerations. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Reported results may not generalise. |

## 7. Cybersecurity Developments Monitor  (`cybersecurity-developments-monitor`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Track vulnerabilities, advisories and threat developments relevant to the owner's stack. |
| Needs web access | yes (discovery mode) |
| Source classes | vendor security advisories; national CERT pages; reputable security news |
| Data fields | advisory_id, affected_products, severity_as_published, published_at, mitigation_summary, source_url |
| Method / framework | Report severity as published by the source; link advisories; never provide exploit instructions; recommend patching via official guidance. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Not a substitute for a security team; no scanning of owner systems. |

## 8. Software Release Monitor  (`software-release-monitor`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Track releases of software the owner depends on. |
| Needs web access | yes (discovery mode) |
| Source classes | release pages; changelogs; package registries |
| Data fields | software, version, release_date, highlights, breaking_changes, end_of_life_dates, source_url |
| Method / framework | Use official release pages; record EOL from the vendor only. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Not an update installer. |

## 9. Technical Standards Monitor  (`technical-standards-monitor`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Track changes to technical standards and specifications. |
| Needs web access | yes (discovery mode) |
| Source classes | standards body pages; working-group drafts |
| Data fields | standard, status, version, change_summary, effective_date, source_url |
| Method / framework | Cite the standards body; note draft vs published status. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Access to full texts may be paid. |

## 10. Technology Adoption Tracker  (`technology-adoption-tracker`)

| Item | Definition |
|---|---|
| Type / modes | tracking, analysis (hybrid) |
| Objective | Track the owner's own technology adoption decisions and outcomes. |
| Needs web access | no |
| Source classes | (none; user-entered) |
| Data fields | technology, decision, date, rationale, outcome_note, review_date |
| Method / framework | Record decisions and outcomes; analyse patterns across entries only. |
| Output & evidence | Standard tracking record (value, unit/currency, occurred_at, captured_at, capture_source, edit_history) |
| Limitations | Reflects the owner's records only. |
