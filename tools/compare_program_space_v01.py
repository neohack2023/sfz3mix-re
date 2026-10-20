#!/usr/bin/env python3
"""Compare HBMAME CPU data-space read snapshots to raw v0.32 CPU ROM member."""
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

root = Path(r"D:\AIOS_SFZ3MIX_V032")
archive = root / "downloads" / "sfz3mix_v032_original.zip"
probe = root / "evidence" / "program_space_probe_v01.tsv"
target = root / "evidence" / "program_space_mapping_v01.json"
expected = "867b8356872a034ec7e06f776bf757ec2095fee7616931b71f720f30369806ab"
assert hashlib.sha256(archive.read_bytes()).hexdigest() == expected
with ZipFile(archive) as z:
    program = z.read("sz3mx.03")
results = []
for line in probe.read_text(encoding="utf-8").splitlines()[1:]:
    addr_hex, value = line.split("\t", 1)
    addr = int(addr_hex, 16)
    if value.startswith("ERROR:"):
        results.append({"cpu_address": addr_hex, "error": value})
        continue
    b = bytes.fromhex(value)
    same_offset = program[addr:addr + len(b)] == b
    hits = []
    start = 0
    for _ in range(6):
        hit = program.find(b, start)
        if hit < 0:
            break
        hits.append(hit)
        start = hit + 1
    results.append({"cpu_address": addr_hex, "sample_length": len(b),
                    "raw_rom_same_offset_matches": same_offset,
                    "raw_rom_occurrences_first_6": hits})
record = {"schema": "sfz3mix.program_data_space_mapping.v01",
          "source_archive_sha256": expected,
          "method": "read_u8(:maincpu program space) snapshot vs original sz3mx.03 bytes",
          "limitation": "Sampled data-space bytes only; does not prove CPU opcode decrypt/fetch path or all address ranges",
          "comparisons": results,
          "same_offset_matches": sum(bool(r.get("raw_rom_same_offset_matches")) for r in results),
          "sample_count": len(results)}
assert not target.exists()
target.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
print(json.dumps(record, indent=2))
