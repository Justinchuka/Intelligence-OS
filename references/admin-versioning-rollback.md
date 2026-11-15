# Administration Centre, versioning, rollback, run controls, alerts

## 1. Administration sections
Dashboard Configuration · Default Features · My Features / Custom Modules · Feature Builder · Source Management · Run Centre · Scanning Instructions · Data & History · Exports & Reports · General Settings · Appearance & Templates · Profile & Permissions · Notifications & Alerts · Backup / Portability. Show only what the environment supports; label the rest "documented, not available here".

## 2. Appearance & Templates
All ten templates become available after setup (see `templates/README.md`). Actions: preview with the owner's data (render), apply, restore previous, save current as custom, create custom from a natural-language description. Switching changes only `config.appearance`; records, modules and history are untouched (`ios.py template set` asserts data hashes unchanged).

## 3. Config versioning and rollback
- Every meaningful change calls `ios.py` which writes `versions/vNNNN.json` and updates `config.json.version`.
- Rollback: `ios.py rollback <version>` restores `config.json` from the snapshot and itself creates a new version (history is never rewritten). Records are not rolled back; only configuration. Say so.
- Always show a diff summary (`ios.py diff <a> <b>`) before confirming rollback.

## 4. Run Centre
Available only for actions that can really run now.
| Control | Behaviour |
|---|---|
| Run All Enabled | run enabled discovery modules sequentially, one run report each |
| Run Selected / Run one | as chosen |
| Depth presets | quick / standard / deep per module |
| Enable / disable | disable stops execution |
| Status & logs | from `logs/runs.jsonl`, real runs only |
Say when a run is long and that usage is drawn from the owner's Claude plan; no exact time/cost promises. Scheduled or background runs are unavailable unless a real mechanism exists; never describe a module as "running in the background".

## 5. Alerts
Types: new matching opportunity, deadline, competitor development, research item, metric threshold, goal slippage, run failure, source problem. Modes: immediate (in-chat when active), daily digest, weekly digest, critical only, in-dashboard. User-defined thresholds are evaluated when data is available in a session. Email/external delivery requires a real connected integration and permission. Provide snooze, mute, thresholds and relevance controls. Alerts are *evaluated at session time*; say so.

## 6. Retention, deletion
Disable/hide keep history. Deleting a source keeps findings. Deleting a custom module archives. Permanent deletion: state exactly what will be removed, require explicit confirmation, log the decision.
