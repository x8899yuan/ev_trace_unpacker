from pathlib import Path

from services.trace_inventory_service import TraceInventoryService


def test_service_returns_valid_blf_file(tmp_path):
    trace_file = tmp_path / "vehicle.blf"
    trace_file.write_text("data")

    service = TraceInventoryService()
    inventory = service.build(tmp_path)

    assert len(inventory) == 1
    assert trace_file in inventory


def test_service_returns_valid_pcap_file(tmp_path):
    trace_file = tmp_path / "network.pcap"
    trace_file.write_text("data")

    service = TraceInventoryService()
    inventory = service.build(tmp_path)

    assert len(inventory) == 1
    assert trace_file in inventory


def test_service_returns_valid_dlt_file(tmp_path):
    trace_file = tmp_path / "diagnostics.dlt"
    trace_file.write_text("data")

    service = TraceInventoryService()
    inventory = service.build(tmp_path)

    assert len(inventory) == 1
    assert trace_file in inventory


def test_service_filters_empty_trace_files(tmp_path):
    trace_file = tmp_path / "empty.blf"
    trace_file.touch()

    service = TraceInventoryService()
    inventory = service.build(tmp_path)

    assert inventory == []


def test_service_filters_unsupported_files(tmp_path):
    unsupported_file = tmp_path / "notes.txt"
    unsupported_file.write_text("data")

    service = TraceInventoryService()
    inventory = service.build(tmp_path)

    assert inventory == []


def test_service_recursive_discovery(tmp_path):
    nested_dir = tmp_path / "logs" / "vehicle"
    nested_dir.mkdir(parents=True)

    trace_file = nested_dir / "vehicle.blf"
    trace_file.write_text("data")

    service = TraceInventoryService()
    inventory = service.build(tmp_path)

    assert len(inventory) == 1
    assert trace_file in inventory


def test_service_multiple_trace_types(tmp_path):
    blf_file = tmp_path / "vehicle.blf"
    pcap_file = tmp_path / "network.pcap"
    dlt_file = tmp_path / "diagnostics.dlt"

    blf_file.write_text("data")
    pcap_file.write_text("data")
    dlt_file.write_text("data")

    service = TraceInventoryService()
    inventory = service.build(tmp_path)

    assert len(inventory) == 3
    assert blf_file in inventory
    assert pcap_file in inventory
    assert dlt_file in inventory


def test_service_empty_inventory(tmp_path):
    service = TraceInventoryService()

    inventory = service.build(tmp_path)

    assert inventory == []