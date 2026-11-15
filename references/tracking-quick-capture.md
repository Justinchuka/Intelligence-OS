# Tracking modules and Quick Capture

## 1. Principles
Trackers store user-reported or integrated records and do not browse the internet unless the owner enables it. Manual and structured entry must not require AI: use `ios.py record add` (forms/flags) for deterministic entry. Use AI only to interpret free text.

## 2. Quick Capture procedure
Free text such as "I walked 6,200 steps today", "I spent N8,500 on transport today", "I completed a 3km run", "I studied AI for 2 hours".

1. Extract: `module (likely)`, `value`, `unit`, `occurred_at`, `currency`, `category`, `capture_source: quick_capture`.
2. Resolve relative dates ("today") using the current date and the owner's time zone if known; state the resolved date.
3. Destination or meaning ambiguous (e.g. "spent 8,500" with several finance trackers; "ran 3" with no unit)? Ask **one concise question**. Do not guess units or currency.
4. No tracker exists for it? Propose a tracker with fields and confirm before creating.
5. Show the parsed record in one line and write it with `ios.py record add`. Report the record_id.
6. Corrections: never overwrite; `ios.py record edit` appends to `edit_history` with prior value, new value, time, actor.

## 3. Voice
Do not advertise voice capture. Only offer it if a real speech-input capability is visible in the current environment, and state that it is environment-provided.

## 4. Record integrity
Stable `record_id`, `captured_at` (entry time) distinct from `occurred_at` (activity time), unit/currency kept as stated, `created_by`/`edited_by`, no silent normalisation. Currency conversion is never applied unless the user supplies a rate, and then the rate is stored.

## 5. Health-related trackers
Organise readings, show trends, give general educational context. Never diagnose, never advise medication changes, suggest a clinician for concerning values. Treat as sensitive data: excluded from exports unless the owner opts in.

## 6. Reminders
Offer reminders only if a real reminder/scheduling capability is present and configured. Otherwise say reminders are unavailable.
