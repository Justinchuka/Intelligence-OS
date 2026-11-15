# Intelligence Library, exports and portability

## 1. Logical structure (Appendix A of the spec)
```
Intelligence Library/
  Discoveries/ Opportunities/ Research/ Trackers/ Analyses/
  Goals & Actions/ Sources/ Decisions/ Reports/ Exports/
  Configuration/  (module registry, settings, versions)
  Archive/
```
This is a *logical* organisation. Actual folders exist only where the environment provides storage. In the Claude-native edition the physical form is the **state pack** (below) plus any files created in the outputs folder. Do not claim a private cloud drive or permanent database.

## 2. State pack (the persistence mechanism)
`os-state/` (or `os-state.zip`):
| File | Content |
|---|---|
| manifest.json | OS id, name, schema_version, created/updated, file hashes, counts |
| config.json | profile, modules, permissions, limits, template, goals, workflows, sources |
| versions/ | numbered config snapshots (`v0001.json` ...) for rollback |
| records/<module_id>.jsonl | one record per line, stable IDs, edit history |
| actions.jsonl, decisions.jsonl, goals.jsonl | as per `goals-actions-decisions.md` |
| library/ | saved notes, reports, links index (created on demand) |
| archive/ | archived modules (config + history), created on demand |
| logs/runs.jsonl | execution history (only real runs) |

Workflow: at session end give the user the updated state pack as a downloadable file and tell them to upload it at the next session start. If the owner uses a Claude Project, files may be stored there if the environment allows; verify, don't assume. Chat history alone is not durable storage.

## 3. Naming
`YYYY-MM-DD_<module-id>_<slug>.<ext>`; IDs are stable (`rec_<ulid-like>`, `mod_...`, `act_...`).

## 4. Exports (what the script can generate)
| Export | Tool | Condition |
|---|---|---|
| CSV per module | `ios.py export csv` | always (Python available) |
| Excel workbook | `ios.py export xlsx` | `openpyxl` available |
| Config package (module defs, sources, schemas, instructions) | `ios.py export config` | always |
| Dashboard HTML | `ios.py render` | always |
| Migration manifest | included in config/xlsx exports | always |
| PDF, PowerPoint, Word | via the platform's document skills if present | not provided by this skill; say so |
Workbook sheets: Dashboard Overview, Feature Registry, Discoveries, Opportunities, Research, Sources Registry, Scan History, Source Activity, Archived Features, Saved Items, plus a sheet per custom module. The workbook is an editable export surface, **not** the canonical database. Re-import must never silently overwrite user edits: `ios.py import` reports conflicts and applies none without choice.
`export --public` removes owner profile fields, health data, private notes and anything marked sensitive. Review before sharing.

## 5. Standalone portability
The state pack schemas are database-ready (stable IDs, timestamps, provenance). A full standalone product needs: a backend, a database, authentication, object storage, integrations and secrets management, a scheduler/workers, and AI-provider configuration, none of which this skill provides. Never place API keys in frontend code, exports or public repositories. The Claude-native edition never requires API keys.
