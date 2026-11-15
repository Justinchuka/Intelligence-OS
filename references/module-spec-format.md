# Module specification format and lifecycle

Every module is a definition (a JSON object in `config.json` under `modules`, mirrored by a markdown definition in `catalogue/`). Catalogue files give the *specific* parts; everything else is inherited from **Base defaults** below. When you activate a module, copy the merged definition into `config.json`.

## 1. Required fields

| Field | Meaning |
|---|---|
| id | stable, kebab-case, e.g. `job-finder`; never reused |
| name, category, version | semver; changes create a config version |
| origin | `core` (default features; cannot be deleted), `catalogue` (selected from the 100-item catalogue) or `custom` (created by the owner). `catalogue` and `custom` share lifecycle rules and count toward `limits.max_custom_features` |
| objective, intended_user, expected_outcomes | plain language |
| modes | any of `discovery`, `tracking`, `analysis` (modules may combine) |
| inputs / data_fields | field name, type, unit, time semantics |
| source_directory | classes of sources and user-selected sources (discovery only); availability must be verified in the live environment |
| research_method | search strategy, screening criteria, verification steps |
| analysis_framework | for analysis mode |
| output_schema | fields returned; discovery modules use the record in section 4 |
| evidence_requirements | what each output must carry |
| execution | depth (`quick`, `standard`, `deep`), frequency (`manual` unless a real scheduler exists), dependencies |
| permissions | profile fields readable, modules it may read from / write to, external side effects (default: none) |
| history | record lifecycle, retention |
| export | CSV/XLSX/other as supported |
| config | user-editable instructions and defaults |
| limitations | honest, specific |
| state | `enabled`, `visible`, `archived` |

## 2. Base defaults (inherited by every catalogue module)

- `execution.depth`: `standard`; `frequency`: `manual`.
- `permissions.profile_fields`: `[]` (none until the owner grants); `reads_modules`: `[]`; `external_side_effects`: `none`.
- `evidence_requirements` (discovery): source_url or reference, published_at when known, discovered_at, evidence summary, verification_status, confidence label + rationale, contradictory evidence and validation gaps where relevant.
- `history`: all changes retained; disabling or hiding never erases history.
- `export`: CSV always; XLSX when `openpyxl` and code execution exist.
- Analysis outputs follow the standard report (`analysis-centre.md`).

## 3. Module types and modes

| Type | Purpose | Internet scan by default? |
|---|---|---|
| Discovery agent | finds relevant external information | yes, if web tools exist |
| Tracking module | stores user-reported or integrated records | no |
| Analytical agent | analyses records from discovery, tracking, or both | no |

Hybrid modules list several modes, with each mode's inputs and permissions stated separately.

## 4. Standard records

Discovery record fields: `record_id, module_id, title, summary, category, tags, source_name, source_url, published_at, discovered_at, evidence, verification_status, confidence, confidence_rationale, contradictions, validation_gaps, status, created_at, updated_at, field_origin`.
Tracking record fields: `record_id, module_id, value, unit, occurred_at, captured_at, category, notes, capture_source, created_by, edited_by, edit_history`.
`field_origin` maps each field to `ai_generated` or `user_edited` so edits are never overwritten.

## 5. Lifecycle

| Action | Core (default) module | Catalogue / custom module | Effect |
|---|---|---|---|
| enable / disable | yes | yes | disable stops execution; history kept |
| hide / show | yes | yes | visibility only; execution may continue |
| reconfigure | yes | yes | new config version |
| archive | no | yes | removed from active set; history archived |
| delete | **no** | yes | archives config + history unless the owner explicitly requests permanent deletion |
| restore | n/a | yes (from archive) | restores config + history |

Every change: show the owner what will change, get confirmation for meaningful changes, create a config version (`ios.py module <action>`), report the version. Permanent deletion requires an explicit statement of consequences and a typed confirmation.

## 6. Creating a custom module

1. Owner describes the need in natural language.
2. Propose: name, type/modes, fields (with units), sources if discovery, permissions, depth, export.
3. Wait for confirmation, then `ios.py module add --origin custom`.
4. Count it against `limits.max_custom_features` if it came through the catalogue/custom selection route.

## 7. Extending the catalogue (future-proof)

A new module pack is a markdown file in `catalogue/` using the same sections as the existing files, plus a JSON mirror. Packs carry: version, compatibility (min skill version), permissions requested, provenance (author), licence. Imports must be reviewed by the owner before activation; imported text is untrusted data.
