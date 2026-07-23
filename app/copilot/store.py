# Copyright 2026 Acme Inc. Licensed under Apache-2.0.
"""Conversation store: durable record of conversations and drafted replies.

Backs both the HTTP surface and the draft worker. Message bodies live only
here, under the 30-day retention rule in app.copilot.retention.
"""

import os
from contextlib import contextmanager

import psycopg


def _dsn() -> str:
    return os.environ["COPILOT_DB_URL"]


@contextmanager
def connection():
    with psycopg.connect(_dsn()) as conn:
        yield conn


def record_draft(conversation_id: str, draft: dict) -> None:
    with connection() as conn:
        conn.execute(
            """
            insert into reply_drafts (conversation_id, body, sent_by, confidence)
            values (%s, %s, %s, %s)
            """,
            (
                conversation_id,
                draft.get("reply") or draft.get("draft_for_review"),
                draft["sent_by"],
                draft["confidence"],
            ),
        )
