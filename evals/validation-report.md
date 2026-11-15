# Validation report (build 1.0.0)

## Results actually obtained
| Check | Method | Result |
|---|---|---|
| Tooling tests | `python evals/test_ios.py` | 20 tests, all passed (re-run at the end of the build) |
| Package checks | `python evals/check_package.py . --zip ...` | all passed (frontmatter keys, name = folder, description <= 200 chars, SKILL.md < 500 lines, paths exist, no empty files/folders, no secret patterns, ZIP has one top-level folder) |
| Catalogue vs spec | script comparison of category and module names with spec section 8 | 10 categories x 10 modules, names identical, 100 unique ids |
| Template structure | test: 10 renders differ after removing CSS; HTML-escaping of hostile titles; no external script hosts | passed |
| Layout overflow | headless Chromium, all 10 templates at 1200px and 375px | no horizontal overflow after fixes (first pass found 5 failing layouts, fixed) |
| Visual inspection | screenshots of Operations, Bento, Glass | layouts clearly distinct; Operations and Bento had a chart-scaling and word-wrapping defect, fixed |
| State pack round trip | zip, unzip, validate | passed (found and fixed a bug: empty folders were lost in ZIP and broke validation) |

## NOT done
| Item | Why |
|---|---|
| Behavioural tests B01-B30 | Need a fresh Claude session with the skill installed; cannot be driven from here. Cases are written in `test-cases.md` |
| Install in claude.ai / Claude Code | Not performed |
| Verification of packaging rules against Anthropic's own documentation | Rules came from third-party and community pages found by search; recheck before publishing |
| Safari, Firefox, real mobile devices | Not tested |
| GitHub publication | Not performed; a ZIP and folder are delivered |
| xlsx re-import | Not implemented by design |

## Requirement status
See `docs/REQUIREMENTS-TRACEABILITY.md`. Unsupported capabilities are disclosed in `README.md` and `docs/KNOWN-LIMITATIONS.md`.

## Defects found during build (fixed)
1. Shell brace expansion produced wrong folders (build-environment only).
2. Description exceeded 200 characters (211, now 197).
3. Empty state folders would not survive zipping and broke `validate`.
4. Five dashboard layouts overflowed horizontally; chart text over-scaled; table words broke mid-word.
