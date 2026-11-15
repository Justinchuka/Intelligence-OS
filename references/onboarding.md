# Onboarding

Read this before first-run, renaming, or changing owner context.

## 1. Owner contexts

| Context | Profile fields to collect (only what is needed) | Typical intelligence needs |
|---|---|---|
| individual | preferred name, background, skills, interests, location preferences, objectives, constraints | career, learning, finances, productivity, activity tracking, research, opportunities |
| business_brand | brand name, industry, products/services, markets, customers, competitors, objectives, operating context | market, customer, competitor, revenue, operations, product, funding, regulation |
| team_org | organisation profile, roles, shared objectives, departments, access boundaries, reporting needs | shared research, workflows, project tracking, team performance, governance |
| project_research | project name, subject, scope, stakeholders, research questions, milestones, evidence requirements | literature, progress tracking, analysis, reporting |

The context changes: questions asked, suggested modules and default dashboard content. Never assume a human personal profile. Profile fields are optional and each is permission-controlled (see `security-governance.md`).

## 2. Naming

1. Ask: "What would you like to call your Intelligence OS? You can skip this."
2. Custom name given: use it.
3. Skipped and a reliable preferred name or brand name is already known from the user's own words in this chat: generate 3-5 brandable ideas, choose one as default, and say it is an *automatically suggested name* that can be renamed.
4. Skipped and nothing reliable is known: use the neutral temporary name `My Intelligence OS` or ask one concise question. Never invent a person's name.
5. Renaming later is always allowed (`ios.py rename`). Optional identity: monogram/logo text, brand colours, short description, tagline.
6. OS identity is separate from owner identity. Client-facing exports must not include the creator's personal identity (`export --public` strips owner profile fields).

## 3. Initial template choice (only these three)

| Template id | Name | Language |
|---|---|---|
| essential-minimal | Essential — Minimal | light, spacious, typography-led |
| intelligence-operations | Intelligence — Operations | dark, dense, operational grid |
| atmosphere-glass | Atmosphere — Glass | layered glass surfaces, floating modules |

The other seven are revealed only after setup, in Administration > Appearance & Templates.

## 4. Natural questions (guided route)

Ask a short opening set; do not ask all of them. Choose by context. Avoid asking only "what are your goals?"

- What are you currently trying to make progress on?
- What would you like to get better at?
- What opportunities would you like to discover?
- What would you like to keep an eye on?
- What would you like to organise better?
- Business: who are your customers, and who do you compete with? Team: who needs to see what? Project: what questions must this answer?

Ask follow-ups only where an answer would change the configuration. If the user cannot articulate goals, offer 3-4 plain-language examples to react to.

## 5. Inference step

From answers produce, labelled **Proposed**:

| Item | Rule |
|---|---|
| Objectives | one sentence each, in the user's words where possible |
| Desired outcome | measurable target ONLY if the user stated one or agrees; otherwise `target: null` |
| Possible measures / milestones | suggested, not imposed; never invent numeric targets |
| Modules | from `catalogue/INDEX.md`, each with a one-line *why relevant*, its type(s), and whether it needs web access |
| Dashboard sections | from the 10 universal groupings (Latest Developments, Opportunities, Resources, Trends & Emerging Signals, Events & Activities, Organisations & Ecosystem, Research & Knowledge, Funding & Support, People & Networks, Changes & Alerts) |

## 6. Review and approval screen

Present one table: item | proposal | why | accept / edit / reject / defer. Nothing is activated before the owner responds. Deferred items are saved with status `proposed`.

## 7. Create

After approval run `ios.py init`, then `ios.py module add` per approved module and `ios.py goal add` per approved objective. Report the config version created. Deliver the state pack.

## 8. Catalogue route

Display the 10 categories from `catalogue/INDEX.md` with their 10 items each. The user picks across categories. **Maximum 15 custom features active** (default rule; visible in settings as `limits.max_custom_features`). Show only the selected items for confirmation, then implement. If more than 15 are selected, say so and ask which to defer. Changing the cap needs an explicit owner decision recorded in the decision log. After install, the cap applies to active custom features: replacing one frees a slot.
