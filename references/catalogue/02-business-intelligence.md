# Business Intelligence

Catalogue module definitions. Each inherits **Base defaults** from `../module-spec-format.md` (depth `standard`, frequency `manual`, no profile or cross-module access until granted, no external side effects, history preserved, CSV/XLSX export). Only module-specific parts are listed. Source names are *candidate source classes*: availability and access must be verified in the live environment, and every run records what was actually reached. Machine-readable mirror: `modules.json`.

## 1. Competitor Intelligence  (`competitor-intelligence`)

| Item | Definition |
|---|---|
| Type / modes | discovery, analysis (hybrid) |
| Objective | Track and compare competitors' products, positioning, pricing, hiring and announcements. |
| Needs web access | yes (discovery mode) |
| Source classes | competitor sites; press and blogs; product changelogs; job posts; review sites; filings where public |
| Data fields | competitor, product_or_feature, positioning, pricing_if_public, change_observed, date, source_url |
| Method / framework | Maintain a competitor list the owner approves; log changes versus the prior snapshot; separate confirmed changes from rumours; record contradictions. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Cannot see private data; pricing pages may differ by region. |

## 2. Customer Pain-Point Finder  (`customer-pain-point-finder`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Find recurring customer complaints and unmet needs in a defined market. |
| Needs web access | yes (discovery mode) |
| Source classes | forums; communities; review sites; support threads; social posts |
| Data fields | pain_point, customer_segment, frequency_signal, example_quotes_paraphrased, current_workarounds, source_url |
| Method / framework | Cluster by theme; report frequency as observed counts of sampled sources, not market prevalence; keep quotes short and paraphrased. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Samples are self-selected and biased; frequency is not market size. |

## 3. Startup Gap Finder  (`startup-gap-finder`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Identify plausible product or startup opportunities grounded in real pain points, evidence of demand and gaps in existing solutions. |
| Needs web access | yes (discovery mode) |
| Source classes | Reddit; Google Search; Y Combinator; Product Hunt; G2; Capterra; Crunchbase; Hacker News; user-selected sources (access verified at run time) |
| Data fields | opportunity, target_user, problem, evidence, existing_solutions, recurring_complaints, demand_signals, potential_market, product_direction, competition_differentiation, source_links, confidence, validation_gaps, recommended_next_steps |
| Method / framework | Investigate products gaining traction, recurring complaints, underserved users, broken workflows, weak alternatives, competitor positioning and emerging business models. Do not assert revenue, MRR, profitability or market size without evidence; distinguish verified figures, reported estimates and unverified claims. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Demand signals are indirect; market size estimates are low-confidence unless sourced. |

## 4. Business Model Intelligence  (`business-model-intelligence`)

| Item | Definition |
|---|---|
| Type / modes | discovery, analysis (hybrid) |
| Objective | Document how comparable businesses make money, with evidence. |
| Needs web access | yes (discovery mode) |
| Source classes | company sites; investor materials; filings; credible analyses |
| Data fields | company, model_type, revenue_streams, pricing_structure, cost_drivers, evidence_level, source_url |
| Method / framework | Mark each element as disclosed, reported or inferred; never present inferred economics as fact. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Private company economics are rarely disclosed. |

## 5. Customer Review Intelligence  (`customer-review-intelligence`)

| Item | Definition |
|---|---|
| Type / modes | discovery, analysis (hybrid) |
| Objective | Analyse customer reviews of products or services for themes, sentiment and changes over time. |
| Needs web access | yes (discovery mode) |
| Source classes | review platforms; app stores; marketplace listings |
| Data fields | product, period, review_count_sampled, themes, sentiment_summary, notable_changes, source_url |
| Method / framework | State sample size and platform; avoid generalising beyond the sample; flag suspected fake-review patterns without asserting fraud. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Platforms limit access; review authenticity is uncertain. |

## 6. Pricing Intelligence  (`pricing-intelligence`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Track competitor and market pricing and packaging. |
| Needs web access | yes (discovery mode) |
| Source classes | public pricing pages; marketplace listings; published price lists |
| Data fields | product, plan, price, currency, billing_period, features_included, region, captured_on, source_url |
| Method / framework | Snapshot with date and region; flag prices needing login or quote; compare like-for-like plans only. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Dynamic and personalised pricing may not be visible. |

## 7. Partnership Opportunities  (`partnership-opportunities`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Find potential partners, distributors and collaborators aligned with the owner's objectives. |
| Needs web access | yes (discovery mode) |
| Source classes | industry directories; partner programme pages; event attendee lists; news |
| Data fields | organisation, partnership_type, fit_rationale, contact_route_public, programme_terms_if_public, source_url |
| Method / framework | Verify organisation identity and programme details; do not send outreach (drafts only, owner sends). |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Fit judgments are interpretations; contact information is not collected beyond public routes. |

## 8. Supplier & Vendor Intelligence  (`supplier-vendor-intelligence`)

| Item | Definition |
|---|---|
| Type / modes | discovery |
| Objective | Find and compare suppliers and vendors on stated criteria. |
| Needs web access | yes (discovery mode) |
| Source classes | vendor sites; marketplaces; trade directories; certifications registries |
| Data fields | vendor, offering, location, certifications_claimed, pricing_if_public, lead_time_if_stated, reviews_note, source_url |
| Method / framework | Separate claimed certifications from registry-verified ones; flag missing evidence; never assert reliability without sources. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Quality and reliability cannot be verified remotely. |

## 9. Business Performance Tracker  (`business-performance-tracker`)

| Item | Definition |
|---|---|
| Type / modes | tracking, analysis (hybrid) |
| Objective | Track revenue, costs and operating metrics entered by the owner and analyse performance. |
| Needs web access | no |
| Source classes | (none; user-entered or connected exports) |
| Data fields | metric, value, unit_currency, period, category, notes |
| Method / framework | Aggregate by period; compare to prior periods; show data coverage; never infer missing months. |
| Output & evidence | Standard tracking record (value, unit/currency, occurred_at, captured_at, capture_source, edit_history) |
| Limitations | Accuracy depends entirely on entered data; not accounting or tax advice. |

## 10. Business Risk Monitor  (`business-risk-monitor`)

| Item | Definition |
|---|---|
| Type / modes | discovery, analysis (hybrid) |
| Objective | Watch for developments that threaten the business: regulatory, supplier, market, reputational, security. |
| Needs web access | yes (discovery mode) |
| Source classes | news; regulator pages; industry bulletins; supplier announcements |
| Data fields | risk, category, trigger_event, affected_area, severity_assessment_rationale, date, source_url, recommended_response |
| Method / framework | Rate severity as a labelled judgment with rationale; list sources; separate confirmed events from speculation. |
| Output & evidence | Standard discovery record (source_url, published_at, discovered_at, evidence, verification_status, confidence + rationale, validation gaps) |
| Limitations | Not exhaustive; severity is an interpretation. |
