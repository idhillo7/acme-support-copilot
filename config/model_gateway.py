"""Provider configuration for the support copilot.

This file is the single authority on which model providers may receive
customer conversation content. Changing it is a security-relevant act and
goes through review: recipients of Acme's security answers are told exactly
which providers process conversation data, and this configuration is the
source of that statement.
"""

PRIMARY_PROVIDER = "anthropic"
PRIMARY_MODEL = "claude-sonnet-4-6"

# Fallback provider added for the Q3 availability incident review: when the
# primary is unavailable after retries, conversations route to OpenAI GPT-5
# instead of queueing for a person.
FALLBACK_PROVIDER = "openai"
FALLBACK_MODEL = "gpt-5"

RETRY_BEFORE_FALLBACK = 2
REQUEST_TIMEOUT_SECONDS = 30
MAX_OUTPUT_TOKENS = 700
