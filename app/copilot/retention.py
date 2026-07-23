"""Conversation retention: records older than 30 days are deleted nightly."""

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
