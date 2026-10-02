# System Design (read this first)

LawSafe checks how risky a question is before answering it.

## Pipeline
1. `classify_safety_tier(question)` returns `{"tier", "reason"}`
2. `generate_safe_response(question, tier)` returns a reply shaped by the tier
3. `log_interaction(question, tier, response)` adds one line to `logs/audit.jsonl`

`app.py` runs these in order.

## Tiers
| Tier | Meaning | Behaviour |
|------|---------|-----------|
| safe | General information | Answer directly |
| caution | Specific legal situation | General info only, no advice, recommend an attorney |
| refuse | Privileged or unethical | Decline, explain, point to the attorney |

If anything goes wrong, fall back to `caution`, never `safe`.

## Answer before you start
1. Why classify first instead of one prompt that "answers safely"?
2. Why does an unknown tier become `caution` and not `safe`?
3. What is the worst thing an unguarded legal assistant could do?
