from pathlib import Path

from traces.trace_validator import is_valid_trace


def test_valid_blf_file(tmp_path):
    trace_file = tmp_path / "vehicle.blf"
    trace_file.write_text("data")

    assert is_valid_trace(trace_file) is True


def test_valid_pcap_file(tmp_path):
    trace_file = tmp_path / "network.pcap"
    trace_file.write_text("data")

    assert is_valid_trace(trace_file) is True


def test_valid_dlt_file(tmp_path):
    trace_file = tmp_path / "diagnostics.dlt"
    trace_file.write_text("data")

    assert is_valid_trace(trace_file) is True


def test_missing_file_is_invalid():
    trace_file = Path("does_not_exist.blf")

    assert is_valid_trace(trace_file) is False


def test_unsupported_extension_is_invalid(tmp_path):
    trace_file = tmp_path / "notes.txt"
    trace_file.write_text("data")

    assert is_valid_trace(trace_file) is False


def test_empty_file_is_invalid(tmp_path):
    trace_file = tmp_path / "empty.blf"
    trace_file.touch()

    assert is_valid_trace(trace_file) is False


def test_directory_is_invalid(tmp_path):
    directory = tmp_path / "logs"
    directory.mkdir()

    assert is_valid_trace(directory) is False


def test_extension_check_is_case_insensitive(tmp_path):
    trace_file = tmp_path / "VEHICLE.BLF"
    trace_file.write_text("data")

    assert is_valid_trace(trace_file) is True