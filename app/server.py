"""HTTP surface: the support product calls this to draft replies."""

from fastapi import FastAPI
from pydantic import BaseModel

from app.copilot.assistant import draft_reply

app = FastAPI(title="acme-support-copilot")


class DraftRequest(BaseModel):
    conversation: list[dict]
    customer_tier: str = "standard"


@app.post("/v1/draft-reply")
def post_draft_reply(body: DraftRequest) -> dict:
    return draft_reply(body.conversation, body.customer_tier)
