"""
processing_result.py

Processing result models used throughout ev_trace_unpacker.
"""

from dataclasses import dataclass

from models.archive_info import ArchivePackage
from models.processing_status import ProcessingStatus
from models.publish_result import PublishResult


@dataclass(frozen=True)
class ArchiveProcessingResult:
    """
    Final result for processing a single archive package.
    """

    archive: ArchivePackage
    status: ProcessingStatus

    discovered_file_count: int = 0
    classified_trace_count: int = 0
    ignored_file_count: int = 0

    publish_results: tuple[PublishResult, ...] = ()

    errors: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()

    @property
    def successful_publish_count(self) -> int:
        return sum(
            1
            for result in self.publish_results
            if result