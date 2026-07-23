create table conversations (
  id uuid primary key default gen_random_uuid(),
  customer_tier text not null default 'standard',
  started_at timestamptz not null default now()
);

create table conversation_queue (
  id uuid primary key default gen_random_uuid(),
  turns jsonb not null,
  customer_tier text not null default 'standard',
  enqueued_at timestamptz not null default now(),
  drafted_at timestamptz
);

create table reply_drafts (
  id uuid primary key default gen_random_uuid(),
  conversation_id text not null,
  body text,
  sent_by text not null,
  confidence numeric not null,
  created_at timestamptz not null default now()
);
