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
| escalate | Urgent or high-stakes (arrest, deadline today, safety, complaint) | Don't answer; tell them to contact a person at the firm now (911 if in danger) |
| refuse | Privileged or unethical | Decline, explain, point to the attorney |

If anything goes wrong, fall back to `caution`, never `safe`.

## Answer before you start
1. Why classify first instead of one prompt that "answers safely"?

   _Answer:_ A separate classification step makes the risk decision explicit, testable and
   loggable. A single "answer safely" prompt mixes judging and answering, so the model can
   talk itself into helping (especially when a user pushes it), and we'd have no record of
   what it decided. Splitting them lets the responder use a strict, tier-specific prompt
   and gives us a tier to show in the UI and write to the audit log.

2. Why does an unknown tier become `caution` and not `safe`?

   _Answer:_ Failing safe. If the classifier errors or returns garbage we don't know how
   risky the question is. `caution` still gives general information but never legal
   advice, so a misfire costs a little helpfulness instead of risking unauthorized advice
   or a leak. Defaulting to `safe` would let any failure (or a prompt injection that
   breaks the parser) bypass the safety layer.

3. What is the worst thing an unguarded legal assistant could do?

   _Answer:_ Disclose another client's privileged or confidential information, or help
   someone commit fraud or obstruction (hiding evidence, forging court documents). Close
   behind: giving confident, specific legal advice that a person relies on and loses
   their case or misses a deadline because of it.
