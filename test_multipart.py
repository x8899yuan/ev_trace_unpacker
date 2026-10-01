from pathlib import Path
import tempfile
import shutil
import py7zr

parts = [
    Path("archives/VW316660436_BEUS_20251022_083710h_10242km_Trace.blf.7z.001"),
    Path("archives/VW316660436_BEUS_20251022_083710h_10242km_Trace.blf.7z.002"),
    Path("archives/VW316660436_BEUS_20251022_083710h_10242km_Trace.blf.7z.003"),
    Path("archives/VW316660436_BEUS_20251022_083710h_10242km_Trace.blf.7z.004"),
]

with tempfile.NamedTemporaryFile(
    suffix=".7z",
    delete=False
) as tmp:

    tmp_path = Path(tmp.name)

    for part in parts:
        with open(part, "rb") as src:
            shutil.copyfileobj(src, tmp)

print(f"Combined archive: {tmp_path}")

with py7zr.SevenZipFile(tmp_path, "r") as archive:
    archive.extractall("temp_extract")