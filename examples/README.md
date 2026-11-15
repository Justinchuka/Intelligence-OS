# Examples (illustrative)

Everything here is **fictional** and exists to show shapes and behaviour. None of it is real data, a real discovery, or a real source check.

| File | What it shows |
|---|---|
| `example-os-state/` | A small state pack for a fictional bakery: config, version snapshots, records, audit log, run log, goal and action |
| `example-dashboard-operations.html` | A static dashboard rendered from that state with the Intelligence — Operations layout (open in a browser) |
| `example-custom-module.json` | A custom tracking module definition (Water Intake) |

Regenerate the dashboard: `python scripts/ios.py render --dir examples/example-os-state --out examples/example-dashboard-operations.html`
