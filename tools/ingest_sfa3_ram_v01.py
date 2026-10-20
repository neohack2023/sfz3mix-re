#!/usr/bin/env python3
"""Non-destructive additive SQLite migration: documented SFA3 profile vs SFZ3 Mix v0.32 RAM."""
import argparse,json,sqlite3,hashlib,shutil
from pathlib import Path
def ingest(db, report):
    if not db.is_file(): raise FileNotFoundError(db)
    data=json.loads(report.read_text())
    if data.get("schema")!="sfz3mix.sfa3_ram_profile.v02":
        raise ValueError("Unexpected RAM comparison report schema")
    out=db.with_name(db.stem+"_before_ram_profile_v01"+db.suffix)
    if out.exists(): raise FileExistsError("Backup path already occupied; refusing double migration")
    con=sqlite3.connect(db)
    con.execute("PRAGMA foreign_keys=ON")
    try:
        if con.execute("SELECT value FROM metadata WHERE key='ram_profile_migration'").fetchone():
            raise ValueError("Already ingested")
        original_counts={name:con.execute("SELECT count(*) FROM "+name).fetchone()[0]
                         for name in ("functions","calls","evidence","function_issues")}
        # Backup through SQLite's consistent backup API, not a filesystem copy of a live DB.
        with sqlite3.connect(out) as backup:con.backup(backup)
        con.execute("""CREATE TABLE ram_structures(
          id TEXT PRIMARY KEY,base_address INTEGER NOT NULL,slot_stride INTEGER NOT NULL,
          source_slot_count INTEGER NOT NULL,status TEXT NOT NULL,source_url TEXT NOT NULL,
          receipt TEXT NOT NULL,notes TEXT NOT NULL)""")
        con.execute("""CREATE TABLE ram_slots(
          structure_id TEXT NOT NULL REFERENCES ram_structures(id),
          slot INTEGER NOT NULL,cpu_address INTEGER NOT NULL,
          observed_states INTEGER NOT NULL,active_marker_states INTEGER NOT NULL,
          status TEXT NOT NULL, PRIMARY KEY(structure_id,slot))""")
        con.execute("""CREATE TABLE ram_fields(
          structure_id TEXT NOT NULL REFERENCES ram_structures(id),
          field TEXT NOT NULL,offset INTEGER NOT NULL,
          semantics TEXT NOT NULL,status TEXT NOT NULL,source_url TEXT NOT NULL,
          PRIMARY KEY(structure_id,field))""")
        con.execute("""CREATE TABLE ram_observations(
          structure_id TEXT NOT NULL, slot INTEGER NOT NULL, frame INTEGER NOT NULL,
          nonzero_first_256 INTEGER NOT NULL, state_label TEXT NOT NULL,
          PRIMARY KEY(structure_id,slot,frame),
          FOREIGN KEY(structure_id,slot) REFERENCES ram_slots(structure_id,slot))""")
        con.execute("""CREATE TABLE ram_issue_links(
          structure_id TEXT NOT NULL REFERENCES ram_structures(id),
          issue_id TEXT NOT NULL REFERENCES issues(id),
          relationship TEXT NOT NULL, PRIMARY KEY(structure_id,issue_id))""")
        con.execute("""CREATE TABLE function_ram_xrefs(
          function_id TEXT NOT NULL REFERENCES functions(id),
          structure_id TEXT NOT NULL REFERENCES ram_structures(id),
          field TEXT NOT NULL, cpu_instruction_address INTEGER NOT NULL,
          kind TEXT NOT NULL, evidence_uri TEXT NOT NULL,confidence TEXT NOT NULL,
          PRIMARY KEY(function_id,structure_id,field,cpu_instruction_address,kind))""")
        source=data["source"]; receipt="Host 02 evidence/sfa3_ram_comparison_v02.json"
        for layout in data["layouts"]:
            sid="sfa3_"+layout["kind"]+"_pool"
            con.execute("INSERT INTO ram_structures VALUES (?,?,?,?,?,?,?,?)",
              (sid,int(layout["base"],16),int(layout["stride"],16),layout["slots"],
              layout["evidence_status"],source,receipt,
              "Observed under established v0.32 game input sequence; historical profile isn't proven causal collision logic"))
            con.execute("INSERT INTO ram_issue_links VALUES (?,?,?)",
              (sid,"hitboxes","candidate_for_collision_investigation_not_causal_proof"))
        object_summary={s["id"]:s for s in data["objects_summary"]}
        obj_samples={s["id"]:s for s in data["objects_samples"]}
        for kind in ("player","projectile"):
            sid="sfa3_"+kind+"_pool"
            n=4 if kind=="player" else 24
            base=0xFF8400 if kind=="player" else 0xFF9400
            stride=0x400 if kind=="player" else 0x100
            for i in range(n):
                key="sfa3_"+("p" if kind=="player" else "proj")+str(i)
                stat=object_summary.get(key)
                status=("RUNTIME_DYNAMIC_REGION_NOT_SEMANTICS_CONFIRMED"
                        if kind=="player" and i<2
                        else "NOT_ACTIVE_IN_SAMPLED_FRAMES" if stat
                        else "NOT_SAMPLED")
                con.execute("INSERT INTO ram_slots VALUES (?,?,?,?,?,?)",
                  (sid,i,base+i*stride,len(data["frames"]) if stat else 0,
                   stat["active_marker_nonzero_frames"] if stat else 0,status))
                if key in obj_samples:
                    for row in obj_samples[key]["states"]:
                        con.execute("INSERT INTO ram_observations VALUES (?,?,?,?,?)",
                            (sid,i,row["frame"],row["nonzero_first_256"],
                             "active_marker_nonzero" if int(row["fields"]["active_marker"],16)!=0 else "inactive_or_unproven"))
        field_offset={"status":0x04,"flip":0x0B,"pos_x":0x10,"pos_y":0x14,
                      "animation_pointer":0x1C,"box90":0x90,"box94":0x94,"box98":0x98,
                      "box9c":0x9C,"boxa0":0xA0,
                      "id_c8":0xC8,"id_c9":0xC9,"id_ca":0xCA,"id_cb":0xCB}
        meaning={"box90":"original vulnerability box address table 1",
                 "box94":"original vulnerability box address table 2",
                 "box98":"original vulnerability box address table 3",
                 "box9c":"original push/throwable address table",
                 "boxa0":"original attack address table"}
        for field,off in field_offset.items():
            status="RUNTIME_VALUE_VARIATION" if field in ["status","pos_x","pos_y","animation_pointer"] else "ORIGINAL_PROFILE_CANDIDATE_UNVERIFIED_SEMANTICS"
            con.execute("INSERT INTO ram_fields VALUES (?,?,?,?,?,?)",
              ("sfa3_player_pool",field,off,meaning.get(field,"original SFA3 candidate object field"),status,source))
        con.execute("INSERT INTO evidence VALUES (?,?,?,?,?)",
          ("ram-profile-v02","runtime_ram_checkpoint_comparison",receipt,
           "RUNTIME_OBSERVED_STRUCTURE_NOT_SEMANTICS_PROVEN",
           "11 frames, 0x400 player stride, 0x100 projectile stride; source-corrected profile"))
        con.execute("INSERT INTO metadata VALUES (?,?)",("ram_profile_migration","v01_2026-10-20"))
        for name,count in original_counts.items():
            assert con.execute("SELECT count(*) FROM "+name).fetchone()[0] == count+(1 if name=="evidence" else 0)
        assert con.execute("SELECT count(*) FROM function_ram_xrefs").fetchone()[0]==0
        assert con.execute("PRAGMA foreign_key_check").fetchall()==[]
        con.commit()
        assert con.execute("PRAGMA quick_check").fetchone()[0]=="ok"
        print(json.dumps({"status":"PASS","db":str(db),"backup":str(out),
              "original_tables_preserved":original_counts,
              "ram_structures":con.execute("SELECT count(*) FROM ram_structures").fetchone()[0],
              "ram_slots":con.execute("SELECT count(*) FROM ram_slots").fetchone()[0],
              "ram_fields":con.execute("SELECT count(*) FROM ram_fields").fetchone()[0],
              "ram_observations":con.execute("SELECT count(*) FROM ram_observations").fetchone()[0],
              "issue_links":con.execute("SELECT count(*) FROM ram_issue_links").fetchone()[0],
              "verified_function_xrefs":con.execute("SELECT count(*) FROM function_ram_xrefs").fetchone()[0],
              "foreign_keys":"PASS","integrity":"PASS"},indent=2))
    except Exception:
        con.rollback()
        raise
    finally: con.close()
def main():
    a=argparse.ArgumentParser()
    a.add_argument("--database",type=Path,required=True)
    a.add_argument("--report",type=Path,required=True)
    v=a.parse_args();ingest(v.database,v.report)
if __name__=="__main__":main()
