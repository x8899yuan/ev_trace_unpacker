"""
processing_status.py

Shared processing status enumeration used throughout
ev_trace_unpacker.
"""

from enum import Enum


class ProcessingStatus(str, Enum):
    """
    Common processing states used by validation,
    extraction, publishing, and overall workflow results.
    """

    SUCCESS = "success"
    PARTIAL_SUCCESS = "partial_success"
    FAILED = "failed"
    SKIPPED = "skipped"

    @property
    def is_success(self) -> bool:
        """
        Returns True only for fully successful operations.
        """
        return self == ProcessingStatus.SUCCESS

    @property
    def is_failure(self) -> bool:
        """
        Returns True only for failed operations.
        """
        return self == ProcessingStatus.FAILED