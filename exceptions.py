"""
Custom exceptions for EV Trace Unpacker.

All application-specific exceptions should inherit from
TraceUnpackerError.
"""


class TraceUnpackerError(Exception):
    """
    Base exception for the EV Trace Unpacker application.
    """


class ConfigurationError(TraceUnpackerError):
    """
    Raised when application configuration is invalid.
    """


class ArchiveDiscoveryError(TraceUnpackerError):
    """
    Raised when archive discovery fails.
    """


class ArchiveValidationError(TraceUnpackerError):
    """
    Raised when archive validation fails.
    """


class MultipartArchiveError(TraceUnpackerError):
    """
    Raised when multipart archive processing fails.
    """


class ArchiveMergeError(TraceUnpackerError):
    """
    Raised when archive merging fails.
    """


class ArchiveExtractionError(TraceUnpackerError):
    """
    Raised when archive extraction fails.
    """


class StagingError(TraceUnpackerError):
    """
    Raised when staging workspace operations fail.
    """


class TraceDiscoveryError(TraceUnpackerError):
    """
    Raised when trace-file discovery fails.
    """


class TraceClassificationError(TraceUnpackerError):
    """
    Raised when trace-file classification fails.
    """


class TracePublishingError(TraceUnpackerError):
    """
    Raised when publishing trace files fails.
    """


class CleanupError(TraceUnpackerError):
    """
    Raised when cleanup operations fail.
    """