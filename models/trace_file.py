"""
trace_file.py

Trace file models used throughout ev_trace_unpacker.
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class TraceType(str, Enum):
    """
    Supported trace file types.
    """

    BLF = "blf"
    PCAP = "pcap"
    PCAPNG = "pcapng"
    DLT = "dlt"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class TraceCandidate:
    """
    Represents a discovered file before classification.
    """

    source_path: Path
    relative_path: Path
    source_archive_id: str
    size_bytes: int


@dataclass(frozen=True)
class TraceFile:
    """
    Represents a classified trace file.
    """

    candidate: TraceCandidate
    trace_type: TraceType

    @property
    def source_path(self) -> Path:
        return self.candidate.source_path

    @property
    def filename(self) -> str:
        return self.candidate.source_path.name

    @property
    def size_bytes(self) -> int:
        return self.candidate.size_bytes