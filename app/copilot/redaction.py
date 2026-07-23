"""Payment-shaped strings never reach a model provider."""

import re

_CARD = re.compile(r"\b(?:\d[ -]*?){13,19}\b")
_IBAN = re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{10,30}\b")


def redact_payment_shapes(text: str) -> str:
    text = _CARD.sub("[redacted-card]", text)
    return _IBAN.sub("[redacted-iban]", text)
