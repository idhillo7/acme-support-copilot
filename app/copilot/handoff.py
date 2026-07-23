# Copyright 2026 Acme Inc. Licensed under Apache-2.0.
"""Human handoff: a person can be requested at any point in a conversation.

Low-confidence drafts and provider outages land here too — the copilot never
sends a reply it is not confident in, and never routes content to a second
vendor just to avoid queueing for a person.
"""


def queue_for_human(conversation, draft, confidence) -> dict:
    return {
        "reply": None,
        "sent_by": "queued_for_human",
        "draft_for_review": draft,
        "confidence": confidence,
    }
