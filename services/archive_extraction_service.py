from pathlib import Path
from typing import List, Set

from archives.extractor_factory import ExtractorFactory


class ArchiveExtractionService:
    """
    Coordinate standard, multipart, and nested archive extraction.
    """

    _NESTED_ARCHIVE_SUFFIXES = {".zip", ".7z"}

    def extract_archive(
        self,
        archive_path: Path,
        output_directory: Path,
    ) -> List[Path]:
        """
        Extract an archive and recursively process nested archives.
        """
        processed_archives: Set[Path] = set()

        return self._extract_recursive(
            archive_path=archive_path,
            output_directory=output_directory,
            processed_archives=processed_archives,
        )

    def _extract_recursive(
        self,
        archive_path: Path,
        output_directory: Path,
        processed_archives: Set[Path],
    ) -> List[Path]:
        """
        Extract one archive and process nested archives.
        """
        archive_path = archive_path.resolve()

        if archive_path in processed_archives:
            return []

        processed_archives.add(archive_path)

        extractor = ExtractorFactory.get_extractor(archive_path)

        extracted_files = extractor.extract(
            archive_path,
            output_directory,
        )

        all_files = list(extracted_files)

        for extracted_file in extracted_files:
            extracted_file = extracted_file.resolve()

            if not self._is_nested_archive(extracted_file):
                continue

            if extracted_file in processed_archives:
                continue

            nested_files = self._extract_recursive(
                archive_path=extracted_file,
                output_directory=extracted_file.parent,
                processed_archives=processed_archives,
            )

            all_files.extend(nested_files)

        return self._unique_paths(all_files)

    def _is_nested_archive(
        self,
        file_path: Path,
    ) -> bool:
        """
        Return True if the file is a supported archive.
        """
        return file_path.suffix.lower() in self._NESTED_ARCHIVE_SUFFIXES

    @staticmethod
    def _unique_paths(
        paths: List[Path],
    ) -> List[Path]:
        """
        Remove duplicate paths while preserving order.
        """
        return list(dict.fromkeys(paths))
