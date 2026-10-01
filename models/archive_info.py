"""
archive_info.py

Core archive-related models used throughout ev_trace_unpacker.
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class ArchiveType(str, Enum):
    """
    Supported archive types.
    """

    SEVEN_ZIP = "7z"
    ZIP = "zip"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ArchivePackage:
    """
    Represents a logical archive package.

    Examples

    Single-file archive:
        Vehicle_A.zip

    Multipart archive:
        Vehicle_B.7z.001
        Vehicle_B.7z.002
        Vehicle_B.7z.003
    """

    package_id: str
    primary_path: Path
    archive_type: ArchiveType
    parts: tuple[Path, ...]
    is_multipart: bool

    @property
    def display_name(self) -> str:
        """
        Human-readable archive name.
        """
        return self.primary_path.name

    @property
    def part_count(self) -> int:
        """
        Number of files that make up this package.
        """
        return len(self.parts)