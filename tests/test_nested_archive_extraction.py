from pathlib import Path

from services.archive_extraction_service import (
    ArchiveExtractionService,
)


class MockExtractor:
    def __init__(self, extracted_files):
        self._extracted_files = extracted_files

    def extract(self, archive_path, output_directory):
        return self._extracted_files


def test_extract_archive_returns_nested_files(
    monkeypatch,
    tmp_path,
):
    """
    Verify nested archives are recursively processed.

    archive.7z
        -> trace.zip
            -> trace.blf
    """

    archive_7z = tmp_path / "archive.7z"
    archive_7z.touch()

    trace_zip = tmp_path / "trace.zip"
    trace_zip.touch()

    trace_blf = tmp_path / "trace.blf"
    trace_blf.touch()

    extractors = {
        archive_7z.resolve(): MockExtractor(
            [trace_zip]
        ),
        trace_zip.resolve(): MockExtractor(
            [trace_blf]
        ),
    }

    def mock_get_extractor(
        archive_path,
    ):
        return extractors[
            archive_path.resolve()
        ]

    monkeypatch.setattr(
        "services.archive_extraction_service."
        "ExtractorFactory.get_extractor",
        mock_get_extractor,
    )

    service = ArchiveExtractionService()

    extracted_files = service.extract_archive(
        archive_7z,
        tmp_path,
    )

    assert trace_blf in extracted_files


def test_nested_archive_processed_once(
    monkeypatch,
    tmp_path,
):
    """
    Verify nested archives are not processed repeatedly.
    """

    archive_7z = tmp_path / "archive.7z"
    archive_7z.touch()

    trace_zip = tmp_path / "trace.zip"
    trace_zip.touch()

    trace_blf = tmp_path / "trace.blf"
    trace_blf.touch()

    extraction_calls = []

    class TrackingExtractor:
        def __init__(
            self,
            extracted_files,
        ):
            self._extracted_files = extracted_files

        def extract(
            self,
            archive_path,
            output_directory,
        ):
            extraction_calls.append(
                archive_path.resolve()
            )
            return self._extracted_files

    extractors = {
        archive_7z.resolve(): TrackingExtractor(
            [trace_zip]
        ),
        trace_zip.resolve(): TrackingExtractor(
            [
                trace_zip,
                trace_blf,
            ]
        ),
    }

    def mock_get_extractor(
        archive_path,
    ):
        return extractors[
            archive_path.resolve()
        ]

    monkeypatch.setattr(
        "services.archive_extraction_service."
        "ExtractorFactory.get_extractor",
        mock_get_extractor,
    )

    service = ArchiveExtractionService()

    service.extract_archive(
        archive_7z,
        tmp_path,
    )

    assert (
        extraction_calls.count(
            trace_zip.resolve()
        )
        == 1
    )