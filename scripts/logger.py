#!/usr/bin/env python3
from __future__ import annotations
import logging

# === Basic addition to the build in logger to support colors and tag prefixes ===
# Note that we don't do any additional support so this might not work in some consoles.

_RESET = "\x1b[0m"
_DIM = "\x1b[2m"
_BOLD = "\x1b[1m"

_BLUE = "\x1b[34m"
_YELLOW = "\x1b[33m"
_RED = "\x1b[31m"
_MAGENTA = "\x1b[35m"

_LEVEL_TO_LABEL = {
    logging.DEBUG: "[DEBUG]",
    logging.INFO: "[INFO]",
    logging.WARNING: "[WARN]",
    logging.ERROR: "[ERROR]",
    logging.CRITICAL: "[FATAL]",
}

_LEVEL_TO_COLOR = {
    logging.DEBUG: _DIM,
    logging.INFO: _BLUE,
    logging.WARNING: _YELLOW + _BOLD,
    logging.ERROR: _RED + _BOLD,
    logging.CRITICAL: _MAGENTA + _BOLD,
}

class _Formatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        ts = self.formatTime(record, "%H:%M:%S")
        msg = record.getMessage()
        label = _LEVEL_TO_LABEL.get(record.levelno, "[INFO]")
        color = _LEVEL_TO_COLOR.get(record.levelno, "")
        return f"{_DIM}{ts}{_RESET} | {color}{label}{_RESET} {msg}"

def setup_logging(level: int = logging.INFO) -> None:
    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()
    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(_Formatter())
    root.addHandler(handler)