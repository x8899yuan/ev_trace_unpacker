from pathlib import Path

from archives.extractors.seven_zip_extractor import (
    SevenZipExtractor,
)


def test_can_extract_standard_7z():
    extractor = SevenZipExtractor()

    archive_path = Path(
        "example.7z"
    )

    assert extractor.can_extract(
        archive_path
    )


def test_can_extract_multipart_7z():
    extractor = SevenZipExtractor()

    archive_path = Path(
        "example.7z.001"
    )

    assert extractor.can_extract(
        archive_path
    )


def test_rebuild_multipart_archive(
    tmp_path,
):
    """
    Verify multipart archives are rebuilt
    into a temporary .7z file.
    """

    part_1 = tmp_path / "trace.7z.001"
    part_2 = tmp_path / "trace.7z.002"
    part_3 = tmp_path / "trace.7z.003"

    part_1.write_bytes(b"AAA")
    part_2.write_bytes(b"BBB")
    part_3.write_bytes(b"CCC")

    extractor = SevenZipExtractor()

    rebuilt_archive = (
        extractor._combine_multipart_archive(
            part_1
        )
    )

    try:

        assert rebuilt_archive.exists()

        assert (
            rebuilt_archive.read_bytes()
            == b"AAABBBCCC"
        )

    finally:

        if rebuilt_archive.exists():
            rebuilt_archive.unlink()


def test_rebuild_multipart_archive_missing_parts(
    tmp_path,
):
    """
    Verify a multipart archive can
    still be rebuilt from the files
    that are present.
    """

    part_1 = tmp_path / "trace.7z.001"

    part_1.write_bytes(
        b"ONLY_ONE_PART"
    )

    extractor = SevenZipExtractor()

    rebuilt_archive = (
        extractor._combine_multipart_archive(
            part_1
        )
    )

    try:

        assert rebuilt_archive.exists()

        assert (
            rebuilt_archive.read_bytes()
            == b"ONLY_ONE_PART"
        )

    finally:

        if rebuilt_archive.exists():
            rebuilt_archive.unlink()