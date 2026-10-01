"""Tests for archives.archive_discovery."""

from dataclasses import replace
from pathlib import Path

import pytest

from archives.archive_discovery import discover_archives
from config.settings import Settings
from exceptions import ArchiveDiscoveryError


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    """Return isolated settings for archive-discovery tests."""

    data_folder = tmp_path / "data"
    incoming_folder = data_folder / "incoming"
    staging_folder = data_folder / "staging"
    output_folder = data_folder / "output"

    incoming_folder.mkdir(parents=True)

    return Settings(
        project_root=tmp_path,
        data_folder=data_folder,
        incoming_folder=incoming_folder,
        staging_folder=staging_folder,
        output_folder=output_folder,
        blf_output_folder=output_folder / "blf",
        pcap_output_folder=output_folder / "pcap",
        dlt_output_folder=output_folder / "dlt",
        supported_archive_extensions=(".7z", ".zip"),
        supported_trace_extensions=(".blf", ".pcap", ".pcapng", ".dlt"),
        recursive_archive_search=True,
        recursive_trace_search=True,
        overwrite_existing_output=False,
        cleanup_staging_after_success=True,
        cleanup_staging_after_failure=False,
    )


def test_discovers_supported_7z_and_zip_archives(settings: Settings) -> None:
    """Supported 7Z and ZIP files should be returned."""

    seven_zip = settings.incoming_folder / "vehicle_trace.7z"
    zip_file = settings.incoming_folder / "network_trace.zip"

    seven_zip.touch()
    zip_file.touch()

    result = discover_archives(settings)

    assert result == sorted(
        [seven_zip.resolve(), zip_file.resolve()],
        key=lambda path: str(path).casefold(),
    )


def test_archive_extensions_are_case_insensitive(settings: Settings) -> None:
    """Uppercase archive extensions should be supported."""

    uppercase_7z = settings.incoming_folder / "TRACE.7Z"
    uppercase_zip = settings.incoming_folder / "LOGS.ZIP"

    uppercase_7z.touch()
    uppercase_zip.touch()

    result = discover_archives(settings)

    assert uppercase_7z.resolve() in result
    assert uppercase_zip.resolve() in result


def test_ignores_unsupported_files(settings: Settings) -> None:
    """Files not listed in the archive settings should be ignored."""

    supported = settings.incoming_folder / "supported.zip"
    unsupported_rar = settings.incoming_folder / "unsupported.rar"
    trace_file = settings.incoming_folder / "already_extracted.blf"
    text_file = settings.incoming_folder / "notes.txt"

    for file_path in (
        supported,
        unsupported_rar,
        trace_file,
        text_file,
    ):
        file_path.touch()

    result = discover_archives(settings)

    assert result == [supported.resolve()]


def test_ignores_directories_with_archive_suffix(settings: Settings) -> None:
    """A directory whose name ends with an archive suffix is not a file."""

    archive_named_directory = settings.incoming_folder / "not_an_archive.zip"
    archive_named_directory.mkdir()

    assert discover_archives(settings) == []


def test_recursive_search_finds_nested_archives(settings: Settings) -> None:
    """Recursive discovery should include archives in nested folders."""

    nested_folder = settings.incoming_folder / "vehicle" / "session_001"
    nested_folder.mkdir(parents=True)

    nested_archive = nested_folder / "trace_package.7z"
    nested_archive.touch()

    assert discover_archives(settings) == [nested_archive.resolve()]


def test_nonrecursive_search_ignores_nested_archives(settings: Settings) -> None:
    """Top-level discovery should not include nested archives."""

    top_level_archive = settings.incoming_folder / "top_level.zip"
    top_level_archive.touch()

    nested_folder = settings.incoming_folder / "nested"
    nested_folder.mkdir()
    nested_archive = nested_folder / "nested.7z"
    nested_archive.touch()

    nonrecursive_settings = replace(
        settings,
        recursive_archive_search=False,
    )

    assert discover_archives(nonrecursive_settings) == [
        top_level_archive.resolve()
    ]


def test_returns_empty_list_when_no_archives_exist(settings: Settings) -> None:
    """An empty incoming folder should produce an empty result."""

    assert discover_archives(settings) == []


def test_results_are_sorted_case_insensitively(settings: Settings) -> None:
    """Discovery order should be deterministic."""

    archive_names = (
        "zeta.zip",
        "Alpha.7z",
        "middle.ZIP",
    )

    for archive_name in archive_names:
        (settings.incoming_folder / archive_name).touch()

    result = discover_archives(settings)

    assert [path.name for path in result] == [
        "Alpha.7z",
        "middle.ZIP",
        "zeta.zip",
    ]


def test_missing_incoming_folder_raises_error(settings: Settings) -> None:
    """A missing incoming folder should raise ArchiveDiscoveryError."""

    missing_folder_settings = replace(
        settings,
        incoming_folder=settings.data_folder / "missing",
    )

    with pytest.raises(
        ArchiveDiscoveryError,
        match="Incoming folder does not exist",
    ):
        discover_archives(missing_folder_settings)


def test_incoming_path_must_be_directory(
    settings: Settings,
    tmp_path: Path,
) -> None:
    """A file configured as the incoming folder should be rejected."""

    incoming_file = tmp_path / "incoming_is_a_file"
    incoming_file.touch()

    invalid_settings = replace(
        settings,
        incoming_folder=incoming_file,
    )

    with pytest.raises(
        ArchiveDiscoveryError,
        match="Incoming path is not a directory",
    ):
        discover_archives(invalid_settings)
