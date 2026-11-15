# Funding & Financial Support

Catalogue module definitions. Each inherits **Base defaults** from `../module-spec-format.md` (depth `standard`, frequency `manual`, no profile or cross-module access until granted, no external side effects, history preserved, CSV/XLSX export). Only module-specific parts are listed. Source names are *candidate source classes*: availability and access must be verified in the live environment, and every run records what was actually reached. Machine-readable mirror: `modules.json`.

## 1. Grant Finder  (`grant-finder`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Find grants matching the owner's organisation, purpose and location. |
| Needs web access | yes (discovery mode) |
| Source classes | funder websites; government portals; foundation databases |
| Data fields | grant, funder, purpose, amount_range, eligibility, deadline, match_required, source_url |
| Method / framework | Verify eligibility and deadline on the funder's page; flag aggregator-only listings as unverified. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Eligibility interpretation needs owner review; competitiveness unknown. |

## 2. Startup Funding Finder  (`startup-funding-finder`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Find funding programmes for startups: accelerators, grants, competitions, funds. |
| Needs web access | yes (discovery mode) |
| Source classes | accelerator pages; investor programme pages; government schemes |
| Data fields | programme, provider, stage_focus, terms_if_disclosed, equity_or_non_dilutive, deadline, source_url |
| Method / framework | State whether terms (equity, fees) are disclosed; never recommend giving equity without owner's decision. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Terms often negotiable and undisclosed. |

## 3. Business Support Finder  (`business-support-finder`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Find non-financial and financial business support: mentoring, training, services. |
| Needs web access | yes (discovery mode) |
| Source classes | government and enterprise agency pages; chambers; support programmes |
| Data fields | programme, provider, support_type, eligibility, cost, deadline, source_url |
| Method / framework | Confirm on provider page; note region limits. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Availability varies by region and year. |

## 4. Public Funding Monitor  (`public-funding-monitor`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Monitor public funding calls and budgets relevant to the owner. |
| Needs web access | yes (discovery mode) |
| Source classes | official gazettes; ministry and agency portals; procurement notices |
| Data fields | call, authority, amount, eligibility, deadline, status, source_url |
| Method / framework | Use official sources only; mark unofficial reports as unverified. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Language and portal access vary. |

## 5. Competition & Prize Finder  (`competition-prize-finder`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Find competitions and prizes the owner could enter. |
| Needs web access | yes (discovery mode) |
| Source classes | organiser pages; sponsor announcements; platforms |
| Data fields | competition, organiser, theme, prize_if_disclosed, eligibility, deadline, rules_url, source_url |
| Method / framework | Read rules for IP and eligibility; flag entry fees. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Prize payout cannot be verified. |

## 6. Research Funding Finder  (`research-funding-finder`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Find research funding opportunities. |
| Needs web access | yes (discovery mode) |
| Source classes | funder pages; university research offices; grant databases |
| Data fields | call, funder, field, amount, eligibility, deadline, source_url |
| Method / framework | As Grant Finder; record eligibility by applicant type. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Calls are cyclical. |

## 7. Investor Intelligence  (`investor-intelligence`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Research investors relevant to the owner's stage and sector from public information. |
| Needs web access | yes (discovery mode) |
| Source classes | investor sites; portfolio pages; public announcements; databases |
| Data fields | investor, stage_focus, sector_focus, typical_cheque_if_public, portfolio_examples, source_url |
| Method / framework | Use public data only; separate stated thesis from inferred patterns; no private contact scraping. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Public portfolios are incomplete; cheque sizes often estimates. |

## 8. Funding Deadline Tracker  (`funding-deadline-tracker`)

| Item | Definition |
|---|---|
| Type / modes | tracking |
| Objective | Track funding application deadlines the owner is pursuing. |
| Needs web access | no |
| Source classes | (none; user-entered or from discovery records by permission) |
| Data fields | item, funder, deadline, status, materials_needed, owner |
| Method / framework | Compute days remaining from stored dates at session time. |
| Output & evidence | Standard tracking record (value, unit/currency, occurred_at, captured_at, capture_source, edit_history) |
| Limitations | Reminders only if a real scheduler exists. |

## 9. Personal Finance Tracker  (`personal-finance-tracker`)

| Item | Definition |
|---|---|
| Type / modes | tracking, analysis (hybrid) |
| Objective | Track income, spending, savings and debts entered by the owner. |
| Needs web access | no |
| Source classes | (none; user-entered) |
| Data fields | amount, currency, category, occurred_at, account_label, notes |
| Method / framework | Deterministic summaries by period and category; never sum mixed currencies. |
| Output & evidence | Standard tracking record (value, unit/currency, occurred_at, captured_at, capture_source, edit_history) |
| Limitations | Not financial, tax or investment advice; do not store account numbers. |

## 10. Funding Eligibility Analyst  (`funding-eligibility-analyst`)

| Item | Definition |
|---|---|
| Type / modes | analysis |
| Objective | Assess likely fit between the owner profile and funding opportunities. |
| Needs web access | no |
| Source classes | (reads discovery records and profile by permission) |
| Data fields | opportunity_id, criteria, owner_status_per_criterion, fit_assessment, gaps |
| Method / framework | Check criterion by criterion; mark unknowns; no guarantees of award. |
| Output & evidence | Observations / interpretations / recommendations separated; records and IDs used are listed |
| Limitations | Final eligibility is decided by the funder. |
