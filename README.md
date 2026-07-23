# Acme Support Copilot

The AI assistant inside Acme's customer support inbox. It reads an open
conversation, drafts a reply with Anthropic Claude, and either sends it or
queues it for a human support lead when confidence is low.

## How it runs

- `app/server.py` — HTTP surface the support product calls (`/v1/draft-reply`,
  `/v1/conversations/enqueue`).
- `app/ops/draft_worker.py` — background worker draining the conversation
  queue; deployed as the `worker` service in `docker-compose.yml`.
- `config/model_gateway.py` — the single authority on model providers.
  Anthropic only; there is no fallback provider.
- `app/copilot/redaction.py` — payment-shaped strings never reach a provider.
- `app/copilot/retention.py` — conversations are deleted after 30 days.
- `app/copilot/handoff.py` — a person can be requested at any point.

## Operating facts recipients rely on

- Customer conversations are processed exclusively by Anthropic Claude models.
- Conversation data is retained for 30 days, then deleted.
- Prompts and outputs are logged as counters only — never message bodies.

## Deploy

CI runs on every push (`.github/workflows/ci.yml`). Production runs the two
containers in `docker-compose.yml` behind the platform load balancer.
