from pathlib import Path
from unittest.mock import Mock, patch

from services.archive_ingestion_service import (
    ArchiveIngestionService,
)


def test_ingest_archive_returns_inventory():
    """
    Verify the inventory produced by the processing
    service is returned to the caller.
    """
    archive_path = Path("sample.zip")
    extraction_directory = Path("extracted")

    expected_inventory = [
        {"path": "trace1.blf"},
        {"path": "trace2.pcap"},
    ]

    with patch(
        "services.archive_ingestion_service.ArchiveExtractionService"
    ) as mock_extraction_cls, patch(
        "services.archive_ingestion_service.ArchiveProcessingService"
    ) as mock_processing_cls:

        mock_extraction_service = Mock()
        mock_processing_service = Mock()

        mock_extraction_cls.return_value = (
            mock_extraction_service
        )
        mock_processing_cls.return_value = (
            mock_processing_service
        )

        mock_processing_service.build_trace_inventory.return_value = (
            expected_inventory
        )

        service = ArchiveIngestionService()

        result = service.ingest_archive(
            archive_path,
            extraction_directory,
        )

        assert result == expected_inventory


def test_ingest_archive_calls_extraction_service():
    """
    Verify archive extraction is invoked with the
    correct arguments.
    """
    archive_path = Path("sample.zip")
    extraction_directory = Path("extracted")

    with patch(
        "services.archive_ingestion_service.ArchiveExtractionService"
    ) as mock_extraction_cls, patch(
        "services.archive_ingestion_service.ArchiveProcessingService"
    ):

        mock_extraction_service = Mock()
        mock_extraction_cls.return_value = (
            mock_extraction_service
        )

        service = ArchiveIngestionService()

        service.ingest_archive(
            archive_path,
            extraction_directory,
        )

        mock_extraction_service.extract_archive.assert_called_once_with(
            archive_path,
            extraction_directory,
        )


def test_ingest_archive_calls_processing_service():
    """
    Verify trace inventory processing is invoked with
    the extraction directory.
    """
    archive_path = Path("sample.zip")
    extraction_directory = Path("extracted")

    with patch(
        "services.archive_ingestion_service.ArchiveExtractionService"
    ), patch(
        "services.archive_ingestion_service.ArchiveProcessingService"
    ) as mock_processing_cls:

        mock_processing_service = Mock()
        mock_processing_cls.return_value = (
            mock_processing_service
        )

        service = ArchiveIngestionService()

        service.ingest_archive(
            archive_path,
            extraction_directory,
        )

        mock_processing_service.build_trace_inventory.assert_called_once_with(
            extraction_directory,
        )


def test_ingest_archive_extracts_before_processing():
    """
    Verify extraction occurs before inventory
    processing.
    """
    archive_path = Path("sample.zip")
    extraction_directory = Path("extracted")

    call_order = []

    with patch(
        "services.archive_ingestion_service.ArchiveExtractionService"
    ) as mock_extraction_cls, patch(
        "services.archive_ingestion_service.ArchiveProcessingService"
    ) as mock_processing_cls:

        mock_extraction_service = Mock()
        mock_processing_service = Mock()

        mock_extraction_cls.return_value = (
            mock_extraction_service
        )
        mock_processing_cls.return_value = (
            mock_processing_service
        )

        def extraction_side_effect(*args, **kwargs):
            call_order.append("extract")

        def processing_side_effect(*args, **kwargs):
            call_order.append("process")
            return []

        mock_extraction_service.extract_archive.side_effect = (
            extraction_side_effect
        )

        mock_processing_service.build_trace_inventory.side_effect = (
            processing_side_effect
        )

        service = ArchiveIngestionService()

        service.ingest_archive(
            archive_path,
            extraction_directory,
        )

        assert call_order == [
            "extract",
            "process",
        ]