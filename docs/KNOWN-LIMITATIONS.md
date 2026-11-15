# Known limitations

| Limitation | Detail |
|---|---|
| Not a hosted app | No server, database, auth or standalone UI. |
| Persistence | Only via the state pack you re-upload (or files in a Project if your environment stores them). Nothing is guaranteed across chats otherwise. |
| No background work | No scheduled/unattended runs, no reminders, no email/push alerts, unless your environment offers them (not assumed). Alerts are evaluated when you open a session. |
| Discovery | Needs web search/fetch tools; source names are candidates; access is verified per run; paywalled and login-only sources are out of reach. Results are only as good as retrieval. |
| Voice | Not provided. |
| Dashboard | Static HTML snapshot (tabs/filter only); no drag/resize/rearrange; custom templates are layout specs rendered by Claude-authored changes, not a visual editor. Layouts were checked in headless Chromium for horizontal overflow at 1200px and 375px and three were inspected by eye; Safari/Firefox and real phones were not tested. |
| Import | Re-importing edited spreadsheets is not implemented (documented design only); use the state pack. |
| Multi-user | Roles (owner/admin/editor/viewer) are a design for team/standalone use; not enforced in a single chat. |
| Client Workspace Management, Marketplace | Documented extension points only; not implemented. |
| Number of modules | Catalogue modules are compact definitions (shared base defaults); flagship modules are more detailed than others. |
| Other exports | PDF, PowerPoint, Word are not produced by this Skill; use Claude's document capabilities if present. |
| Testing | Tooling is tested; Claude's behaviour in a fresh install is NOT tested here (see `evals/validation-report.md`). |
