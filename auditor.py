import json
import os
from datetime import datetime, timezone
from config import LOG_FILE


def log_interaction(question: str, tier: str, response: str) -> None:
    """
    Append a record of this interaction to the audit log.

    TODO — Milestone 3:

    Before writing code, complete specs/auditor-spec.md. Decide which fields to log,
    how much text to keep, and what to do if logs/ doesn't exist.

    Write one JSON object per line to LOG_FILE ("logs/audit.jsonl").

    Required fields:
      - "timestamp"        : ISO 8601 string
      - "tier"             : the tier assigned to the question
      - "question"         : truncate to 300 chars
      - "response_preview" : first 200 characters of the response

    Create logs/ if it doesn't exist. Also print a one-line summary, for example:
      [LOGGED] tier=caution | "Should I settle or go to trial..." -> 212 chars
    """
    pass
