from services.archive_processing_service import (
    ArchiveProcessingService,
)

def test_build_trace_inventory_empty_directory(
    tmp_path,
):
    service = ArchiveProcessingService()

    inventory = service.build_trace_inventory(
        tmp_path
    )

    assert inventory == []


def test_build_trace_inventory_returns_valid_blf(
    tmp_path,
):
    trace_file = tmp_path / "vehicle.blf"
    trace_file.write_text("data")

    service = ArchiveProcessingService()

    inventory = service.build_trace_inventory(
        tmp_path
    )

    assert len(inventory) == 1
    assert trace_file in inventory


def test_build_trace_inventory_returns_valid_pcap(
    tmp_path,
):
    trace_file = tmp_path / "network.pcap"
    trace_file.write_text("data")

    service = ArchiveProcessingService()

    inventory = service.build_trace_inventory(
        tmp_path
    )

    assert len(inventory) == 1
    assert trace_file in inventory


def test_build_trace_inventory_returns_valid_dlt(
    tmp_path,
):
    trace_file = tmp_path / "diagnostics.dlt"
    trace_file.write_text("data")

    service = ArchiveProcessingService()

    inventory = service.build_trace_inventory(
        tmp_path
    )

    assert len(inventory) == 1
    assert trace_file in inventory


def test_build_trace_inventory_filters_empty_trace(
    tmp_path,
):
    trace_file = tmp_path / "empty.blf"
    trace_file.touch()

    service = ArchiveProcessingService()

    inventory = service.build_trace_inventory(
        tmp_path
    )

    assert inventory == []


def test_build_trace_inventory_filters_unsupported_file(
    tmp_path,
):
    text_file = tmp_path / "notes.txt"
    text_file.write_text("data")

    service = ArchiveProcessingService()

    inventory = service.build_trace_inventory(
        tmp_path
    )

    assert inventory == []


def test_build_trace_inventory_recursive_discovery(
    tmp_path,
):
    nested_dir = (
        tmp_path
        / "logs"
        / "vehicle"
    )

    nested_dir.mkdir(parents=True)

    trace_file = (
        nested_dir
        / "vehicle.blf"
    )

    trace_file.write_text("data")

    service = ArchiveProcessingService()

    inventory = service.build_trace_inventory(
        tmp_path
    )

    assert len(inventory) == 1
    assert trace_file in inventory