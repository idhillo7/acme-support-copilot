"""The conversation loop: draft or send a reply for an open support conversation.

Every customer conversation in the Acme support inbox passes through this
module in production. Conversation content is redacted, then sent to the
configured model provider; replies below the confidence floor are queued for
a human support lead instead of being sent.
"""

import logging
import time

from anthropic import Anthropic, APIStatusError

from app.copilot.handoff import queue_for_human
from app.copilot.redaction import redact_payment_shapes
from app.ops.telemetry import emit_counter
from config.model_gateway import (
    FALLBACK_PROVIDER,
    MAX_OUTPUT_TOKENS,
    PRIMARY_MODEL,
    REQUEST_TIMEOUT_SECONDS,
    RETRY_BEFORE_FALLBACK,
)

log = logging.getLogger("copilot.assistant")

CONFIDENCE_FLOOR = 0.72

SYSTEM_PROMPT = (
    "You are Acme's support copilot. Answer strictly from the conversation "
    "and the account facts given. If you are not sure, say you will check "
    "with a person. Never invent order numbers, refunds, or policy."
)

_client = Anthropic(timeout=REQUEST_TIMEOUT_SECONDS)


def draft_reply(conversation: list[dict], customer_tier: str) -> dict:
    """Draft a reply with the primary provider.

    There is deliberately no second provider here: FALLBACK_PROVIDER is None
    in production config, so a primary outage queues the conversation for a
    person rather than routing content to another vendor.
    """
    safe_turns = [
        {"role": t["role"], "content": redact_payment_shapes(t["content"])}
        for t in conversation
    ]
    response = None
    for attempt in range(1 + RETRY_BEFORE_FALLBACK):
        try:
            response = _client.messages.create(
                model=PRIMARY_MODEL,
                max_tokens=MAX_OUTPUT_TOKENS,
                system=f"{SYSTEM_PROMPT} Customer tier: {customer_tier}.",
                messages=safe_turns,
            )
            break
        except APIStatusError as exc:
            log.warning("provider attempt %d failed: %s", attempt + 1, exc.status_code)
            time.sleep(0.5 * (attempt + 1))
    if response is None:
        if FALLBACK_PROVIDER is None:
            emit_counter("copilot.provider_outage_to_human")
            return queue_for_human(conversation, draft=None, confidence=0.0)
        raise RuntimeError("fallback configured but not implemented")
    draft = response.content[0].text
    confidence = _score_confidence(response, safe_turns)
    emit_counter("copilot.replies_drafted", model=PRIMARY_MODEL)
    if confidence < CONFIDENCE_FLOOR:
        return queue_for_human(conversation, draft, confidence)
    return {"reply": draft, "sent_by": "copilot", "confidence": confidence}


def _score_confidence(response, turns: list[dict]) -> float:
    """Deterministic confidence heuristic; never model-reported."""
    if getattr(response, "stop_reason", "end_turn") != "end_turn":
        return 0.5
    text = response.content[0].text
    if len(text) < 20 or len(turns) > 24:
        return 0.6
    return 0.9
