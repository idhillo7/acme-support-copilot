"""Background worker: drafts replies for queued support conversations."""

import logging
import time

from app.copilot.assistant import draft_reply
from app.copilot.store import connection, record_draft
from app.ops.telemetry import emit_counter

log = logging.getLogger("copilot.worker")


def poll_once() -> int:
    with connection() as conn:
        rows = conn.execute(
            """
            select id, turns, customer_tier from conversation_queue
            where drafted_at is null
            order by enqueued_at
            limit 10
            for update skip locked
            """
        ).fetchall()
        for row in rows:
            draft = draft_reply(row[1], row[2])
            record_draft(str(row[0]), draft)
            conn.execute(
                "update conversation_queue set drafted_at = now() where id = %s",
                (row[0],),
            )
            emit_counter("copilot.drafts", sent_by=draft["sent_by"])
    return len(rows)


def main() -> None:
    logging.basicConfig(level="INFO")
    log.info("draft worker up")
    while True:
        handled = poll_once()
        if handled == 0:
            time.sleep(2.0)


if __name__ == "__main__":
    main()
