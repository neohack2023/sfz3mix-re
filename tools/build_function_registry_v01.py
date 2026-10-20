#!/usr/bin/env python3
"""Promote only sanitized, explicitly unverified M68K entrypoint candidates from local CFG."""
import json
from pathlib import Path
root=Path(r"D:\AIOS_SFZ3MIX_V032")
src=root/"evidence/m68k_cfg_v02.json"
dst=root/"evidence/function_registry_sanitized_v01.json"
if dst.exists():raise FileExistsError(dst)
raw=json.loads(src.read_text(encoding="utf-8"))
entries=[]
for i,x in enumerate(raw["function_entry_candidates"],1):
  addr=x["entry"]
  associated=[]
  if addr=="00331C":associated=["continue-counter: investigative lead only"]
  if addr in ["025C40","025CC0"]:associated=["continue-counter: investigative lead only"]
  if addr=="026438":associated=["continue-screen sprite artifact: investigative lead only"]
  entries.append({"id":f"FUNC_CAND_{i:04d}","cpu_address":"0x"+addr,
                  "source":x["reason"],"status":"UNVERIFIED_STATIC_ENTRY_CANDIDATE",
                  "linked_community_todos":associated,
                  "runtime_confirmed":False,"function_bounds_confirmed":False})
out={"schema":"sfz3mix.function_registry.v01","cpu_program_sha256":raw["cpu_sha256"],
     "source_archive_sha256":raw["source_archive_sha256"],
     "derived_from":"Host 02 m68k_cfg_v02.json",
     "disclaimer":"Entrypoint candidates only: no verified function meanings, boundaries, or instruction-fetch parity",
     "summary":raw["summary"],"entries":entries}
dst.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"count":len(entries),"filename":str(dst),"status":"WRITTEN"}))
