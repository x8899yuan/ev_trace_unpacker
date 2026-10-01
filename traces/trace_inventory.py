from __future__ import annotations

from pathlib import Path
from typing import List

from traces.trace_discovery import discover_traces
from traces.trace_validator import is_valid_trace


def build_trace_inventory(root_directory: Path) -> List[Path]:
    """
    Build an inventory of valid trace files.

    Workflow:
        1. Discover traces
        2. Validate traces
        3. Return valid traces only

    Args:
     ctory:
            Directory to search recursively.

    Returns:
        List of valid trace file paths.
    """

    discovered_traces = discover_traces(root_directory)

    valid_traces = [
        trace
        for trace in discovered_traces
        if is_valid_trace(trace)
    ]

    return valid_traces