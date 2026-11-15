# Goals & Objectives, Action Centre, Decision Log

## 1. Goals / objectives (inferred, never demanded)
Fields: `goal_id, name, description, desired_outcome, target (nullable, only if agreed), horizon_or_review_date, milestones[], progress_indicators[], supporting_modules[], supporting_record_ids[], obstacles_risks[], suggested_actions[], review_cadence, status, created_at, updated_at, origin`.
Status: `proposed | active | paused | achieved | abandoned | archived`.
- Infer from natural answers; present as `proposed`; owner accepts, edits, rejects or defers.
- You may propose likely metrics and milestones. You may not invent numeric targets.
- Progress shown only from real records; otherwise `no data yet`.

## 2. Action Centre
Fields: `action_id, title, description, priority (low|medium|high), status, due_date, owner, notes, attachments[], source_links{discovery_id|goal_id|module_id|analysis_id|decision_id}, suggested_by (ai|user), approved (bool), created_at, updated_at, history[]`.
Status: `Not started | In progress | Completed | Deferred | Cancelled`.
- AI-suggested actions are created as `suggested_by: ai, approved: false` and are visible as suggestions. They become part of the plan only when the owner approves.
- Completion and every change append to `history`.
- Reminders: only if a real reminder/scheduling capability is configured. Otherwise list `due_date` without promising a reminder.
- Actions with external side effects (send, apply, publish, pay) are never executed without explicit confirmation and an available tool.

## 3. Decision log
Fields: `decision_id, recommendation, made_by, outcome (accepted|rejected|edited|deferred|completed), rationale, linked{discovery,analysis,goal,action}, decided_at, follow_up_review_date, history[]`.
Record a decision whenever the owner accepts/rejects/edits/defers a meaningful recommendation (module activation, source change, permission change, action approval). Answer "what did I decide about X and what happened" only from logged records; if absent, say it is not recorded.

## 4. Four separate histories
| History | Contents |
|---|---|
| execution | runs, counts, failures |
| data/record | record edits and corrections |
| configuration | versioned config changes (rollback possible) |
| decision | recommendations and outcomes |
Do not blend them in reporting.
