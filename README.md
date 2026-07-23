# Acme Support Copilot

An AI assistant that drafts and sends replies inside Acme's customer support
inbox. Conversations are processed by Anthropic Claude; replies below the
confidence threshold are queued for a human support lead.

- `app/copilot/assistant.py` — the conversation loop
- `config/model_gateway.py` — provider configuration
- `app/copilot/retention.py` — 30-day conversation retention
- `app/copilot/redaction.py` — strips payment-shaped strings before provider calls
- `app/copilot/handoff.py` — human handoff queue
