#!/usr/bin/env python3
"""Compare a program-space probe TSV against the original ROM CPU member, without asserting code fetch mapping."""
import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile
ORIGINAL="867b8356872a034ec7e06f776bf757ec2095fee7616931b71f720f30369806ab"
p=argparse.ArgumentParser()
p.add_argument("--archive",type=Path,required=True)
p.add_argument("--probe",type=Path,required=True)
p.add_argument("--report",type=Path,required=True)
a=p.parse_args()
assert hashlib.sha256(a.archive.read_bytes()).hexdigest()==ORIGINAL
with ZipFile(a.archive) as z: rom=z.read("sz3mx.03")
result=[]
for line in a.probe.read_text(encoding="utf-8").splitlines()[1:]:
 addr_str,raw=line.split("\t",1)
 addr=int(addr_str,16)
 if raw.startswith("ERROR:"):
  result.append({"cpu_address":addr_str,"error":raw});continue
 b=bytes.fromhex(raw)
 same=rom[addr:addr+len(b)]==b
 occurrences=[]
 start=0
 for _ in range(4):
  loc=rom.find(b,start)
  if loc<0:break
  occurrences.append(loc);start=loc+1
 result.append({"cpu_address":addr_str,"sample_size":len(b),
                "file_same_offset_match":same,"occurrences_first_four":occurrences,
                "within_raw_rom":addr+len(b)<=len(rom)})
report={"schema":"sfz3mix.program_mapping.v02","source_archive_sha256":ORIGINAL,
        "method":"HBMAME CPU program data-space read_u8 snapshot vs raw sz3mx.03 file",
        "caveat":"Only sampled data reads; opcode fetch/decryption and unmapped banking unverified",
        "samples":result,"matches":sum(x.get("file_same_offset_match",False) for x in result),
        "total":len(result)}
if a.report.exists():raise FileExistsError(str(a.report))
a.report.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"matches":report["matches"],"total":report["total"],
                  "mismatches":[x for x in result if not x.get("file_same_offset_match")]},indent=2))
