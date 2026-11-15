# Requirements traceability

Status: **Implemented** (built and, where noted, tool-tested) · **Partial** (built with environment limits) · **Documented-only** (specified, not built) · **Unverified-behaviour** means Claude's runtime behaviour has not been tested (see `evals/test-cases.md`, NOT RUN).

## Spec sections

| Spec § | Requirement | Where | Status |
|---|---|---|---|
| 1 | Product definition and principles | SKILL.md, README | Implemented (behaviour unverified) |
| 2 | Four owner contexts | `references/onboarding.md`, `ios.py init` | Implemented |
| 3 | Naming, rename, identity, separation from owner | onboarding §2, `rename`, config `os` | Implemented (behaviour unverified) |
| 4 | Onboarding sequence, natural questions, two routes, approval | onboarding.md | Implemented (behaviour unverified) |
| 5 | 10 templates, 3 at setup, preserve data, presets, responsive, custom via description | `render_dashboard.py`, `templates/README.md`, `ios.py template` | Partial: static layouts only, no drag/resize; overflow-checked in Chromium (see validation report) |
| 6 | Navigation, Quick Capture, command bar, universal search, saved views/workspaces | SKILL.md §4b, `search`, `workspace` | Partial (command bar is instruction-level) |
| 7 | Module types, standard spec, lifecycle | `module-spec-format.md`, `ios.py module` | Implemented (tool-tested) |
| 8 | 10 x 10 catalogue; cap of 15 | `catalogue/`, `modules.json` | Implemented (tool-tested; names verified against spec) |
| 9 | Universal taxonomy; distinguished counts | discovery-method §3, §10; `run`; `discovery` | Implemented (tool-tested) |
| 10 | Discovery methodology incl. Startup Gap Finder, Job Finder | discovery-method; catalogue 02, 01 | Implemented (behaviour unverified) |
| 11 | Tracking and Quick Capture, IDs, history | tracking-quick-capture; `record` | Implemented (tool-tested); voice not provided |
| 12 | Goals centre | goals-actions-decisions §1; `goal` | Implemented |
| 13 | Action Centre | same §2; `action` | Implemented; reminders not provided |
| 14 | Analysis Centre, standard report | analysis-centre; `analyse` | Implemented (aggregation tool-tested; interpretation unverified) |
| 15 | Collaboration, permissions, workflows | collaboration-workflows; `permission` | Partial: permissions stored and checked by instruction; workflows are definitions, no unattended execution |
| 16 | Evidence, confidence, source health, depth | discovery-method §4-7; `source health` | Implemented (tool-tested) |
| 17 | Library and file organisation | library-exports-portability | Partial: state pack, not a cloud drive |
| 18 | Decision log, histories | goals-actions-decisions §3-4; `decision`, `versions` | Implemented |
| 19 | Alerts | admin §5 | Partial: evaluated in-session; no delivery integrations |
| 20 | Profile & Context Centre, field permissions | `profile`, `permission` | Implemented |
| 21 | Search, command bar, workspaces | `search`, `workspace` | Partial |
| 22 | Administration Centre, Run Centre | admin-versioning-rollback | Partial: run controls are instruction-level; no scheduling |
| 23 | Data model and integrity | `ios.py` records, versions, validate | Implemented (tool-tested) |
| 24 | Exports and portability | `export`, `render` | Partial: CSV, XLSX, config, HTML; no PDF/PPT/Word; no import of edited workbooks |
| 25 | Security and privacy | security-governance; script gates | Implemented; roles not enforced |
| 26 | Client delivery | security-governance §9 | Documented-only |
| 27 | Marketplace | module-spec-format §7 | Documented-only (extension format) |
| 28 | Capability boundaries | architecture-capability-boundary | Implemented |
| 29 | Testing | evals/ | Partial: tooling tested; behavioural NOT RUN |
| 30 | Open decisions documented | docs/decision-log.md | Implemented |
| 31 | Success criteria | all | Not measured |

## Build prompt principles (1-14) and outputs
| # | Principle | Evidence |
|---|---|---|
| 1-2 | Claude-native, no API key | SKILL.md header; no API code anywhere |
| 3-4 | Natural personalisation, inference proposed for approval | onboarding §4-6 |
| 5 | Four contexts | `CONTEXTS` in ios.py |
| 6 | Catalogue broad, activation selective | modules added only via `module add --confirm` |
| 7-8 | Module types; all centres | catalogue, goals/actions/decisions, alerts, search |
| 9 | Controlled collaboration | collaboration-workflows |
| 10 | Approval for meaningful changes | `confirm()` gate; test `test_approval_gate_blocks_without_confirm` |
| 11 | Never fabricate | SKILL.md §5; `run` count checks; source health restricted to real statuses |
| 12 | Manual capture avoids AI | deterministic `record add` |
| 13 | Provenance, IDs, edits, history | records, field_origin, edit_history |
| 14 | Portability | state pack schema, config export |

| Required output | Location | Status |
|---|---|---|
| Installable package | `intelligence-os.zip` | Built; install in a live Claude NOT tested |
| SKILL.md + references | root, `references/` | Done |
| README | `README.md` | Done |
| Onboarding and user guides | `references/onboarding.md`, `docs/user-guide.md` | Done |
| Architecture / capability boundary | `references/architecture-capability-boundary.md` | Done |
| Module catalogue + extensible format | `references/catalogue/`, `module-spec-format.md` | Done |
| Examples (marked illustrative) | `examples/` | Done |
| Test plan, cases, validation report | `evals/` | Done (behavioural NOT RUN) |
| Change log, decision log | `CHANGELOG.md`, `docs/decision-log.md` | Done |
