from pathlib import Path

from archives.archive_discovery import discover_archives
from services.trace_inventory_service import TraceInventoryService
from validators.archive.archive_validator import validate_archives


class ArchiveProcessingService:
    """Coordinate archive discovery and trace inventory creation."""

    def __init__(self) -> None:
        self._trace_inventory_service = TraceInventoryService()

    def discover_valid_archives(
        self,
        root_directory: Path,
    ) -> list[Path]:
        discovered_archives = discover_archives(root_directory)

        return [
            archive
            for archive in discovered_archives
            if validate_archives(archive)
        ]

    def build_trace_inventory(
        self,
        extracted_directory: Path,
    ) -> list[Path]:
        return self._trace_inventory_service.build(extracted_directory)
