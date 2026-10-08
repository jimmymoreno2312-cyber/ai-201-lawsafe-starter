import json
import os
from datetime import datetime, timezone
from config import LOG_FILE

MAX_QUESTION_CHARS = 300
MAX_PREVIEW_CHARS = 200


def log_interaction(question: str, tier: str, response: str) -> None:
    """Append one JSON line describing this interaction to LOG_FILE."""
    question = question or ""
    response = response or ""
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tier": tier,
        "question": question[:MAX_QUESTION_CHARS],
        "response_preview": response[:MAX_PREVIEW_CHARS],
    }
    try:
        os.makedirs(os.path.dirname(LOG_FILE) or ".", exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError as e:
        print(f"[LOG ERROR] could not write {LOG_FILE}: {e}")
        return

    short_q = question if len(question) <= 40 else question[:40] + "..."
    print(f'[LOGGED] tier={tier} | "{short_q}" -> {len(response)} chars')


def count_tiers() -> dict:
    """Count logged interactions per tier. Returns {} if there is no log yet."""
    counts = {}
    try:
        with open(LOG_FILE, encoding="utf-8") as f:
            for line in f:
                try:
                    tier = json.loads(line).get("tier", "unknown")
                except json.JSONDecodeError:
                    continue
                counts[tier] = counts.get(tier, 0) + 1
    except FileNotFoundError:
        pass
    return counts
