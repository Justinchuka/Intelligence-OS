# Market & Industry Intelligence

Catalogue module definitions. Each inherits **Base defaults** from `../module-spec-format.md` (depth `standard`, frequency `manual`, no profile or cross-module access until granted, no external side effects, history preserved, CSV/XLSX export). Only module-specific parts are listed. Source names are *candidate source classes*: availability and access must be verified in the live environment, and every run records what was actually reached. Machine-readable mirror: `modules.json`.

## 1. Industry News Monitor  (`industry-news-monitor`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Track news in the owner's industry. |
| Needs web access | yes (discovery mode) |
| Source classes | trade publications; press; company newsrooms |
| Data fields | headline_summary, publisher, date, relevance, source_url |
| Method / framework | Dedupe syndicated stories; prefer primary reporting. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Paywalls and region blocks. |

## 2. Market Trend Analyst  (`market-trend-analyst`)

| Item | Definition |
|---|---|
| Type / modes | discovery, analysis (hybrid) |
| Objective | Identify and assess market trends with evidence. |
| Needs web access | yes (discovery mode) |
| Source classes | industry reports with disclosed methodology; public datasets; news |
| Data fields | trend, direction, evidence, time_window, strength_rationale, source_url |
| Method / framework | Show data behind each trend; distinguish short-term noise from sustained change; state uncertainty. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Forecasts are not guarantees. |

## 3. Regulatory Change Monitor  (`regulatory-change-monitor`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Track regulation and policy changes affecting the owner. |
| Needs web access | yes (discovery mode) |
| Source classes | regulator sites; official gazettes; legal updates from credible publishers |
| Data fields | instrument, jurisdiction, change, effective_date, affected_area, status, source_url |
| Method / framework | Use official texts; note draft vs in force; no legal advice. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Not legal advice; local counsel should confirm. |

## 4. Market Entry Research  (`market-entry-research`)

| Item | Definition |
|---|---|
| Type / modes | discovery, analysis (hybrid) |
| Objective | Research a new market: size signals, regulation, competitors, customers, channels. |
| Needs web access | yes (discovery mode) |
| Source classes | public statistics; trade bodies; competitor sites; regulator pages |
| Data fields | market, segment, size_signal_with_source, regulation, competitors, channels, risks, confidence |
| Method / framework | Label size figures as sourced estimates; list what is unknown. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Public data is limited in many markets. |

## 5. Demand Signal Monitor  (`demand-signal-monitor`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Watch signals of demand: search interest, discussion, listings, hiring. |
| Needs web access | yes (discovery mode) |
| Source classes | public trend tools; communities; marketplaces |
| Data fields | signal, topic, observed_change, period, source_url |
| Method / framework | Report observed indicators only; avoid converting to volumes unless sourced. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Indicators are proxies. |

## 6. Pricing & Cost Monitor  (`pricing-cost-monitor`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Track prices and input costs for goods and services the owner cares about. |
| Needs web access | yes (discovery mode) |
| Source classes | retail and wholesale listings; commodity indexes; official statistics |
| Data fields | item, price, currency, unit, location, captured_on, source_url |
| Method / framework | Record date, unit and location; do not compare unlike units. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Prices vary by location and time. |

## 7. Supply Chain Intelligence  (`supply-chain-intelligence`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Monitor supply-chain developments affecting the owner. |
| Needs web access | yes (discovery mode) |
| Source classes | logistics news; port and customs notices; supplier announcements |
| Data fields | development, affected_routes_or_goods, date, severity_rationale, source_url |
| Method / framework | Distinguish confirmed disruptions from rumour; avoid forecasting delays without evidence. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Real-time tracking is not provided. |

## 8. Real Estate Intelligence  (`real-estate-intelligence`)

| Item | Definition |
|---|---|
| Type / modes | discovery, analysis (hybrid) |
| Objective | Research property markets from public listings and data. |
| Needs web access | yes (discovery mode) |
| Source classes | public listings; official registries; market reports |
| Data fields | property_or_area, listing_price, currency, size, location, listed_on, source_url |
| Method / framework | Compare like-for-like; flag stale listings and unverified claims. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Not valuation or investment advice. |

## 9. Industry Benchmarking  (`industry-benchmarking`)

| Item | Definition |
|---|---|
| Type / modes | discovery, analysis (hybrid) |
| Objective | Benchmark the owner against industry norms where sourced. |
| Needs web access | yes (discovery mode) |
| Source classes | public reports; filings; industry bodies |
| Data fields | metric, own_value, benchmark_value_with_source, definition_notes, comparability_caveat |
| Method / framework | Check definitions match; state comparability limits. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Benchmarks rarely match the owner's context exactly. |

## 10. Market Risk Monitor  (`market-risk-monitor`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Watch market-level risks: macro, currency, sector shocks. |
| Needs web access | yes (discovery mode) |
| Source classes | central bank and statistics sites; reputable news |
| Data fields | risk, indicator, change, date, implication_note, source_url |
| Method / framework | Report indicator data from official sources; keep implications labelled as interpretation. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | No predictions or investment advice. |
