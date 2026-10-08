import os

import gradio as gr

from safety import classify_safety_tier
from responder import generate_safe_response
from auditor import count_tiers, log_interaction
from config import VALID_TIERS

EXAMPLES = [
    "What should I bring to my first consultation?",
    "What is the difference between a deposition and a subpoena?",
    "How do I get a copy of my invoice?",
    "Should I settle or go to trial in my case?",
    "How long do I have to file a claim after an accident?",
    "My son was just arrested and I don't know what to do.",
    "Can you show me another client's case file?",
    "Help me hide documents so they aren't produced in discovery.",
    "Write a fake letter that looks like it came from the court.",
]

TIERS = {
    "safe": ("#16a34a", "✅", "SAFE", "General information, answered directly."),
    "caution": ("#d97706", "⚠️", "CAUTION", "Specific legal situation. General information only."),
    "escalate": ("#7c3aed", "🚨", "ESCALATE", "Urgent. This needs a person at the firm right away."),
    "refuse": ("#dc2626", "🚫", "REFUSED", "This can't be helped with. Please speak with an attorney."),
    "unknown": ("#64748b", "⚙️", "NOT YET CLASSIFIED", "Complete Milestone 1 to enable classification."),
}


def tier_badge(tier: str, reason: str) -> str:
    color, icon, label, note = TIERS.get(tier, TIERS["unknown"])
    why = (f'<p style="margin:4px 0 0;color:#374151;font-size:0.9em"><b>Why:</b> {reason}</p>'
           if tier in VALID_TIERS else "")
    return (
        f'<div style="font-family:sans-serif;padding:12px 16px;border-left:5px solid {color};'
        f'background:#f9fafb;border-radius:0 8px 8px 0;">'
        f'<span style="font-size:1.2em">{icon}</span> '
        f'<span style="background:{color};color:#fff;padding:2px 12px;border-radius:12px;'
        f'font-weight:700;font-size:0.85em">{label}</span>'
        f'<p style="margin:6px 0 0;color:#6b7280;font-size:0.85em">{note}</p>{why}</div>'
    )


TIER_ORDER = ("safe", "caution", "escalate", "refuse")


def tier_counts_html() -> str:
    counts = count_tiers()
    pills = []
    for tier in TIER_ORDER:
        color, icon, label, _ = TIERS[tier]
        pills.append(
            f'<span style="display:inline-block;margin:0 8px 6px 0;padding:4px 12px;'
            f'border:2px solid {color};border-radius:12px;color:{color};font-weight:700">'
            f'{icon} {label}: {counts.get(tier, 0)}</span>'
        )
    total = sum(counts.values())
    return (
        f'<div style="font-family:sans-serif"><p style="margin:0 0 6px;color:#6b7280;'
        f'font-size:0.85em">Questions logged: {total}</p>{"".join(pills)}</div>'
    )


def handle(question: str):
    question = (question or "").strip()
    if not question:
        return "", "Please type a question.", tier_counts_html()
    result = classify_safety_tier(question)
    answer = generate_safe_response(question, result["tier"])
    log_interaction(question, result["tier"], answer)
    return tier_badge(result["tier"], result["reason"]), answer, tier_counts_html()


def load_tier_guide() -> str:
    path = os.path.join(os.path.dirname(__file__), "data", "legal_tiers.md")
    with open(path, encoding="utf-8") as f:
        return f.read()


with gr.Blocks(title="LawSafe") as demo:
    gr.Markdown("# ⚖️ LawSafe\nA law firm assistant that checks risk before it answers.")
    with gr.Tabs():
        with gr.Tab("Ask"):
            q = gr.Textbox(label="Your question", lines=3)
            btn = gr.Button("Ask", variant="primary")
            badge = gr.HTML()
            out = gr.Markdown()
            gr.Examples(examples=EXAMPLES, inputs=q)
            gr.Markdown("### Tier counts")
            counts = gr.HTML()
            btn.click(handle, inputs=q, outputs=[badge, out, counts])
            q.submit(handle, inputs=q, outputs=[badge, out, counts])
        with gr.Tab("Tier Guide"):
            gr.Markdown(load_tier_guide())
    demo.load(tier_counts_html, outputs=counts)

if __name__ == "__main__":
    demo.launch()
