from __future__ import annotations

import zipfile
from pathlib import Path
from typing import List

from archives.extractors.base_extractor import BaseExtractor


class ZipExtractor(BaseExtractor):
    """
    Extracts standard ZIP archives.
    """

    def can_extract(self, archive_path: Path) -> bool:
        """
        Determine whether the archive is a ZIP file.

        Args:
            archive_path: Archive file to inspect

        Returns:
            True if supported
        """
        return archive_path.suffix.lower() == ".zip"

    def extract(
        self,
        archive_path: Path,
        output_directory: Path
    ) -> List[Path]:
        """
        Extract a ZIP archive.

        Args:
            archive_path: ZIP archive path
            output_directory: Destination folder

        Returns:
            List of extracted files

        Raises:
            FileNotFoundError  If archive does not exist

            zipfile.BadZipFile:
                If archive is invalid
        """

        if not archive_path.exists():
            raise FileNotFoundError(
                f"Archive does not exist: {archive_path}"
            )

        output_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        with zipfile.ZipFile(
            archive_path,
            mode="r"
        ) as archive:

            archive.extractall(output_directory)

        extracted_files: List[Path] = [
            path
            for path in output_directory.rglob("*")
            if path.is_file()
        ]

        return extracted_files