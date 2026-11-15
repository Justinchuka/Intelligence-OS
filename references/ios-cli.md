# ios.py command reference

Run from the skill folder: `python scripts/ios.py <command> --dir os-state ...`. Pure Python (stdlib; `openpyxl` optional for xlsx). No network, no AI, no scheduling. **Meaningful changes print a PLAN and exit with code 3 until `--confirm` is passed**; pass `--confirm` only after the owner approved. If code execution is unavailable, apply the same rules by hand and say state is not file-backed.

| Task | Command |
|---|---|
| Create OS | `init --name N --name-origin user\|auto_suggested\|temporary --context individual\|business_brand\|team_org\|project_research --template essential-minimal\|intelligence-operations\|atmosphere-glass [--profile k=v ...] --confirm` |
| Rename | `rename --name N --confirm` |
| Appearance (all 10 after setup) | `template --template <id> [--preset compact\|expanded\|research\|monitoring] --confirm` |
| List modules | `module list` |
| Add from catalogue / custom | `module add --catalogue <id> --confirm` · `module add --name N --modes tracking,analysis --fields "a;b;c" --confirm` |
| Lifecycle | `module enable\|disable\|hide\|show\|archive\|restore\|delete --id X --confirm` (`delete --permanent` erases) |
| Quick Capture entry | `record add --module M --value V --unit U --currency C --occurred-at ISO --category X --source quick_capture` (no --confirm needed) |
| Correct a record | `record edit --module M --id R --set value=9000 [--by user\|ai]` (history kept; AI cannot overwrite user edits) |
| Store discoveries | `discovery --module M --json findings.json` (rejects records missing evidence/confidence; dedupes) |
| Log a real run | `run --module M --depth standard --source-checks n --queries n --results n --unique n --new n --updated n --failures n` |
| Sources | `source add --name N --url U --module M --confirm` · `source health --id S --status reachable\|failed\|changed [--error E]` (only after a real check) · `source remove --id S --confirm` |
| Permissions | `permission profile --module M --fields f1 f2 --confirm` · `permission module --module READER --source-module SRC --fields f --purpose "..." --confirm` |
| Goals / actions / decisions | `goal\|action\|decision add --title T [--by ai]` · `update --id I --set k=v [--approve]` · `list` |
| Versions | `versions list` · `versions diff --a 2 --b 5` · `versions rollback --to 3 --confirm` |
| Analysis | `analyse --module M [M2] --period today\|yesterday\|7d\|30d\|3m\|6m\|1y\|all\|custom [--start D --end D]` |
| Exports | `export csv\|xlsx\|config --out exports [--public]` |
| Dashboard | `render [--template id] --out exports/dashboard.html` |
| Universal search | `search --q text [--module M ...]` |
| Profile | `profile show` · `profile set --set key=value --confirm` |
| Saved views / workspaces | `workspace add --name N --modules M1 M2 [--filter k=v] --confirm` · `workspace list` |
| Integrity | `validate` · `manifest` (after intentional manual edits) |

Exit codes: 0 ok · 1 validation problems · 2 error/refusal · 3 awaiting `--confirm`.
