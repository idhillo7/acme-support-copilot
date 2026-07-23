import datetime as dt

from app.copilot import retention


def test_retention_window_is_thirty_days():
    assert retention.RETENTION_DAYS == 30


def test_cutoff_is_in_the_past():
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=retention.RETENTION_DAYS)
    assert cutoff < dt.datetime.now(dt.timezone.utc)
