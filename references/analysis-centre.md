# Analysis Centre

## 1. Inputs
| Choice | Options |
|---|---|
| Module(s) | one module, or a permitted combination (check `permissions.reads_modules`) |
| Period | Today, Yesterday, Last 7 days, Last 30 days, 3 months, 6 months, 1 year, custom, all time |
| Metrics / dimensions | chosen by user, or proposed from the module's data fields |
| Visual | pick by data shape: line/trend (time series), bars (comparison), heatmap (day x hour or category x period), cumulative/area (running totals), timeline (events), table (mixed or sparse) |

Period filtering and aggregation (sum, mean, count, min, max, by day/week/month/category) are deterministic: use `ios.py analyse`. Use AI only for interpretation, and say which parts are AI-written.

## 2. Data sufficiency check (before any conclusion)
Report: records in period, date coverage, gaps (days with no records), units and currencies present, records excluded and why. If coverage is thin (e.g. fewer than ~5 records, or large gaps), say so and limit conclusions. Mixed units or currencies are never summed; show them separately or ask for a conversion rate.

## 3. Standard analysis report (always this order)
1. **Performance Overview**: factual totals and ranges.
2. **Patterns & Trends**: what the data shows over time.
3. **Strengths & Weaknesses**
4. **Insights & Recommendations**
5. **Improvement Plan**: concrete, owner-approved steps; propose actions, never create them silently.

Within sections 1-2 label statements `Observation`; interpretations `Interpretation`; sections 4-5 `Recommendation`. Do not infer causation from correlation. Do not fill gaps with invented records, averages presented as data, or extrapolations presented as facts; a forecast is labelled an estimate with its method.

## 4. Cross-module analysis
Only when the owner initiates it or approves it. List the modules and record IDs that informed the result. Respect permissions. Where records came from discovery agents, keep their confidence labels.

## 5. Output and export
Offer: table in chat, CSV/XLSX export, a rendered HTML dashboard section, a report document. State what was actually generated. Analysis reports are stored as `Analyses/` library items with the parameters used so they can be reproduced.

## 6. Health-related data
General educational context only; no diagnosis, no medication advice; suggest a clinician for concerning values.
