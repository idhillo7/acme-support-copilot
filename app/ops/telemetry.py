# Copyright 2026 Acme Inc. Licensed under Apache-2.0.
"""Minimal telemetry: counters to the log pipeline; no message bodies ever.

Prompts and outputs are observable only as counts and labels — the logging
promise in the README is enforced by this being the only telemetry seam.
"""

import logging

log = logging.getLogger("copilot.telemetry")


def emit_counter(name: str, **labels: str) -> None:
    log.info("counter %s %s", name, labels)
