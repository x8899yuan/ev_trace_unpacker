import sys
from pathlib import Path

from services.archive_ingestion_service import (
    ArchiveIngestionService,
)


def main() -> int:
    """
    EV Trace Unpacker entry point.

    Usage:
        python main.py <archive_path>
    """

    if len(sys.argv) != 2:
        print(
            "Usage: python main.py <archive_path>"
        )
        return 1

    archive_path = Path(sys.argv[1])

    extraction_directory = (
        archive_path.parent
        / f"{archive_path.stem}_extracted"
    )

    try:
        ingestion_service = (
            ArchiveIngestionService()
        )

        inventory = (
            ingestion_service.ingest_archive(
                archive_path,
                extraction_directory,
            )
        )

        print()
        print("Trace Inventory")
        print("=" * 60)

        if not inventory:
            print("No valid traces discovered.")
            return 0

        print(
            f"Discovered {len(inventory)} valid trace(s)"
        )
        print()

        for trace in inventory:
            print(trace)

        return 0

    except Exception as exc:
        print(
            f"ERROR: {exc}"
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())