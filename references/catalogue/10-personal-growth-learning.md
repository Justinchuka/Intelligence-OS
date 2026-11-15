# Personal Growth & Learning

Catalogue module definitions. Each inherits **Base defaults** from `../module-spec-format.md` (depth `standard`, frequency `manual`, no profile or cross-module access until granted, no external side effects, history preserved, CSV/XLSX export). Only module-specific parts are listed. Source names are *candidate source classes*: availability and access must be verified in the live environment, and every run records what was actually reached. Machine-readable mirror: `modules.json`.

## 1. Learning Path Builder  (`learning-path-builder`)

| Item | Definition |
|---|---|
| Type / modes | discovery, analysis (hybrid) |
| Objective | Build a staged learning path toward a stated skill or role. |
| Needs web access | yes (discovery mode) |
| Source classes | course catalogues; syllabi; credential bodies; reading lists |
| Data fields | stage, topic, resource, estimated_effort_by_source, prerequisites, checkpoint |
| Method / framework | Order by prerequisites; cite resources; effort is an estimate; owner approves the path. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Learning outcomes not guaranteed. |

## 2. Skill Gap Analyst  (`skill-gap-analyst`)

| Item | Definition |
|---|---|
| Type / modes | analysis |
| Objective | Compare the owner's skills with a target role or objective. |
| Needs web access | no |
| Source classes | (reads profile and discovery records by permission) |
| Data fields | target, required_skill, owner_level_self_reported, evidence, gap_assessment |
| Method / framework | Use owner-reported levels; mark unknown; recommend options, not verdicts. |
| Output & evidence | Observations / interpretations / recommendations separated; records and IDs used are listed |
| Limitations | Self-reported levels. |

## 3. Course Finder  (`course-finder`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Find courses on a topic with cost, level and format. |
| Needs web access | yes (discovery mode) |
| Source classes | provider pages; course platforms; university catalogues |
| Data fields | course, provider, level, cost, duration, format, accreditation_claim, source_url |
| Method / framework | Verify accreditation claims on the awarding body page. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Quality cannot be verified. |

## 4. Certification Finder  (`certification-finder`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Find certifications and their requirements. |
| Needs web access | yes (discovery mode) |
| Source classes | certifying body pages; exam providers |
| Data fields | certification, body, prerequisites, exam_fee, renewal, validity, source_url |
| Method / framework | Always confirm with the certifying body. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Fees and rules change. |

## 5. Study Tracker  (`study-tracker`)

| Item | Definition |
|---|---|
| Type / modes | tracking, analysis (hybrid) |
| Objective | Log study sessions. |
| Needs web access | no |
| Source classes | (none; user-entered) |
| Data fields | subject, duration, unit_minutes, occurred_at, notes |
| Method / framework | Summarise time by subject and period. |
| Output & evidence | Standard tracking record (value, unit/currency, occurred_at, captured_at, capture_source, edit_history) |
| Limitations | Self-reported time. |

## 6. Habit Tracker  (`habit-tracker`)

| Item | Definition |
|---|---|
| Type / modes | tracking, analysis (hybrid) |
| Objective | Track habits and streaks. |
| Needs web access | no |
| Source classes | (none; user-entered) |
| Data fields | habit, done_bool, date, notes |
| Method / framework | Compute streaks and completion rates from entries; missing days are shown as gaps, not as failures. |
| Output & evidence | Standard tracking record (value, unit/currency, occurred_at, captured_at, capture_source, edit_history) |
| Limitations | Behavioural advice is general only. |

## 7. Fitness & Activity Tracker  (`fitness-activity-tracker`)

| Item | Definition |
|---|---|
| Type / modes | tracking, analysis (hybrid) |
| Objective | Track activity such as steps, runs, workouts. |
| Needs web access | no |
| Source classes | (none; user-entered; connected exports where available) |
| Data fields | activity, value, unit, occurred_at, notes |
| Method / framework | Summaries by period; general educational context only; no diagnosis or medical advice. |
| Output & evidence | Standard tracking record (value, unit/currency, occurred_at, captured_at, capture_source, edit_history) |
| Limitations | Not medical advice; devices not read unless connected. |

## 8. Expense Tracker  (`expense-tracker`)

| Item | Definition |
|---|---|
| Type / modes | tracking, analysis (hybrid) |
| Objective | Track expenses by category, currency and date. |
| Needs web access | no |
| Source classes | (none; user-entered) |
| Data fields | amount, currency, category, occurred_at, merchant_or_note |
| Method / framework | Deterministic totals; never combine currencies without a stored rate. |
| Output & evidence | Standard tracking record (value, unit/currency, occurred_at, captured_at, capture_source, edit_history) |
| Limitations | Not financial advice; do not store card numbers. |

## 9. Reading & Knowledge Tracker  (`reading-knowledge-tracker`)

| Item | Definition |
|---|---|
| Type / modes | tracking, analysis (hybrid) |
| Objective | Track reading and key takeaways. |
| Needs web access | no |
| Source classes | (none; user-entered) |
| Data fields | title, status, progress, takeaway, date |
| Method / framework | Summaries from entries only. |
| Output & evidence | Standard tracking record (value, unit/currency, occurred_at, captured_at, capture_source, edit_history) |
| Limitations | None beyond data entered. |

## 10. Personal Productivity Analyst  (`personal-productivity-analyst`)

| Item | Definition |
|---|---|
| Type / modes | analysis |
| Objective | Analyse productivity from the owner's tracked data. |
| Needs web access | no |
| Source classes | (reads study, habit, activity, action records by permission) |
| Data fields | period, focus_time, completed_actions, patterns, observations |
| Method / framework | Observations vs interpretations separated; no causal claims from correlations. |
| Output & evidence | Observations / interpretations / recommendations separated; records and IDs used are listed |
| Limitations | Limited by recorded data. |
