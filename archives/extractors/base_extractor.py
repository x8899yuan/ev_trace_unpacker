from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List


class BaseExtractor(ABC):
    """
    Base interface for all archive extractors.

    Examples:
        ZipExtractor
        SevenZipExtractor
    """

    @abstractmethod
    def can_extract(self, archive_path: Path) -> bool:
        """
        Determine whether this extractor supports the archive.

        Args:
            archive_path: Archive to inspect

        Returns:
            True if supported, otherwise False
        """
        pass

    @abstractmethod
    def extract(
        self,
        archive_path: Path,
        output_directory: Path
    ) -> List[Path]:
        """
        Extract an archive.

        Args:
            archive_path: Archive file
            output_directory: Destination folder

        Returns:
            List of         """
        pass