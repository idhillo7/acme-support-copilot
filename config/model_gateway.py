"""Provider configuration for the support copilot.

The gateway names exactly which model providers may receive conversation
content. Ops changes this file through review only.
"""

PRIMARY_PROVIDER = "anthropic"
PRIMARY_MODEL = "claude-sonnet-4-6"
FALLBACK_PROVIDER = None
FALLBACK_MODEL = None
RETRY_BEFORE_FALLBACK = 2
REQUEST_TIMEOUT_SECONDS = 30
MAX_OUTPUT_TOKENS = 700
