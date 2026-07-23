# Copyright 2026 Acme Inc. Licensed under Apache-2.0.
"""HTTP surface: the support product calls this to draft replies.

Deployed as the `copilot` service in docker-compose.yml; the platform load
balancer fronts it in production. Every draft request flows through
app.copilot.assistant, which owns redaction and the human-handoff floor.
"""

from fastapi import FastAPI
from pydantic import BaseModel

from app.copilot.assistant import draft_reply
from app.copilot.store import connection

app = FastAPI(title="acme-support-copilot")


class DraftRequest(BaseModel):
    conversation: list[dict]
    customer_tier: str = "standard"


@app.get("/healthz")
def healthz() -> dict:
    return {"ok": True}


@app.post("/v1/draft-reply")
def post_draft_reply(body: DraftRequest) -> dict:
    """Synchronous draft for the agent-assist pane in the support inbox."""
    return draft_reply(body.conversation, body.customer_tier)


@app.post("/v1/conversations/enqueue")
def enqueue_conversation(body: DraftRequest) -> dict:
    """Queue a conversation for the background draft worker."""
    with connection() as conn:
        row = conn.execute(
            "insert into conversation_queue (turns, customer_tier) values (%s, %s) returning id",
            (body.conversation, body.customer_tier),
        ).fetchone()
    return {"queued": str(row[0])}
