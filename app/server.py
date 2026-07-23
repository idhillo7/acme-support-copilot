"""HTTP surface: the support product calls this to draft replies."""

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
    return draft_reply(body.conversation, body.customer_tier)


@app.post("/v1/conversations/enqueue")
def enqueue_conversation(body: DraftRequest) -> dict:
    with connection() as conn:
        row = conn.execute(
            "insert into conversation_queue (turns, customer_tier) values (%s, %s) returning id",
            (body.conversation, body.customer_tier),
        ).fetchone()
    return {"queued": str(row[0])}
