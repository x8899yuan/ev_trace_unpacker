from pathlib import Path

from services.archive_extraction_service import (
    ArchiveExtractionService,
)
from services.archive_processing_service import (
    ArchiveProcessingService,
)


class ArchiveIngestionService:
    """
    Top-level orchestration service for archive ingestion.

    Workflow:
        1. Extract archive
        2. Discover traces
        3. Validate traces
        4. Build trace inventory
        5. Return inventory
    """

    def __init__(self) -> None:
        self._extraction_service = ArchiveExtractionService()
        self._processing_service = ArchiveProcessingService()

    def ingest_archive(
        self,
        archive_path: Path,
        extraction_directory: Path,
    ) -> list:
        """
        Ingest an archive and return a trace inventory.

        Args:
            archive_path:
                Path to the archive package.

            extraction_directory:
                Directory where archive contents
                will be extracted.

        Returns:
            A validated trace inventory.
        """

        self._extraction_service.extract_archive(
            archive_path,
            extraction_directory,
        )

        return self._processing_service.build_trace_inventory(
            extraction_directory,
        )