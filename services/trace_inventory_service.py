from __future__ import annotations

from pathlib import Path
from typing import List

from traces.trace_inventory import build_trace_inventory


class TraceInventoryService:
    """
    Service responsible for building a validated
    trace inventory from an extracted directory.
    """

    def build(self, root_directory: Path) -> List[Path]:
        """
        Build a trace inventory.

          root_directory:
                Directory containing extracted trace files.

        Returns:
            List of validated trace file paths.
        """
        return build_trace_inventory(root_directory)