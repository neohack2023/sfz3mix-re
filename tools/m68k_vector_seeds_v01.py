#!/usr/bin/env python3
"""Extract bounded Motorola 68000 reset/exception-vector seeds from original SFZ3 Mix CPU ROM.
This is not executable-code recovery or validated runtime control flow.
"""
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile
import argparse
EXPECTED="867b8356872a034ec7e06f776bf757ec2095fee7616931b71f720f30369806ab"
ap=argparse.ArgumentParser()
ap.add_argument("--archive",type=Path,required=True)
ap.add_argument("--report",type=Path,required=True)
args=ap.parse_args()
assert hashlib.sha256(args.archive.read_bytes()).hexdigest()==EXPECTED
with ZipFile(args.archive) as z:
    b=z.read("sz3mx.03")
raw=[int.from_bytes(b[i*4:i*4+4],"big") for i in range(64)]
entries=[]
for i,target in enumerate(raw):
    role="reset_stack_pointer" if i==0 else "reset_program_counter" if i==1 else "exception_vector"
    valid=(target % 2==0 and 0<=target<len(b))
    entries.append({"vector_index":i,"source_file_offset":4*i,
                    "target_hex":f"0x{target:08X}","role":role,
                    "possible_cpu_rom_code_address":valid if i!=0 else False,
                    "execution_verified":False})
candidates=sorted(set(raw[i] for i in range(1,64) if entries[i]["possible_cpu_rom_code_address"]))
record={
  "schema":"sfz3mix.m68k_vector_seeds.v01",
  "source_archive_sha256":EXPECTED,
  "program_sha256":hashlib.sha256(b).hexdigest(),
  "exception_vector_interpretation":"first 64 longwords (256 bytes) treated as M68000 vector candidates; validate against emulator reset/state",
  "reset_ssp":f"0x{raw[0]:08X}","reset_pc_candidate":f"0x{raw[1]:08X}",
  "candidate_in_range_even_targets":len(candidates),
  "candidate_targets_hex":[f"0x{v:06X}" for v in candidates],
  "confidence":"STRUCTURAL_CANDIDATE_ONLY",
  "vectors":entries}
if args.report.exists():raise FileExistsError(args.report)
args.report.write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"reset_ssp":record["reset_ssp"],"reset_pc_candidate":record["reset_pc_candidate"],
                  "candidate_targets":record["candidate_in_range_even_targets"],
                  "target_samples":record["candidate_targets_hex"][:20]},indent=2))
