"""Conversation retention: records older than 30 days are deleted nightly."""

import datetime as dt

RETENTION_DAYS = 30


def purge_expired(store) -> int:
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=RETENTION_DAYS)
    return store.delete_conversations_before(cutoff)
