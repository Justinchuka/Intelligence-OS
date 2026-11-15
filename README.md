# Intelligence OS (Claude-native Skill)

A modular **Intelligence Operating System** that runs inside Claude. Describe what you want to improve, discover, monitor or organise; it proposes goals, modules and a dashboard for your approval; then runs discovery agents, tracking modules and analytical agents, keeps evidence and history, turns findings into approved actions, and exports portable data.

It is an instruction package plus a small deterministic script. It is **not** a hosted app, a database, or a scheduler (see Limits).

## Who it is for
Individuals, businesses/brands, teams/organisations and research projects. Onboarding adapts to the context you choose.

## Requirements
| Need | For |
|---|---|
| Claude plan that supports Skills, with code execution / file creation enabled | installing the Skill and using `scripts/ios.py` (state pack, exports, dashboard) |
| Web search / fetch enabled in your chat | Discovery agents only. Without it, tracking, analysis, goals, actions and exports still work |
| Python 3 (provided in Claude's code environment); `openpyxl` optional | Excel export (CSV works without it) |
No Anthropic API key and no separate API billing are needed. Usage counts against your own Claude plan; deep investigations use more.

## Install
Package conventions change; check Anthropic's current Skills documentation if a step fails. At build time these were the conventions found in third-party and community documentation (not verified against Anthropic's own pages by the author):

**claude.ai / Claude Desktop**
1. Download `intelligence-os.zip` (the ZIP contains one folder, `intelligence-os/`).
2. Open Settings, then Capabilities (or Features), then Skills; upload the ZIP; switch the skill on.
3. Start a chat and say: **"Set up an Intelligence OS"**.

**Claude Code**: copy the `intelligence-os/` folder to `~/.claude/skills/` (user) or `.claude/skills/` (project).

**GitHub**: put the `intelligence-os/` folder in your repository (for example under `skills/`). For claude.ai, zip that folder (the folder, not its contents) and upload. Custom skills do not sync between claude.ai, the API and Claude Code; install on each surface you use.

## Activate and use
Say things like: "Set up an Intelligence OS for my bakery", "Add a Job Finder", "I spent N8,500 on transport today", "Analyse my spending for the last 30 days", "Show my dashboard", "Switch appearance to Mosaic — Bento".

## Persistence: the state pack
Claude chats do not guarantee storage. Your OS lives in a portable `os-state/` folder that the skill creates and gives you as a download. **Upload it at the start of the next session** to continue. Keep your copy safe; if you lose it, the data is gone. See `references/library-exports-portability.md`.

## What is included
- 4 owner contexts; 10 categories x 10 modules (100 catalogue modules) plus custom modules; 15-active-custom-feature limit.
- Evidence, confidence labels and source-health records; honest run counts.
- Quick Capture, trackers, Analysis Centre, Goals, Action Centre, Decision Log, alerts (evaluated in-session).
- Configuration versions with rollback; archive/restore; permission grants.
- Exports: CSV, Excel (with openpyxl), configuration package, static HTML dashboard in 10 layout systems.

## Limits (read this)
No background or scheduled runs, no email/notifications, no voice, no private cloud drive, no live drag-and-drop dashboard, no multi-user access control. Discovery quality depends on the web tools in your environment. The dashboard is a generated snapshot. Full list: `docs/KNOWN-LIMITATIONS.md`.

## Configuration
`config.json` in the state pack holds the owner profile, modules, permissions, limits, appearance and sources. Change it through the assistant (or `scripts/ios.py`), never by hand-editing, so versions and history stay consistent.

## Troubleshooting
| Problem | Fix |
|---|---|
| Upload rejected | Description over 200 characters, wrong folder name, or loose files at ZIP root. Re-zip the `intelligence-os/` folder |
| "Skill not triggering" | Say "Intelligence OS" explicitly, check the skill is toggled on |
| "No web tools" | Enable web search for the chat; discovery cannot run without it |
| `validate` reports "modified since manifest" | Files changed outside the tool; run `manifest` if intended, else restore your backup |
| Excel export fails | `openpyxl` missing; use CSV |
| Lost state | Upload your latest `os-state.zip`; versions in `versions/` can restore configuration (not records) |

## Repository layout
See `docs/user-guide.md` and `references/`. Tests: `python evals/test_ios.py`. Package check: `python evals/check_package.py .`

## Licence
MIT.
