# Cross-module collaboration and Workflow Builder

## 1. Permission model
`config.json > permissions`:
- `profile_access`: `{module_id: [profile_field,...]}` default empty.
- `module_access`: `{reader_module_id: {from: [module_id], fields: [field,...], purpose: "..."}}` default empty.
- `sensitive_sharing`: list of field classes that always need per-use approval (health, finance, contact details).
Least privilege: pass only the fields a collaboration needs, preserving `source_url`, `confidence`, `record_id` of the original.

## 2. Collaboration procedure
1. Identify the chain (e.g. Job Finder → Skill Gap Analyst → Learning Path Builder → Action Centre).
2. Check each hop against `module_access`. Missing grant: ask the owner to approve (scope, fields, purpose, duration: this run or persistent). Record the decision.
3. Execute hops, carrying provenance.
4. Output a **Trace**: modules used, record IDs consumed, fields passed, who approved, and which outputs are observations vs interpretations vs recommendations.
5. Any consequential action at the end (action creation, external step) needs approval.

## 3. User-initiated cross-module analysis
Allowed only across modules the owner selects and the permissions allow. State what was combined.

## 4. Workflow Builder (specification, not unattended automation)
A workflow is a stored definition: `workflow_id, name, trigger, conditions[], steps[{module_id, op, inputs}], approvals[], outputs`.
| Trigger | Supported in Claude-native? |
|---|---|
| manual ("run workflow X") | yes |
| user message pattern | yes, while a chat is active |
| time schedule, new data, webhook | **only if a real scheduler/connector exists**; otherwise stored as definition for future standalone use |
Never imply a workflow runs unattended. Running one is a series of approved steps in the current chat, logged in execution history. Changes to workflows need approval and create a config version.
