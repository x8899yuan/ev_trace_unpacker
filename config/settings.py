"""
Application configuration for EV Trace Unpacker.

Responsibilities:
    - Define repository paths
    - Define supported archive formats
    - Define supported trace formats
    - Configure discovery behavior
    - Configure publishing behavior
    - Configure cleanup behavior

This module must NOT contain:
    - Archive extraction logic
    - Trace-file processing logic
    - BLF/PCAP/DLT parsing logic
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Settings:
    """
    Application settings.
    """

    project_root: Path

    # Data folders
    data_folder: Path
    incoming_folder: Path
    staging_folder: Path
    output_folder: Path

    # Trace output folders
    blf_output_folder: Path
    pcap_output_folder: Path
    dlt_output_folder: Path

    # Supported archive types
    supported_archive_extensions: tuple[str, ...]

    # Supported trace types
    supported_trace_extensions: tuple[str, ...]

    # Discovery behavior
    recursive_archive_search: bool
    recursive_trace_search: bool

    # Publishing behavior
    overwrite_existing_output: bool

    # Cleanup behavior
    cleanup_staging_after_success: bool
    cleanup_staging_after_failure: bool


def load_settings() -> Settings:
    """
    Load application settings.

    Returns:
        Validated Settings instance.
    """

    project_root = Path(__file__).resolve().parent.parent

    data_folder = project_root / "data"

    incoming_folder = data_folder / "incoming"
    staging_folder = data_folder / "staging"
    output_folder = data_folder / "output"

    blf_output_folder = output_folder / "blf"
    pcap_output_folder = output_folder / "pcap"
    dlt_output_folder = output_folder / "dlt"

    settings = Settings(
        project_root=project_root,
        data_folder=data_folder,
        incoming_folder=incoming_folder,
        staging_folder=staging_folder,
        output_folder=output_folder,
        blf_output_folder=blf_output_folder,
        pcap_output_folder=pcap_output_folder,
        dlt_output_folder=dlt_output_folder,
        supported_archive_extensions=(
            ".7z",
            ".zip",
        ),
        supported_trace_extensions=(
            ".blf",
            ".pcap",
            ".pcapng",
            ".dlt",
        ),
        recursive_archive_search=True,
        recursive_trace_search=True,
        overwrite_existing_output=False,
        cleanup_staging_after_success=True,
        cleanup_staging_after_failure=False,
    )

    create_required_folders(settings)

    return settings


def create_required_folders(settings: Settings) -> None:
    """
    Create required application folders if they do not exist.
    """

    required_folders = (
        settings.data_folder,
        settings.incoming_folder,
        settings.staging_folder,
        settings.output_folder,
        settings.blf_output_folder,
        settings.pcap_output_folder,
        settings.dlt_output_folder,
    )

    for folder in required_folders:
        folder.mkdir(
            parents=True,
            exist_ok=True,
        )


def is_supported_archive_file(file_path: Path) -> bool:
    """
    Return True if a file is a supported archive.
    """

    return (
        file_path.suffix.lower()
        in load_settings().supported_archive_extensions
    )


def is_supported_trace_file(file_path: Path) -> bool:
    """
    Return True if a file is a supported trace file.
    """

    return (
        file_path.suffix.lower()
        in load_settings().supported_trace_extensions
    )