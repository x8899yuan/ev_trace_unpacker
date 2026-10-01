from __future__ import annotations

from pathlib import Path


SUPPORTED_TRACE_EXTENSIONS = {
    ".blf",
    ".pcap",
    ".dlt",
}


def is_valid_trace(trace_path: Path) -> bool:
    """
    Validate a trace file.

    Validation rules:
        - File exists
        - Path is a file
        - Supported extension
        - File size > 0

    Args:
        trace_path:
            Trace file to validate

    Returns:
        True if valid, otherwise False.
    """

    if not trace_path.exists():
        return False

    if not trace_path.is_file():
        return False

    if trace_path.suffix.lower() not in SUPPORTED_TRACE_EXTENSIONS:
        return False

    if trace_path.stat().st_size <= 0:
        return False

    return True