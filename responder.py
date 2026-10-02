from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)


def generate_safe_response(question: str, tier: str) -> str:
    """
    Generate a reply to the question, calibrated to its safety tier.

    TODO — Milestone 2:

    Before writing code, complete specs/responder-spec.md. The most important fields
    are the three system prompts, one per tier. Write them out in full first.

    Use a different system prompt for each tier:
      - "safe"    : answer helpfully and directly
      - "caution" : general information only, no legal advice, recommend an attorney
      - "refuse"  : do NOT help. Explain briefly and point to the attorney

    The refuse case is the hardest. A reply like "I can't help, but here is how you
    would do it..." defeats the safety layer. Your prompt must rule that out.

    If tier is unrecognized (e.g. "unknown"), treat it as "caution".

    Model note: pass max_tokens=1500 and reasoning_effort="low" to chat.completions.create
    (gpt-oss thinks before it answers, so small limits can give empty replies).

    Return the reply as a plain string.
    """
    return "⚙️ Response generation not yet implemented. Complete Milestone 2."
