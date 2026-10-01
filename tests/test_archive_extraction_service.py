from pathlib import Path
from unittest.mock import Mock

from services.archive_extraction_service import (
    ArchiveExtractionService,
)


def test_extract_archive_requests_extractor(
    monkeypatch,
    tmp_path,
):
    archive_path = tmp_path / "sample.zip"
    archive_path.touch()

    mock_extractor = Mock()
    mock_extractor.extract.return_value = []

    mock_get_extractor = Mock(
        return_value=mock_extractor
    )

    monkeypatch.setattr(
        "services.archive_extraction_service.ExtractorFactory.get_extractor",
        mock_get_extractor,
    )

    service = ArchiveExtractionService()

    service.extract_archive(
        archive_path,
        Path("output"),
    )

    mock_get_extractor.assert_called_once_with(
        archive_path.resolve()
    )


def test_extract_archive_calls_extractor(
    monkeypatch,
    tmp_path,
):
    archive_path = tmp_path / "sample.zip"
    archive_path.touch()

    trace_file = tmp_path / "trace.blf"
    trace_file.touch()

    mock_extractor = Mock()
    mock_extractor.extract.return_value = [
        trace_file,
    ]

    monkeypatch.setattr(
        "services.archive_extraction_service.ExtractorFactory.get_extractor",
        Mock(
            return_value=mock_extractor,
        ),
    )

    service = ArchiveExtractionService()

    service.extract_archive(
        archive_path,
        Path("output"),
    )

    mock_extractor.extract.assert_called_once_with(
        archive_path.resolve(),
        Path("output"),
    )