"""The conversation loop: draft a reply for an open support conversation."""

from anthropic import Anthropic

from app.copilot.redaction import redact_payment_shapes
from app.copilot.handoff import queue_for_human
from config.model_gateway import (
    MAX_OUTPUT_TOKENS,
    PRIMARY_MODEL,
    REQUEST_TIMEOUT_SECONDS,
)

CONFIDENCE_FLOOR = 0.72

_client = Anthropic(timeout=REQUEST_TIMEOUT_SECONDS)


def draft_reply(conversation: list[dict], customer_tier: str) -> dict:
    """Draft a reply with the configured provider; low confidence goes human."""
    safe_turns = [
        {"role": t["role"], "content": redact_payment_shapes(t["content"])}
        for t in conversation
    ]
    response = _client.messages.create(
        model=PRIMARY_MODEL,
        max_tokens=MAX_OUTPUT_TOKENS,
        system=(
            "You are Acme's support copilot. Answer from the conversation "
            f"only. Customer tier: {customer_tier}."
        ),
        messages=safe_turns,
    )
    draft = response.content[0].text
    confidence = _score_confidence(response)
    if confidence < CONFIDENCE_FLOOR:
        return queue_for_human(conversation, draft, confidence)
    return {"reply": draft, "sent_by": "copilot", "confidence": confidence}


def _score_confidence(response) -> float:
    stop = getattr(response, "stop_reason", "end_turn")
    return 0.9 if stop == "end_turn" else 0.5
