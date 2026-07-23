"""A person can be requested at any point; low confidence lands here too."""


def queue_for_human(conversation, draft, confidence) -> dict:
    return {
        "reply": None,
        "sent_by": "queued_for_human",
        "draft_for_review": draft,
        "confidence": confidence,
    }
