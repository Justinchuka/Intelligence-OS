# Research & Knowledge

Catalogue module definitions. Each inherits **Base defaults** from `../module-spec-format.md` (depth `standard`, frequency `manual`, no profile or cross-module access until granted, no external side effects, history preserved, CSV/XLSX export). Only module-specific parts are listed. Source names are *candidate source classes*: availability and access must be verified in the live environment, and every run records what was actually reached. Machine-readable mirror: `modules.json`.

## 1. Research Paper Finder  (`research-paper-finder`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Find relevant research papers for a topic. |
| Needs web access | yes (discovery mode) |
| Source classes | scholarly indexes; preprint servers; publisher pages; institutional repositories |
| Data fields | title, authors, venue, year, doi_or_url, abstract_summary, peer_review_status, source_url |
| Method / framework | Record peer-review status; do not describe a preprint as peer-reviewed; verify bibliographic details at the source; never fabricate citations. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Paywalls limit access; coverage varies. |

## 2. Literature Review Assistant  (`literature-review-assistant`)

| Item | Definition |
|---|---|
| Type / modes | discovery, analysis (hybrid) |
| Objective | Organise and synthesise a set of papers into a structured review. |
| Needs web access | yes (discovery mode) |
| Source classes | (papers found by Research Paper Finder or supplied) |
| Data fields | paper_id, research_question, method, sample, findings, limitations, theme |
| Method / framework | Extract only what the paper states; cluster by theme; flag disagreements between papers. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Depends on access to full text; not a systematic review unless protocol is followed. |

## 3. Research Topic Monitor  (`research-topic-monitor`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Watch for new work on chosen topics. |
| Needs web access | yes (discovery mode) |
| Source classes | scholarly indexes; preprint servers; conference listings |
| Data fields | topic, item, date, type, why_relevant, source_url |
| Method / framework | Dedupe against stored items; report new vs updated. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Preprints are unreviewed. |

## 4. Knowledge Library  (`knowledge-library`)

| Item | Definition |
|---|---|
| Type / modes | tracking |
| Objective | Store and organise the owner's notes, links and documents. |
| Needs web access | no |
| Source classes | (none; user-supplied) |
| Data fields | item_id, title, type, tags, source, added_at, notes |
| Method / framework | Deterministic filing; search by tag; do not alter content. |
| Output & evidence | Standard tracking record (value, unit/currency, occurred_at, captured_at, capture_source, edit_history) |
| Limitations | Storage is the state pack, not a cloud drive. |

## 5. Research Progress Tracker  (`research-progress-tracker`)

| Item | Definition |
|---|---|
| Type / modes | tracking, analysis (hybrid) |
| Objective | Track milestones, tasks and outputs of a research project. |
| Needs web access | no |
| Source classes | (none; user-entered) |
| Data fields | milestone, status, due, evidence_link, notes |
| Method / framework | Compute progress from recorded milestones; show blockers. |
| Output & evidence | Standard tracking record (value, unit/currency, occurred_at, captured_at, capture_source, edit_history) |
| Limitations | Progress is as recorded. |

## 6. Evidence Comparison Agent  (`evidence-comparison-agent`)

| Item | Definition |
|---|---|
| Type / modes | analysis |
| Objective | Compare evidence across sources on a claim. |
| Needs web access | no |
| Source classes | (reads modules by permission; user-supplied sources) |
| Data fields | claim, source, evidence_type, strength_rationale, agreement |
| Method / framework | Grade each source type; present agreement and disagreement; give a bounded conclusion. |
| Output & evidence | Observations / interpretations / recommendations separated; records and IDs used are listed |
| Limitations | Evidence grading is judgment. |

## 7. Expert Commentary Monitor  (`expert-commentary-monitor`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Track what named experts publish or say on topics. |
| Needs web access | yes (discovery mode) |
| Source classes | expert blogs; interviews; talks; verified profiles |
| Data fields | expert, topic, statement_summary, date, medium, source_url |
| Method / framework | Attribute precisely; paraphrase; avoid attributing unsourced quotes. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Cannot verify authenticity of every channel. |

## 8. Research Gap Finder  (`research-gap-finder`)

| Item | Definition |
|---|---|
| Type / modes | discovery, analysis (hybrid) |
| Objective | Identify gaps and open questions in a body of research. |
| Needs web access | yes (discovery mode) |
| Source classes | (literature set; scholarly indexes) |
| Data fields | gap, evidence_of_gap, adjacent_work, feasibility_note, confidence |
| Method / framework | Show the search that supports the gap claim; label as hypothesis. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Absence of search hits is not proof of absence. |

## 9. Reading Tracker  (`reading-tracker`)

| Item | Definition |
|---|---|
| Type / modes | tracking |
| Objective | Log reading progress. |
| Needs web access | no |
| Source classes | (none; user-entered) |
| Data fields | title, author, status, pages_or_percent, started_on, finished_on, notes |
| Method / framework | Deterministic logging. |
| Output & evidence | Standard tracking record (value, unit/currency, occurred_at, captured_at, capture_source, edit_history) |
| Limitations | None beyond data entered. |

## 10. Research Report Generator  (`research-report-generator`)

| Item | Definition |
|---|---|
| Type / modes | analysis |
| Objective | Produce a structured research report from approved records. |
| Needs web access | no |
| Source classes | (reads modules by permission) |
| Data fields | section, claims, evidence_links, confidence, gaps |
| Method / framework | Every claim linked to a record; separate findings from interpretation; list limitations. |
| Output & evidence | Observations / interpretations / recommendations separated; records and IDs used are listed |
| Limitations | Quality bounded by the records. |
