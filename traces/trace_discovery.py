from __future__ import annotations

from pathlib import Path
from typing import List, Set


SUPPORTED_TRACE_EXTENSIONS: Set[str] = {
    ".blf",
    ".pcap",
    ".dlt",
}


def discover_traces(root_directory: Path) -> List[Path]:
    """
    Recursively discover supported trace files.

    Args:
        root_directory:
            Directory to search.

    Returns:
        Sorted list of discovered trace files.

    Raises:
        FileNotFoundError:
            If the directory does not exist.

        NotADirectoryError  If the path is not a directory.
    """

    if not root_directory.exists():
        raise FileNotFoundError(
            f"Directory does not exist: {root_directory}"
        )

    if not root_directory.is_dir():
        raise NotADirectoryError(
            f"Path is not a directory: {root_directory}"
        )

    traces = [
        path
        for path in root_directory.rglob("*")
        if path.is_file()
        and path.suffix.lower() in SUPPORTED_TRACE_EXTENSIONS
    ]

    return sorted(traces)