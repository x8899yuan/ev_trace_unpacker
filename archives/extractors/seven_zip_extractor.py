from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from typing import List

import py7zr

from archives.extractors.base_extractor import BaseExtractor


class SevenZipExtractor(BaseExtractor):
    """
    Extracts standard .7z archives and multipart .7z archives.

    Supported examples:

        archive.7z

        archive.7z.001
        archive.7z.002
        archive.7z.003
        archive.7z.004
    """

    def can_extract(self, archive_path: Path) -> bool:
        """
        Determine whether the archive is a supported .7z archive.
        """
        name = archive_path.name.lower()

        return (
            name.endswith(".7z")
            or name.endswith(".7z.001")
        )

    def extract(
        self,
        archive_path: Path,
        output_directory: Path
    ) -> List[Path]:
        """
        Extract a .7z archive.

        Args:
            archive_path:
                Path to archive.

            output_directory:
                Extraction       Returns:
            List of extracted files.
        """
        if not archive_path.exists():
            raise FileNotFoundError(
                f"Archive does not exist: {archive_path}"
            )

        output_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        temporary_archive = None
        archive_to_extract = archive_path

        try:
            if archive_path.name.lower().endswith(".7z.001"):
                temporary_archive = self._combine_multipart_archive(
                    archive_path
                )
                archive_to_extract = temporary_archive

            with py7zr.SevenZipFile(
                archive_to_extract,
                mode="r"
            ) as archive:
                archive.extractall(
                    path=output_directory
                )

        finally:
            if (
                temporary_archive is not None
                and temporary_archive.exists()
            ):
                temporary_archive.unlink()

        extracted_files = [
            path
            for path in output_directory.rglob("*")
            if path.is_file()
        ]

        return extracted_files

    def _combine_multipart_archive(
        self,
        archive_path: Path
    ) -> Path:
        """
        Combine archive.7z.001/.002/.003... into
        a temporary standard .7z file.
        """
        base_name = archive_path.name[:-4]

        archive_parts = sorted(
            archive_path.parent.glob(
                f"{base_name}.[0-9][0-9][0-9]"
            )
        )

        if not archive_parts:
            raise FileNotFoundError(
                f"No multipart archive parts found: {archive_path}"
            )

        temp_file = tempfile.NamedTemporaryFile(
            suffix=".7z",
            delete=False
        )

        temp_archive_path = Path(temp_file.name)

        temp_file.close()

        with open(
            temp_archive_path,
            "wb"
        ) as output_stream:

            for archive_part in archive_parts:

                with open(
                    archive_part,
                    "rb"
                ) as input_stream:

                    shutil.copyfileobj(
                        input_stream,
                        output_stream
                    )

        return temp_archive_path