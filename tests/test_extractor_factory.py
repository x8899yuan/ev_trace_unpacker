from pathlib import Path

import pytest

from archives.extractor_factory import ExtractorFactory
from archives.extractors.seven_zip_extractor import SevenZipExtractor
from archives.extractors.zip_extractor import ZipExtractor


def test_returns_zip_extractor():
    extractor = ExtractorFactory.get_extractor(
        Path("trace.zip")
    )

    assert isinstance(
        extractor,
        ZipExtractor
    )


def test_returns_seven_zip_extractor():
    extractor = ExtractorFactory.get_extractor(
        Path("trace.7z")
    )

    assert isinstance(
        extractor,
        SevenZipExtractor
    )


def test_unsupported_extension_raises():
    with pytest.raises(ValueError):
        ExtractorFactory.get_extractor(
            Path("trace.rar")
        )


def test_case_insensitive_zip():
    extractor = ExtractorFactory.get_extractor(
        Path("TRACE.ZIP")
    )

    assert isinstance(
        extractor,
        ZipExtractor
    )


def test_case_insensitive_seven_zip():
    extractor = ExtractorFactory.get_extractor(
        Path("TRACE.7Z")
    )

    assert isinstance(
        extractor,
        SevenZipExtractor
    )