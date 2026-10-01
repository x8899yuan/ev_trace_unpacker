from pathlib import Path

import pytest

from traces.trace_discovery import discover_traces


def test_discover_blf_file(tmp_path):
    trace_file = tmp_path / "vehicle.blf"
    trace_file.write_text("test")

    traces = discover_traces(tmp_path)

    assert len(traces) == 1
    assert trace_file in traces


def test_discover_pcap_file(tmp_path):
    trace_file = tmp_path / "network.pcap"
    trace_file.write_text("test")

    traces = discover_traces(tmp_path)

    assert len(traces) == 1
    assert trace_file in traces


def test_discover_dlt_file(tmp_path):
    trace_file = tmp_path / "diagnostics.dlt"
    trace_file.write_text("test")

    traces = discover_traces(tmp_path)

    assert len(traces) == 1
    assert trace_file in traces


def test_ignore_unsupported_files(tmp_path):
    (tmp_path / "notes.txt").write_text("test")
    (tmp_path / "readme.md").write_text("test")
    (tmp_path / "config.json").write_text("test")

    traces = discover_traces(tmp_path)

    assert len(traces) == 0


def test_recursive_discovery(tmp_path):
    nested_directory = tmp_path / "logs" / "vehicle"
    nested_directory.mkdir(parents=True)

    trace_file = nested_directory / "vehicle.blf"
    trace_file.write_text("test")