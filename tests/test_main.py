from pathlib import Path
from unittest.mock import Mock, patch

import main


def test_main_returns_error_when_archive_missing(
    capsys,
):
    """
    Verify usage information is displayed when
    no archive path is supplied.
    """
    with patch(
        "sys.argv",
        ["main.py"],
    ):
        result = main.main()

    captured = capsys.readouterr()

    assert result == 1
    assert (
        "Usage: python main.py <archive_path>"
        in captured.out
    )


def test_main_returns_success_for_empty_inventory(
    capsys,
):
    """
    Verify successful execution when no traces
    are discovered.
    """
    archive_path = "sample.zip"

    with patch(
        "sys.argv",
        ["main.py", archive_path],
    ):
        with patch(
            "main.ArchiveIngestionService"
        ) as mock_service_cls:

            mock_service = Mock()
            mock_service_cls.return_value = (
                mock_service
            )

            mock_service.ingest_archive.return_value = []

            result = main.main()

    captured = capsys.readouterr()

    assert result == 0
    assert (
        "No valid traces discovered."
        in captured.out
    )


def test_main_returns_inventory(
    capsys,
):
    """
    Verify inventory entries are displayed when
    traces are discovered.
    """
    archive_path = "sample.zip"

    inventory = [
        {"path": "trace1.blf"},
        {"path": "trace2.pcap"},
    ]

    with patch(
        "sys.argv",
        ["main.py", archive_path],
    ):
        with patch(
            "main.ArchiveIngestionService"
        ) as mock_service_cls:

            mock_service = Mock()
            mock_service_cls.return_value = (
                mock_service
            )

            mock_service.ingest_archive.return_value = (
                inventory
            )

            result = main.main()

    captured = capsys.readouterr()

    assert result == 0
    assert (
        "Discovered 2 valid trace(s)"
        in captured.out
    )

    assert "trace1.blf" in captured.out
    assert "trace2.pcap" in captured.out


def test_main_passes_correct_arguments():
    """
    Verify archive and extraction paths are passed
    correctly to the ingestion service.
    """
    archive_path = "sample.zip"

    with patch(
        "sys.argv",
        ["main.py", archive_path],
    ):
        with patch(
            "main.ArchiveIngestionService"
        ) as mock_service_cls:

            mock_service = Mock()
            mock_service_cls.return_value = (
                mock_service
            )

            mock_service.ingest_archive.return_value = []

            main.main()

            mock_service.ingest_archive.assert_called_once_with(
                Path("sample.zip"),
                Path("sample_extracted"),
            )


def test_main_handles_exception(
    capsys,
):
    """
    Verify exceptions are caught and reported.
    """
    archive_path = "sample.zip"

    with patch(
        "sys.argv",
        ["main.py", archive_path],
    ):
        with patch(
            "main.ArchiveIngestionService"
        ) as mock_service_cls:

            mock_service = Mock()
            mock_service_cls.return_value = (
                mock_service
            )

            mock_service.ingest_archive.side_effect = (
                RuntimeError("boom")
            )

            result = main.main()

    captured = capsys.readouterr()

    assert result == 1
    assert "ERROR: boom" in captured.out