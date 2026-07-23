# Copyright 2026 Acme Inc. Licensed under Apache-2.0.
"""Conversation retention: records older than 30 days are deleted nightly.

Scheduled by the platform cron against the worker container. The 30-day
window is an operating fact recipients of Acme's security answers rely on.
"""

import datetime as dt

from app.copilot.store import connection

RETENTION_DAYS = 30


def purge_expired() -> int:
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=RETENTION_DAYS)
    with connection() as conn:
        result = conn.execute(
            "delete from conversations where started_at < %s", (cutoff,)
        )
        return result.rowcount
