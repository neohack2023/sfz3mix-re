#!/usr/bin/env python3
"""Source-corrected SFA3 CPS2 memory structure assessment for existing SFZ3 Mix v0.32 traces."""
from pathlib import Path
from hashlib import sha256
import json,re
ROOT=Path(r"D:\AIOS_SFZ3MIX_V032")
E=ROOT/"evidence"
files=sorted((int(match.group(1)),p) for p in E.glob("ram_*.bin")
             if (match:=re.fullmatch(r"ram_(\d+)\.bin",p.name)) and p.stat().st_size==65536)
if len(files)<5: raise RuntimeError("Insufficient sampled gameplay states")
snap={f:p.read_bytes() for f,p in files}
def u(raw,a,n=1): return int.from_bytes(raw[a:a+n],"big")
def hx(n,width=6):return f"0x{n:0{width}X}"
field_defs={"active_marker":(0,1),"status":(4,2),"flip":(0x0B,1),
 "pos_x":(0x10,2),"pos_y":(0x14,2),"animation_pointer":(0x1C,4),
 "box90":(0x90,4),"box94":(0x94,4),"box98":(0x98,4),
 "box9c":(0x9C,4),"boxa0":(0xA0,4),
 "id_c8":(0xC8,1),"id_c9":(0xC9,1),"id_ca":(0xCA,1),"id_cb":(0xCB,1)}
objects=[{"id":"sfa3_p"+str(i),"kind":"player","cpu_address":0xFF8400+i*0x400,"stride":0x400} for i in range(4)]
objects += [{"id":"sfa3_proj"+str(i),"kind":"projectile","cpu_address":0xFF9400+i*0x100,"stride":0x100} for i in range(4)]
samples=[];stats=[]
for obj in objects:
 base=obj["cpu_address"]-0xFF0000
 rows=[]
 for frame,raw in snap.items():
  fields={name:hx(u(raw,base+off,size),size*2) for name,(off,size) in field_defs.items()}
  nonzero=sum(b!=0 for b in raw[base:base+0x100])
  rows.append({"frame":frame,"nonzero_first_256":nonzero,"fields":fields})
 sample={"id":obj["id"],"kind":obj["kind"],"cpu_address":hx(obj["cpu_address"]),
         "historical_stride":hx(obj["stride"]),"states":rows}
 samples.append(sample)
 first_byte=[u(raw,base) for raw in snap.values()]
 ptrs=[u(raw,base+0x90,4) for raw in snap.values()]
 stats.append({"id":obj["id"],"nonzero_states":sum(r["nonzero_first_256"]>0 for r in rows),
 "active_marker_nonzero_frames":sum(v>0 for v in first_byte),
 "field_variations":{name:len(set(r["fields"][name] for r in rows))
                     for name in field_defs},
 "box90_nonzero_in_program_range":sum(0<v<6291456 and v%2==0 for v in ptrs),
 "nonzero_bytes_range":[min(r["nonzero_first_256"] for r in rows),
                         max(r["nonzero_first_256"] for r in rows)]})
objmap={s["id"]:s for s in stats}
confirm_player_base=(objmap["sfa3_p0"]["active_marker_nonzero_frames"]>=2 and
   objmap["sfa3_p0"]["box90_nonzero_in_program_range"]>=2 and
   objmap["sfa3_p0"]["field_variations"]["status"]>=2)
report={"schema":"sfz3mix.sfa3_ram_profile.v02",
"source":"https://github.com/Jesuszilla/mame-rr-scripts/blob/master/cps2-hitboxes.lua",
"source_sha":"3c4523278db5a0420d3920668a89103b00881697",
"source_notes":"Script defaults player_space to 0x400, object_space to 0x100; read player.base status if byte0 > 0.",
"runtime":"HBMAME :maincpu program RAM SFZ3 Mix v0.32 deterministic ram_trace.lua",
"scope":"static RAM checkpoints with automated coin/start/select and continue sequence",
"read_only":True,
"frames":list(snap),
"dump_sha256":{str(f):sha256(data).hexdigest() for f,data in snap.items()},
"layouts":[{"kind":"player","base":"0xFF8400","stride":"0x400","slots":4,
  "evidence_status":"OBSERVED_DYNAMIC_PLAYER_OBJECT_REGION" if confirm_player_base else "INSUFFICIENT"},
 {"kind":"projectile","base":"0xFF9400","stride":"0x100","slots":24,
  "evidence_status":"NOT_ACTIVELY_TESTED_NO_PROJECTILE_INPUT"}],
"field_assessments":[
 {"field":"status","offset":"0x04","status":"DYNAMIC_CORROBORATION" if confirm_player_base else "UNVERIFIED"},
 {"field":"animation_pointer","offset":"0x1C","status":"DYNAMIC_CORROBORATION" if confirm_player_base else "UNVERIFIED"},
 {"field":"box90","offset":"0x90","status":"PLAUSIBLE_ROM_POINTER_NOT_COLLISION_PROVEN"},
 {"field":"box94","offset":"0x94","status":"PLAUSIBLE_ROM_POINTER_NOT_COLLISION_PROVEN"},
 {"field":"box98","offset":"0x98","status":"PLAUSIBLE_ROM_POINTER_NOT_COLLISION_PROVEN"},
 {"field":"box9c","offset":"0x9C","status":"PLAUSIBLE_ROM_POINTER_NOT_COLLISION_PROVEN"},
 {"field":"boxa0","offset":"0xA0","status":"PLAUSIBLE_ROM_POINTER_NOT_COLLISION_PROVEN"},
 {"field":"id_c8_to_cb","offset":"0xC8","status":"CHANGES_OBSERVED_MEANING_NOT_RUNTIME_VERIFIED"},
 {"field":"screen_left","offset":"0xFF8290","status":"DYNAMIC_MEMORY_ONLY"}],
"objects_summary":stats,"objects_samples":samples,
"limitations":["No human-observed collision overlay synced to these frames.",
"Opponent/third/fourth player slot identities are not proven solely from RAM occupancy.",
"Projectile layout cannot be validated without projectile spawn and trace.",
"Even when a pointer lies inside program range, a decoded hitbox table has not been demonstrated.",
"Read-only samples cannot establish writer function, so no function_to_RAM xref is approved."]}
dest=E/"sfa3_ram_comparison_v02.json"
if dest.exists():raise FileExistsError(dest)
dest.write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps({"status":"PASS_ANALYSIS","frames":list(snap),
"layouts":report["layouts"],"objects_summary":stats,"file":str(dest)},indent=2))
