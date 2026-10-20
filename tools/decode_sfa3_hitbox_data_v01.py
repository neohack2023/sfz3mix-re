#!/usr/bin/env python3
"""Read-only static table decode of live RAM pointers using Jesuszilla's SFA3 hitbox record format."""
from pathlib import Path
import json,hashlib,re
R=Path(r"D:\AIOS_SFZ3MIX_V032"); E=R/"evidence"
program=(R/"tools/sz3mx.03").read_bytes()
expected="b5f7a1598e4f91a5113c506505b482b2cd1a19e366fe31471740e45dbd204691"
assert hashlib.sha256(program).hexdigest()==expected
frames=[3000,9300,10000,10300,10550,10640,10730,11000,13000,15000,16900]
box_types=[("vulnerability_1",0x90,0xC8,3),("vulnerability_2",0x94,0xC9,3),
           ("vulnerability_3",0x98,0xCA,3),("push",0x9C,0xCB,3)]
rows=[]
for frame in frames:
    ram=(E/f"ram_{frame:05d}.bin").read_bytes()
    assert len(ram)==65536
    for player in range(2):
        base=0x8400+player*0x400
        for typ,ptr_off,id_off,shift in box_types:
            ptr=int.from_bytes(ram[base+ptr_off:base+ptr_off+4],"big")
            ident=ram[base+id_off]
            addr=ptr+(ident<<shift)
            active=(ptr!=0 and ident>0)
            within=(active and addr>=0 and addr+8<=len(program))
            geo=None
            if within:
                val_x=int.from_bytes(program[addr:addr+2],"big",signed=True)
                val_y=int.from_bytes(program[addr+2:addr+4],"big",signed=True)
                rad_x=int.from_bytes(program[addr+4:addr+6],"big")
                rad_y=int.from_bytes(program[addr+6:addr+8],"big")
                geo={"val_x":val_x,"val_y":val_y,"rad_x":rad_x,"rad_y":rad_y,
                     "geometric_plausibility":bool(rad_x>0 and rad_x<512 and rad_y>0 and rad_y<512 and abs(val_x)<4096 and abs(val_y)<4096)}
            rows.append({"frame":frame,"player_slot":player,"box":typ,
                         "id":ident,"pointer":f"0x{ptr:06X}",
                         "entry_address":f"0x{addr:06X}" if active else None,
                         "active_id_and_pointer":active,"within_verified_program":bool(within),
                         "geometry":geo})
active=[x for x in rows if x["active_id_and_pointer"]]
decoded=[x for x in active if x["within_verified_program"]]
plaus=[x for x in decoded if x["geometry"]["geometric_plausibility"]]
result={"schema":"sfz3mix.sfa3_hitbox_data_decode.v01",
"source":"https://github.com/Jesuszilla/mame-rr-scripts/blob/master/cps2-hitboxes.lua",
"original_sfa3_rules":"pointer from 0x90/94/98/9C; selector from 0xC8/C9/CA/CB; table entry ptr + (id << 3); signed offsets x/y, unsigned radii x/y, big endian 16-bit",
"cpu_sha256":expected,
"frames":frames,
"attempted_rows":len(rows),"active_pointer_id_rows":len(active),
"within_program_rows":len(decoded),"plausible_dimension_rows":len(plaus),
"rows":rows,"limitations":["Read-only decode of original hacked CPU member. Pointer and dimension consistency is not proof of collision engine reads.",
                       "Graphics/animation control may use additional conditions, including invulnerability rules.",
                       "No ROM changes or RAM writes, and no 68000 instruction-to-field xref." ]}
dest=E/"sfa3_hitbox_pointer_decode_v01.json"
if dest.exists():raise FileExistsError(dest)
dest.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({k:result[k] for k in ["attempted_rows","active_pointer_id_rows","within_program_rows","plausible_dimension_rows"]}))
for row in plaus[:12]:
 print(row["frame"],row["player_slot"],row["box"],row["entry_address"],row["geometry"])
