# Architecture and capability boundary

A Skill is an instruction package. It is not a hosted application and does not by itself provide a database, durable cloud folders, always-on execution, scheduling, voice input, email delivery or an independent interactive dashboard.

## 1. Claude-native vs standalone

| Area | Claude-native (this skill) | Full standalone needs |
|---|---|---|
| AI | Claude's in-product access, subject to the owner's plan limits; no API key | AI provider/API configuration |
| Storage | state pack uploaded/downloaded each session; files in outputs; Project files if available | database, object storage, backup |
| Auth | Claude account | app authentication, sessions, roles |
| Scheduling | none by default | scheduler, queue, workers |
| Integrations | only connected tools, with permission | OAuth/API integrations, secrets management |
| Dashboard | conversation tables + generated single-file HTML artefact | full responsive web app |
| Exports | CSV/XLSX/config/HTML via script; others via other tools | export services, persistent storage |

## 2. Dashboard presentation levels (do not conflate)
1. **Conversation**: tables and text blocks.
2. **Generated artefact**: self-contained HTML file from `ios.py render`; static snapshot of the state (no live database), with limited client-side interaction (tabs, filters, search) where the template provides it.
3. **Independent web UI**: not provided; belongs to a future standalone deployment.

## 3. Portability design
State pack = JSON/JSONL with stable IDs, schema version and provenance, so it can be imported into a database. Module definitions are declarative JSON.

## 4. Platform facts to re-verify at install time
Skill packaging and upload conventions change: folder name = `name`; claude.ai description limit 200 characters; ZIP contains the folder; only spec frontmatter fields; custom skills do not sync across surfaces; claude.ai upload requires code execution. Check current Anthropic documentation before relying on this.
