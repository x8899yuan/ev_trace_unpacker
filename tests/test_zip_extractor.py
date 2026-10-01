from pathlib import Path
import zipfile

import pytest

from archives.extractors.zip_extractor import ZipExtractor


def test_can_extract_zip():
    extractor = ZipExtractor()

    assert extractor.can_extract(Path("trace.zip")) is True


def test_can_extract_non_zip():
    extractor = ZipExtractor()

    assert extractor.can_extract(Path("trace.7z")) is False


def test_extract_zip_archive(tmp_path):
    archive_file = tmp_path / "sample.zip"

    with zipfile.ZipFile(archive_file, "w") as archive:
        archive.writestr(
            "trace.blf",
            "test content"
        )

    output_directory = tmp_path / "output"

    extractor = ZipExtractor()

    extracted_files = extractor.extract(
        archive_file,
        output_directory
    )

    assert len(extracted_files) == 1

    extracted_file = output_directory / "trace.blf"

    assert extracted_file.exists()
    assert extracted_file in extracted_files


def test_extract_missing_archive_raises():
    extractor = ZipExtractor()

    with pytest.raises(FileNotFoundError):
        extractor.extract(
            Path("does_not_exist.zip"),
            Path("output")
        )


def test_extract_multiple_files(tmp_path):
    archive_file = tmp_path / "multi.zip"

    with zipfile.ZipFile(archive_file, "w") as archive:
        archive.writestr("trace1.blf", "data")
        archive.writestr("trace2.pcap", "data")
        archive.writestr("trace3.dlt", "data")

    output_directory = tmp_path / "output"

    extractor = ZipExtractor()

    extracted_files = extractor.extract(
        archive_file,
        output_directory
    )

    assert len(extracted_files) == 3


def test_extract_creates_output_directory(tmp_path):
    archive_file = tmp_path / "sample.zip"

    with zipfile.ZipFile(archive_file, "w") as archive:
        archive.writestr(
            "trace.blf",
            "content"
        )

    output_directory = tmp_path / "new_output"

    extractor = ZipExtractor()

    extractor.extract(
        archive_file,
        output_directory
    )

    assert output_directory.exists()
    assert output_directory.is_dir()