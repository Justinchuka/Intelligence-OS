# Product & Innovation

Catalogue module definitions. Each inherits **Base defaults** from `../module-spec-format.md` (depth `standard`, frequency `manual`, no profile or cross-module access until granted, no external side effects, history preserved, CSV/XLSX export). Only module-specific parts are listed. Source names are *candidate source classes*: availability and access must be verified in the live environment, and every run records what was actually reached. Machine-readable mirror: `modules.json`.

## 1. Product Discovery Research  (`product-discovery-research`)

| Item | Definition |
|---|---|
| Type / modes | discovery, analysis (hybrid) |
| Objective | Research user problems and market context to inform what to build. |
| Needs web access | yes (discovery mode) |
| Source classes | communities; interviews supplied by owner; review sites; search trends; competitor pages |
| Data fields | problem, segment, evidence, current_solutions, opportunity_notes, confidence, validation_gaps |
| Method / framework | Triangulate across at least three source types at standard depth; mark hypotheses; propose validation steps. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Cannot replace primary user research. |

## 2. Product Launch Monitor  (`product-launch-monitor`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Track new product launches in a chosen space. |
| Needs web access | yes (discovery mode) |
| Source classes | launch platforms; press; company blogs; changelogs |
| Data fields | product, company, launch_date, category, key_features, pricing_if_public, source_url |
| Method / framework | Log launch dates from the source; dedupe re-announcements; label rumours. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Coverage depends on sources reachable. |

## 3. Feature Gap Finder  (`feature-gap-finder`)

| Item | Definition |
|---|---|
| Type / modes | discovery, analysis (hybrid) |
| Objective | Compare product features against alternatives and user requests to find gaps. |
| Needs web access | yes (discovery mode) |
| Source classes | product docs; pricing pages; changelogs; feature-request forums |
| Data fields | feature, own_product_status, competitors_offering, user_demand_signal, gap_assessment, source_url |
| Method / framework | Build a feature matrix from sources; mark unknown cells explicitly; interpret gaps as hypotheses. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Documentation may lag the real product. |

## 4. UX Research Intelligence  (`ux-research-intelligence`)

| Item | Definition |
|---|---|
| Type / modes | discovery, analysis (hybrid) |
| Objective | Gather UX patterns, studies and usability findings relevant to the owner's product. |
| Needs web access | yes (discovery mode) |
| Source classes | UX publications; research articles; case studies; conference talks |
| Data fields | finding, context, method_described, sample_if_stated, applicability_note, source_url |
| Method / framework | Report method and sample from the source; flag weak evidence; do not generalise beyond the study. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Findings are context-dependent. |

## 5. Open-Source Project Opportunities  (`open-source-project-opportunities`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Find open-source projects to use, contribute to, or learn from. |
| Needs web access | yes (discovery mode) |
| Source classes | code hosting platforms; project directories; contributor guides |
| Data fields | project, language, licence, activity_signals, good_first_issue_signal, maintainer_responsiveness_note, source_url |
| Method / framework | Check licence and recent activity on the project page; do not judge code quality without inspection; note governance. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Activity metrics do not equal health. |

## 6. Product Feedback Analysis  (`product-feedback-analysis`)

| Item | Definition |
|---|---|
| Type / modes | tracking, analysis (hybrid) |
| Objective | Analyse feedback the owner provides or imports (tickets, surveys, reviews). |
| Needs web access | no |
| Source classes | (none; user-supplied feedback) |
| Data fields | feedback_id, source_channel, date, text, segment, sentiment_tag, theme_tag |
| Method / framework | Cluster themes; report counts per theme; quote briefly; never infer from data not supplied. |
| Output & evidence | Standard tracking record (value, unit/currency, occurred_at, captured_at, capture_source, edit_history) |
| Limitations | Only as representative as the supplied sample. |

## 7. Innovation Radar  (`innovation-radar`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Scan for emerging ideas, technologies and approaches relevant to the owner's domain. |
| Needs web access | yes (discovery mode) |
| Source classes | research feeds; patent and standards announcements; startup news; conference talks |
| Data fields | signal, domain, maturity_estimate, why_relevant, evidence, source_url |
| Method / framework | Label maturity as an estimate with rationale; separate hype from demonstrated adoption. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Early signals are noisy. |

## 8. Product Validation Assistant  (`product-validation-assistant`)

| Item | Definition |
|---|---|
| Type / modes | analysis |
| Objective | Help design and evaluate validation of a product idea using owner-supplied data and discovered evidence. |
| Needs web access | no |
| Source classes | (reads other modules by permission) |
| Data fields | hypothesis, assumption, evidence_for, evidence_against, test_proposed, result, decision |
| Method / framework | Structure assumptions; propose cheapest tests; record outcomes honestly; never claim validation without evidence. |
| Output & evidence | Observations / interpretations / recommendations separated; records and IDs used are listed |
| Limitations | Validation needs real-world tests this module cannot run. |

## 9. Design Pattern Research  (`design-pattern-research`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Collect design patterns and examples with sources and context of use. |
| Needs web access | yes (discovery mode) |
| Source classes | design systems documentation; pattern libraries; case studies |
| Data fields | pattern, problem_solved, example_source, context, pros_cons, source_url |
| Method / framework | Cite the source; describe patterns in own words; avoid copying protected assets. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Pattern fit varies by context. |

## 10. Product Roadmap Analyst  (`product-roadmap-analyst`)

| Item | Definition |
|---|---|
| Type / modes | analysis |
| Objective | Analyse a roadmap the owner provides against objectives, evidence and capacity. |
| Needs web access | no |
| Source classes | (none; user-supplied roadmap; may read discovery records by permission) |
| Data fields | item, objective_link, evidence_links, effort_estimate_by_owner, dependency, status |
| Method / framework | Check each item for objective and evidence links; surface orphans and conflicts; recommendations are suggestions. |
| Output & evidence | Observations / interpretations / recommendations separated; records and IDs used are listed |
| Limitations | Effort and priority inputs come from the owner. |
