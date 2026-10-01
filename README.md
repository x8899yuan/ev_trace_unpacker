# ev_trace_unpacker

## Overview

ev_trace_unpacker is a trace-ingestion and archive-processing tool designed
to discover and inventory automotive trace files contained within
compressed archive packages.

The project supports extraction, validation, and inventory generation
without performing trace decoding.

---

## Supported Archive Types

- ZIP
- 7Z
- Multipart 7Z (.7z.001, .7z.002, .7z.003...)

---

## Supported Trace Types

- BLF
- PCAP
- DLT

---

## Supported Archive Workflows

### Standard Archive

archive.zip
    -> trace.blf

### Nested Archive

archive.7z
    -> archive.zip
        -> trace.blf

### Multipart Archive

archive.7z.001
archive.7z.002
archive.7z.003
    -> archive.zip
        -> trace.blf

---

## Features

- Archive discovery
- Archive validation
- ZIP extraction
- 7Z extraction
- Multipart 7Z reconstruction
- Nested archive extraction
- Trace discovery
- Trace validation
- Trace inventory generation

---

## Example

python main.py archive.7z.001

Output:

Trace Inventory
============================================================
Discovered 1 valid trace(s)

trace.blf

---

## Architecture

archives/
extractors/
models/
services/
traces/
validators/
tests/

---

## Validation Status

Version: 1.0

Validated Against:

- Synthetic test archives
- Unit tests
- Integration tests
- Real VW multipart archive packages

Test Results:

90 passed
0 failed

---

## Future Roadmap

### Phase 2

Trace Metadata Extraction

- BLF metadata
- PCAP metadata
- DLT metadata

### Phase 3

Inventory Export

- CSV
- JSON
- Excel

### Phase 4

Batch Processing

- Multiple archives
- Summary reports
- Batch inventory generation