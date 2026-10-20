#!/usr/bin/env python3
"""Safely attach tested (pointer,id)->8-byte box record decodes to existing RAM SQLite registry."""
import argparse,sqlite3,json
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument("--database",required=True,type=Path)
p.add_argument("--report",required=True,type=Path)
a=p.parse_args()
r=json.loads(a.report.read_text())
if r.get("schema")!="sfz3mix.sfa3_hitbox_data_decode.v01":raise ValueError("Unexpected report schema")
db=sqlite3.connect(a.database);db.execute("PRAGMA foreign_keys=ON")
try:
    if db.execute("SELECT 1 FROM metadata WHERE key='hitbox_decode_v01'").fetchone():
        raise ValueError("Decode evidence already registered")
    assert db.execute("SELECT count(*) FROM ram_structures").fetchone()[0]==2
    assert db.execute("SELECT count(*) FROM functions").fetchone()[0]==59
    assert db.execute("SELECT count(*) FROM calls").fetchone()[0]==76
    # Exact composite slot foreign key is used so no hidden cross-pool player/projectile confusion.
    db.execute("""CREATE TABLE ram_box_decodes(
       frame INTEGER NOT NULL, structure_id TEXT NOT NULL,
       player_slot INTEGER NOT NULL,box_type TEXT NOT NULL,
       selector INTEGER NOT NULL,table_address INTEGER NOT NULL,entry_address INTEGER NOT NULL,
       offset_x INTEGER NOT NULL,offset_y INTEGER NOT NULL,
       radius_x INTEGER NOT NULL,radius_y INTEGER NOT NULL,
       evidence_id TEXT NOT NULL REFERENCES evidence(id),
       PRIMARY KEY(frame,structure_id,player_slot,box_type),
       FOREIGN KEY(structure_id,player_slot) REFERENCES ram_slots(structure_id,slot))""")
    db.execute("CREATE INDEX idx_ram_box_entry ON ram_box_decodes(entry_address)")
    receipt="Host 02 evidence/sfa3_hitbox_pointer_decode_v01.json"
    db.execute("INSERT INTO evidence VALUES (?,?,?,?,?)",
       ("ram-box-decode-v01","runtime_ram_pointer_rom_table_decode",receipt,
       "RUNTIME_POINTER_ROM_RECORD_CORROBORATED",
       "20/20 active historical SFA3 vulnerability/push box pointers resolve to in-range v0.32 program records with plausible dimensions; not proof of CPU collision reads"))
    count=0
    for row in r["rows"]:
        if not row["active_id_and_pointer"] or not row["within_verified_program"]:
            continue
        if not row["geometry"]["geometric_plausibility"]:
            continue
        g=row["geometry"]
        ptr=int(row["pointer"],16); entry=int(row["entry_address"],16)
        db.execute("""INSERT INTO ram_box_decodes
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
           (row["frame"],"sfa3_player_pool",row["player_slot"],
            row["box"],row["id"],ptr,entry,
            g["val_x"],g["val_y"],g["rad_x"],g["rad_y"],"ram-box-decode-v01"))
        count+=1
    assert count==20,(count,len(r["rows"]))
    db.execute("INSERT INTO metadata VALUES (?,?)",("hitbox_decode_v01","verified_20_active_data_table_samples"))
    assert db.execute("SELECT count(*) FROM function_ram_xrefs").fetchone()[0]==0
    assert db.execute("PRAGMA foreign_key_check").fetchall()==[]
    db.commit()
    assert db.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
    print(json.dumps({"status":"PASS","decoded_data_records":count,
          "distinct_entries":db.execute("SELECT count(DISTINCT entry_address) FROM ram_box_decodes").fetchone()[0],
          "function_links":0,"db":str(a.database),"integrity":"PASS"},indent=2))
except Exception:
    db.rollback();raise
finally:db.close()
