from pathlib import Path

from traces.trace_inventory import build_trace_inventory


def test_inventory_returns_valid_blf_file(tmp_path):
    trace_file = tmp_path / "vehicle.blf"
    trace_file.write_text("data")

    inventory = build_trace_inventory(tmp_path)

    assert len(inventory) == 1
    assert trace_file in inventory


def test_inventory_returns_valid_pcap_file(tmp_path):
    trace_file = tmp_path / "network.pcap"
    trace_file.write_text("data")

    inventory = build_trace_inventory(tmp_path)

    assert len(inventory) == 1
    assert trace_file in inventory


def test_inventory_returns_valid_dlt_file(tmp_path):
    trace_file = tmp_path / "diagnostics.dlt"
    trace_file.write_text("data")

    inventory = build_trace_inventory(tmp_path)

    assert len(inventory) == 1
    assert trace_file in inventory


def test_inventory_filters_unsupported_files(tmp_path):
    unsupported_file = tmp_path / "notes.txt"
    unsupported_file.write_text("data")

    inventory = build_trace_inventory(tmp_path)

    assert inventory == []


def test_inventory_filters_empty_trace_files(tmp_path):
    empty_trace = tmp_path / "empty.blf"
    empty_trace.touch()

    inventory = build_trace_inventory(tmp_path)

    assert inventory == []


def test_inventory_recursive_discovery(tmp_path):
    nested_dir = tmp_path / "logs" / "vehicle"
    nested_dir.mkdir(parents=True)

    trace_file = nested_dir / "vehicle.blf"
    trace_file.write_text("data")

    inventory = build_trace_inventory(tmp_path)

    assert len(inventory) == 1
    assert trace_file in inventory


def test_inventory_multiple_trace_types(tmp_path):
    blf_file = tmp_path / "vehicle.blf"
    pcap_file = tmp_path / "network.pcap"
    dlt_file = tmp_path / "diagnostics.dlt"

    blf_file.write_text("data")
    pcap_file.write_text("data")
    dlt_file.write_text("data")

    inventory = build_trace_inventory(tmp_path)

    assert len(inventory) == 3
    assert blf_file in inventory
    assert pcap_file in inventory
    assert dlt_file in inventory


def test_inventory_empty_when_no_traces_exist(tmp_path):
    inventory = build_trace_inventory(tmp_path)

    assert inventory == []