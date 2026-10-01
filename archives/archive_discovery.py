"""Discover supported archive files for EV Trace Unpacker.

This module is responsible only for locating supported archive files in the
configured incoming folder. It does not validate archive contents, group
multipart sets, merge files, or extract archives.
"""

from pathlib import Path

from config.settings import Settings, load_settings
from exceptions import ArchiveDiscoveryError


def discover_archives(settings: Settings | None = None) -> list[Path]:
    active_settings = settings or load_settings()
    incoming_folder = active_settings.incoming_folder

    _validate_incoming_folder(incoming_folder)

    supported_extensions = {
        extension.lower()
        for extension in active_settings.supported_archive_extensions
    }

    try:
        candidates = (
            incoming_folder.rglob("*")
            if active_settings.recursive_archive_search
            else incoming_folder.glob("*")
        )

        archive_paths = {
            candidate.resolve()
            for candidate in candidates
            if candidate.is_file()
            and candidate.suffix.lower() in supported_extensions
        }

    except OSError as exc:
        raise ArchiveDiscoveryError(
            f"Failed to discover archives in: {incoming_folder}"
        ) from exc

    return sorted(
        archive_paths,
        key=lambda path: str(path).casefold(),
    )


def _validate_incoming_folder(incoming_folder: Path) -> None:
    """Validate the configured incoming folder before discovery."""

    if not incoming_folder.exists():
        raise ArchiveDiscoveryError(
            f"Incoming folder does not exist: {incoming_folder}"
        )

    if not incoming_folder.is_dir():
        raise ArchiveDiscoveryError(
            f"Incoming path is not a directory: {incoming_folder}"
        )
