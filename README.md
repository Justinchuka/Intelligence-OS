# Intelligence OS (AI-assisted modular system)

Intelligence-OS is a modular intelligence and personal-operations system designed to work with AI assistants and builder tools. It is not limited to Claude: AI tools such as OpenCode can use it when they can read the project instructions, work with files, and run the included Python script.

Configure an operating system for yourself, a business, a team, or a project, then use it to:

- Discover and track external information
- Capture expenses or other records
- Set goals and actions
- Analyze trends and activity
- Maintain decisions and evidence
- Create personalized dashboards based on your chosen context, needs, and preferences
- Generate static dashboards and CSV/Excel exports
- Save a portable state pack so configuration can continue in another chat or supported AI tool

Describe what you want to improve, discover, monitor or organise; the system proposes goals, modules and a dashboard for your approval; then it runs discovery agents, tracking modules and analytical agents, keeps evidence and history, turns findings into approved actions, and exports portable data.

It is an instruction package plus a small deterministic script. It is **not** a hosted app, a database, or a scheduler (see Limits).

## Who it is for
Individuals, businesses/brands, teams/organisations and research projects. Onboarding adapts to the context you choose.

## Requirements
| Need | For |
|---|---|
| An AI assistant or builder tool that can read the project instructions, create or edit files, and run Python | configuring and using the system, including state packs, exports and dashboards |
| Web search / fetch enabled in your AI tool | Discovery agents only. Without it, tracking, analysis, goals, actions and exports still work |
| Python 3; `openpyxl` optional | Excel export (CSV works without it) |

No Anthropic API key or separate API billing is needed to use the included scripts. Any AI-tool usage or billing is subject to that tool's own plan and policies.

## Install
The exact setup depends on your AI tool. Use its instructions or project-rules feature to provide the contents of this repository's `intelligence-os/` folder as context. For coding agents such as OpenCode or Claude Code, place the folder where the agent can read its instructions, or point the agent to it in your project configuration. For Claude.ai or Claude Desktop, package the folder as a Skill ZIP and install it through the Skills settings.

After setup, start a chat with a request such as: **"Set up an Intelligence OS"**.

## Activate and use
Say things like: "Set up an Intelligence OS for my bakery", "Add a Job Finder", "I spent N8,500 on transport today", "Analyse my spending for the last 30 days", "Create a dashboard for my team's project priorities", "Show my dashboard", or "Switch appearance to Mosaic — Bento".

## Persistence: the state pack
AI chats do not guarantee storage. Your OS lives in a portable `os-state/` folder that the system creates and gives you as a download. **Upload or provide it at the start of the next session** to continue. Keep your copy safe; if you lose it, the data is gone. See `references/library-exports-portability.md`.

## What is included
- 4 owner contexts; 10 categories x 10 modules (100 catalogue modules) plus custom modules; 15-active-custom-feature limit.
- Evidence, confidence labels and source-health records; honest run counts.
- Quick Capture, trackers, Analysis Centre, Goals, Action Centre, Decision Log, alerts (evaluated in-session).
- Configuration versions with rollback; archive/restore; permission grants.
- Exports: CSV, Excel (with openpyxl), configuration package, personalized static HTML dashboards in 10 layout systems.

## Limits (read this)
No background or scheduled runs, no email/notifications, no voice, no private cloud drive, no live drag-and-drop dashboard, no multi-user access control. Discovery quality depends on the web tools in your environment. The dashboard is a generated snapshot. Full list: `docs/KNOWN-LIMITATIONS.md`.

## Configuration
`config.json` in the state pack holds the owner profile, modules, permissions, limits, appearance and sources. Change it through the assistant (or `scripts/ios.py`), never by hand-editing, so versions and history stay consistent.

## Troubleshooting
| Problem | Fix |
|---|---|
| Upload rejected | Description over 200 characters, wrong folder name, or loose files at ZIP root. Re-zip the `intelligence-os/` folder |
| System not responding as expected | Point your AI tool to the `intelligence-os/` instructions and check that it can read the files and run Python |
| No web tools | Enable web search for the chat; discovery cannot run without it |
| `validate` reports "modified since manifest" | Files changed outside the tool; run `manifest` if intended, else restore your backup |
| Excel export fails | `openpyxl` missing; use CSV |
| Lost state | Provide your latest `os-state.zip`; versions in `versions/` can restore configuration (not records) |

## Repository layout
See `docs/user-guide.md` and `references/`. Tests: `python evals/test_ios.py`. Package check: `python evals/check_package.py .`

## Licence
MIT.
