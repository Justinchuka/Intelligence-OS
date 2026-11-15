# Test plan

Two layers, kept separate on purpose.

| Layer | What it proves | How | Status in this build |
|---|---|---|---|
| A. Tooling tests (automated) | `scripts/ios.py` and `render_dashboard.py` behave as specified: approval gate, lifecycle, cap, edit protection, evidence validation, honest counts, versioning, exports, rendering, integrity, round trip | `python evals/test_ios.py` | **RUN, passing** (see validation report) |
| B. Package checks (automated) | frontmatter, name, description length, referenced paths, no empty files/folders, no secret patterns, ZIP structure | `python evals/check_package.py . --zip ../intelligence-os.zip` | **RUN, passing** |
| C. Behavioural tests (manual) | Claude, with the skill installed, follows SKILL.md: onboarding, inference, approvals, honesty, refusal to fabricate | prompts in `test-cases.md`, run in a fresh chat with the skill uploaded | **NOT RUN** (cannot install and drive a fresh Claude session from here) |

Pass criteria for C: every "Expected" bullet holds and no "Must not" bullet occurs. Record results in a copy of `test-cases.md`.

Environment variants to repeat C in: (1) code execution + web search on; (2) code execution on, web search off; (3) code execution off.
