from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL, VALID_TIERS

_client = Groq(api_key=GROQ_API_KEY)


def classify_safety_tier(question: str) -> dict:
    """
    Classify a client question into one of three safety tiers.

    TODO — Milestone 1:

    Before writing code, complete specs/classifier-spec.md. The blank fields there
    are the decisions that drive this function.

    Your implementation should:
      1. Build a prompt with your tier definitions that asks the LLM to classify the
         question and explain its reasoning
      2. Send a single chat completion request (no tools, no history)
      3. Parse the tier and reason out of the reply
      4. Validate the tier against VALID_TIERS; fall back to "caution" if the reply
         can't be parsed or the tier isn't recognized
      5. Return {"tier": ..., "reason": ...}

    Model note: LLM_MODEL is openai/gpt-oss-120b, which thinks before it answers.
    Pass max_tokens=1000 (not less) and reasoning_effort="low" to chat.completions.create,
    or the reply can come back empty.

    The three tiers:
      - "safe"    : general, public information about legal processes
      - "caution" : touches a person's specific legal situation
      - "refuse"  : privileged, confidential or unethical requests
    """
    return {
        "tier": "unknown",
        "reason": "Classification not yet implemented. Complete Milestone 1.",
    }
