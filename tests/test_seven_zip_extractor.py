from pathlib import Path

import py7zr
import pytest

from archives.extractors.seven_zip_extractor import SevenZipExtractor


def test_can_extract_7z():
    extractor = SevenZipExtractor()

    assert extractor.can_extract(Path("trace.7z")) is True


def test_can_extract_non_7z():
    extractor = SevenZipExtractor()

    assert extractor.can_extract(Path("trace.zip")) is False


def test_extract_missing_archive_raises():
    extractor = SevenZipExtractor()

    with pytest.raises(FileNotFoundError):
        extractor.extract(
            Path("does_not_exist.7z"),
            Path("output")
        )


def test_extract_7z_archive(tmp_path):
    archive_file = tmp_path / "sample.7z"

    input_file = tmp_path / "trace.blf"
    input_file.write_text("test content")

    with py7zr.SevenZipFile(archive_file, "w") as archive:
        archive.write(input_file, arcname="trace.blf")

    output_directory = tmp_path / "output"

    extractor = SevenZipExtractor()

    extracted_files = extractor.extract(
        archive_file,
        output_directory
    )

    extracted_file = output_directory / "trace.blf"

    assert extracted_file.exists()
    assert extracted_file in extracted_files
    assert len(extracted_files) == 1


def test_extract_creates_output_directory(tmp_path):
    archive_file = tmp_path / "sample.7z"

    input_file = tmp_path / "trace.blf"
    input_file.write_text("test")

    with py7zr.SevenZipFile(archive_file, "w") as archive:
        archive.write(input_file, arcname="trace.blf")

    output_directory = tmp_path / "new_output"

    extractor = SevenZipExtractor()

    extractor.extract(
        archive_file,
        output_directory
    )

    assert output_directory.exists()
    assert output_directory.is_dir()


def test_extract_multiple_files(tmp_path):
    archive_file = tmp_path / "multi.7z"

    file1 = tmp_path / "trace1.blf"
    file2 = tmp_path / "trace2.pcap"
    file3 = tmp_path / "trace3.dlt"

    file1.write_text("a")
    file2.write_text("b")
    file3.write_text("c")

    with py7zr.SevenZipFile(archive_file, "w") as archive:
        archive.write(file1, arcname="trace1.blf")
        archive.write(file2, arcname="trace2.pcap")
        archive.write(file3, arcname="trace3.dlt")

    output_directory = tmp_path / "output"

    extractor = SevenZipExtractor()

    extracted_files = extractor.extract(
        archive_file,
        output_directory
    )

    assert len(extracted_files) == 3