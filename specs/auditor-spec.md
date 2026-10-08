# Auditor Spec (Milestone 3)

Fill in every blank before writing `auditor.py`.

**1. Fields.** Which fields go in each record and why?

_Answer:_ `timestamp` (UTC ISO 8601, to know when it happened and order events), `tier`
(the safety decision, the main thing we audit), `question` (what triggered that
decision) and `response_preview` (enough of the reply to check it matched the tier).

**2. Truncation.** How many characters of the question and response do you keep, and why not
store everything?

_Answer:_ Question: 300 characters. Response: first 200 characters. That's enough to
review the decision, while keeping the log small and limiting how much potentially
sensitive client text sits on disk.

**3. File format.** Why one JSON object per line instead of one big JSON array?

_Answer:_ JSON Lines is append-only: each interaction is one `write` with no need to read
and rewrite the whole file. A crash mid-write damages at most one line, and tools like
`cat`, `tail`, `grep` and `jq` work on it line by line.

**4. Missing folder.** What happens if `logs/` doesn't exist?

_Answer:_ `os.makedirs(..., exist_ok=True)` creates it before writing. Logging errors are
caught and printed so a logging failure never breaks the user's answer.

**5. Privacy.** The log holds what users typed. What keeps it out of GitHub?

_Answer:_ `.gitignore` contains `logs/*.jsonl` (and `.env`), so the log is never staged.
Only `logs/.gitkeep` is tracked so the folder exists in the repo.
