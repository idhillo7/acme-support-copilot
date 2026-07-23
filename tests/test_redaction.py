from app.copilot.redaction import redact_payment_shapes


def test_card_numbers_never_survive():
    assert "4111 1111 1111 1111" not in redact_payment_shapes(
        "my card is 4111 1111 1111 1111 thanks"
    )
