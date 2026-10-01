from pathlib import Path

import pytest

from config.settings import Settings
from exceptions import ArchiveValidationError
from validators.archive.archive_validator import (
    validate_archive,
    validate_archives,
)


def create_test_settings() -> Settings:
    """
    Create settings suitable for archive validator testing.
    """
    project_root = Path(".")

    return Settings(
        project_root=project_root,
        data_folder=project_root / "data",
        incoming_folder=project_root / "incoming",
        staging_folder=project_root / "staging",
        output_folder=project_root / "output",
        blf_output_folder=project_root / "output" / "blf",
        pcap_output_folder=project_root / "output" / "pcap",
        dlt_output_folder=project_root / "output" / "dlt",
        supported_archive_extensions=(
            ".7z",
            ".zip",
        ),
        supported_trace_extensions=(
            ".blf",
            ".pcap",
            ".dlt",
        ),
        recursive_archive_search=True,
        recursive_trace_search=True,
        overwrite_existing_output=False,
        cleanup_staging_after_success=False,
        cleanup_staging_after_failure=False,
    )



def test_valid_zip_archive_passes(tmp_path):
    archive = tmp_path / "sample.zip"
    archive.write_bytes(b"test")

    result = validate_archive(
        archive,
        create_test_settings(),
    )

    assert result == archive.resolve()


def test_valid_7z_archive_passes(tmp_path):
    archive = tmp_path / "sample.7z"
    archive.write_bytes(b"test")

    result = validate_archive(
        archive,
        create_test_settings(),
    )

    assert result == archive.resolve()


def test_extension_is_case_insensitive(tmp_path):
    archive = tmp_path / "sample.ZIP"
    archive.write_bytes(b"test")

    result = validate_archive(
        archive,
        create_test_settings(),
    )

    assert result == archive.resolve()


def test_missing_file_raises_error(tmp_path):
    archive = tmp_path / "missing.zip"

    with pytest.raises(ArchiveValidationError):
        validate_archive(
            archive,
            create_test_settings(),
        )


def test_directory_is_not_valid_archive(tmp_path):
    archive_dir = tmp_path / "archive.zip"
    archive_dir.mkdir()

    with pytest.raises(ArchiveValidationError):
        validate_archive(
            archive_dir,
            create_test_settings(),
        )


def test_unsupported_extension_raises_error(tmp_path):
    archive = tmp_path / "sample.rar"
    archive.write_bytes(b"test")

    with pytest.raises(ArchiveValidationError):
        validate_archive(
            archive,
            create_test_settings(),
        )


def test_empty_archive_raises_error(tmp_path):
    archive = tmp_path / "empty.zip"
    archive.touch()

    with pytest.raises(ArchiveValidationError):
        validate_archive(
            archive,
            create_test_settings(),
        )


def test_validate_multiple_archives(tmp_path):
    archive1 = tmp_path / "a.zip"
    archive2 = tmp_path / "b.7z"

    archive1.write_bytes(b"test")
    archive2.write_bytes(b"test")

    results = validate_archives(
        [archive1, archive2],
        create_test_settings(),
    )

    assert len(results) == 2
    assert archive1.resolve() in results
    assert archive2.resolve() in results


def test_validate_archives_fails_when_one_invalid(tmp_path):
    valid_archive = tmp_path / "valid.zip"
    invalid_archive = tmp_path / "invalid.rar"

    valid_archive.write_bytes(b"test")
    invalid_archive.write_bytes(b"test")

    with pytest.raises(ArchiveValidationError):
        validate_archives(
            [valid_archive, invalid_archive],
            create_test_settings(),
        )


def test_returns_resolved_path(tmp_path):
    archive = tmp_path / "archive.zip"
    archive.write_bytes(b"test")

    result = validate_archive(
        archive,
        create_test_settings(),
    )

    assert result.is_absolute()