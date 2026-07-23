from unittest.mock import MagicMock

from app.copilot.retention import purge_expired


def test_purge_calls_store_with_cutoff():
    store = MagicMock()
    store.delete_conversations_before.return_value = 3
    assert purge_expired(store) == 3
