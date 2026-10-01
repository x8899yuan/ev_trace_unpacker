from __future__ import annotations

from pathlib import Path

from archives.extractors.base_extractor import BaseExtractor
from archives.extractors.seven_zip_extractor import SevenZipExtractor
from archives.extractors.zip_extractor import ZipExtractor


class ExtractorFactory:
    """
    Factory for selecting the appropriate archive extractor.
    """

    _EXTRACTORS = (
        ZipExtractor(),
        SevenZipExtractor(),
    )

    @classmethod
    def get_extractor(
        cls,
        archive_path: Path
    ) -> BaseExtractor:
        """
        Return the appropriate extractor for the archive.

        Args:
            archive_path: Archive file path

        Returns:
            BaseExtractor implementation

        Raises:
            ValueError:
                If no extractor supports the archive
        """

        for extractor in cls._EXTRACTORS:
            if extractor.can_extract(archive_path):
                return extractor

        raise ValueError(
            f"No extractor available for archive: {archive_path}"
        )