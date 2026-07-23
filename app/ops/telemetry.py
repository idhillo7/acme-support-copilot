"""Minimal telemetry: counters to the log pipeline; no message bodies ever."""

import logging

log = logging.getLogger("copilot.telemetry")


def emit_counter(name: str, **labels: str) -> None:
    log.info("counter %s %s", name, labels)
