"""
publish_result.py

Publishing-related models used by ev_trace_unpacker.
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from models.processing_status import ProcessingStatus
from models.trace_file import TraceFile


class PublishCollisionPolicy(str, Enum):
    """
    Defines behavior when a destination file already exists.
    """

    RENAME = "rename"
    SKIP = "skip"
    FAIL = "fail"


@dataclass(frozen=True)
class PublishResult:
    """
    Result of publishing a trace file to the final output area.
    """

    trace_file: TraceFile
    status: ProcessingStatus
    destination_path: Path | None
    renamed: bool = False
    error: str | None = None

    @property
    def succeeded(self) -> bool:
        """
        Convenience helper for success checks.
        """
        return self.status == ProcessingStatus.SUCCESS

    @property
    def failed(self) -> bool:
        """
        Convenience helper for failure checks.
        """
        return self.status == ProcessingStatus.FAILED
`