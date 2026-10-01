"""
Archive validation for EV Trace Unpacker.

This module validates archive files discovered by
archive_discovery.py before they enter the extraction workflow.
"""

from pathlib import Path

from config.settings import Settings, load_settings
from exceptions import ArchiveValidationError


def validate_archive(
    archive_path: Path,
    settings: Settings | None = None,
) -> Path:
    """
    Validate a single archive file.

    Args:
        archive_path:
            Archive file to validate.

        settings:
            Optional application settings.

    Returns:
        Resolved validated archive path.

    Raises:
        ArchiveValidationError:
            If validation fails.
    """

    active_settings = settings or load_settings()

    archive_path = archive_path.resolve()

    _validate_exists(archive_path)
    _validate_is_file(archive_path)
    _validate_extension(
        archive_path,
        active_settings,
    )
    _validate_not_empty(archive_path)
    _validate_readable(archive_path)

    return archive_path


def validate_archives(
    archive_paths: list[Path],
    settings: Settings | None = None,
) -> list[Path]:
    """
    Validate multiple archive files.

    Args:
        archive_paths:
            Candidate archive files.

        settings:
            Optional application settings.

    Returns:
        List of validated archive paths.

    Raises:
        ArchiveValidationError:
            If any archive fails
    """

    active_settings = settings or load_settings()

    return [
        validate_archive(
            archive_path,
            active_settings,
        )
        for archive_path in archive_paths
    ]


def _validate_exists(
    archive_path: Path,
) -> None:
    """
    Ensure archive exists.
    """

    if not archive_path.exists():
        raise ArchiveValidationError(
            f"Archive does not exist: {archive_path}"
        )


def _validate_is_file(
    archive_path: Path,
) -> None:
    """
    Ensure path is a file.
    """

    if not archive_path.is_file():
        raise ArchiveValidationError(
            f"Archive is not a file: {archive_path}"
        )


def _validate_extension(
    archive_path: Path,
    settings: Settings,
) -> None:
    """
    Ensure extension is supported.
    """

    supported_extensions = {
        extension.lower()
        for extension
        in settings.supported_archive_extensions
    }

    if archive_path.suffix.lower() not in supported_extensions:
        raise ArchiveValidationError(
            f"Unsupported archive type: {archive_path}"
        )


def _validate_not_empty(
    archive_path: Path,
) -> None:
    """
    Ensure archive is not empty.
    """

    if archive_path.stat().st_size == 0:
        raise ArchiveValidationError(
            f"Archive is empty: {archive_path}"
        )


def _validate_readable(
    archive_path: Path,
) -> None:
    """
    Ensure archive can be opened.
    """

    try:
        with archive_path.open("rb"):
            pass

    except OSError as exc:
        raise ArchiveValidationError(
            f"Archive is not readable: {archive_path}"
        ) from exc