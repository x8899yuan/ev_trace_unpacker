"""
Archive type definitions and detection utilities.

Responsibilities:
    - Define supported archive types
    - Detect archive type from file extension
    - Provide centralized archive-type classification

This module must NOT contain:
    - Archive extraction logic
    - 7-Zip execution logic
    - Zip extraction logic
    - File discovery logic
"""

from enum import Enum
from pathlib import Path


class ArchiveType(str, Enum):
    """Supported archive types."""

    ZIP = "zip"
    SEVEN_ZIP = "7z"


def get_archive_type(file_path: Path) -> ArchiveType:
    """
    Determine the archive type from a file path.

    Args:
        file_path:
            Archive file path.

    Returns:
        ArchiveType corresponding to the file extension.

    Raises:
        ValueError:
            If the archive type is unsupported.
    """

    suffix = file_path.suffix.lower()
    filename = file_path.name.lower()

    if suffix == ".7z":
        return ArchiveType.SEVEN_ZIP

    if filename.endswith(".7z.001"):
        return ArchiveType.SEVEN_ZIP

    raise ValueError(
        f"Unsupported archive type: {file_path}"
    )


def is_zip_archive(file_path: Path) -> bool:
    """
    Return True if the archive is a ZIP file.
    """

    return file_path.suffix.lower() == ".zip"


def is_seven_zip_archive(file_path: Path) -> bool:
    """
    Return True if the archive is a 7-Zip file
    or the first segment of a multipart 7-Zip archive.
    """
    name = file_path.name.lower()

    return (
        name.endswith(".7z")
        or name.endswith(".7z.001")
    )