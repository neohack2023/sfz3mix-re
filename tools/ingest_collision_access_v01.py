"""Add validated CPU-originated access observations; never infer function ownership."""
import csv,hashlib,json,re,sqlite3
from pathlib import Path
ROOT=Path(r"D:\AIOS_SFZ3MIX_V032")
def bus_bytes(addr,mask):
    assert mask in (0xffff,0xff00,0x00ff), hex(mask)
    return [addr+i for i,m in ((0,0xff00),(1,0x00ff)) if mask&m]
def main():
    assert bus_bytes(0xff84ca,0x00ff)==[0xff84cb]
    assert bus_bytes(0xff849c,0xffff)==[0xff849c,0xff849d]
    assert bus_bytes(0xff84c8,0xff00)==[0xff84c8]
    trace=ROOT/"evidence/collision_access_v01.tsv"
    validation=json.loads((ROOT/"evidence/collision_access_validation_v01.json").read_text())
    assert validation["status"]=="PASS"
    assert validation["trace_sha256"]==hashlib.sha256(trace.read_bytes()).hexdigest()
    assert all(x["opcode_file_match"] and x["ir_match"] for x in validation["sites"])
    assert hashlib.sha256((ROOT/"tools/sz3mx.03").read_bytes()).hexdigest()=="b5f7a1598e4f91a5113c506505b482b2cd1a19e366fe31471740e45dbd204691"
    rows=list(csv.DictReader([l for l in trace.read_text().splitlines() if not l.startswith("#")],delimiter="\t"))
    assert len(rows)==validation["events"]==50 and "# COMPLETE" in trace.read_text()
    db=ROOT/"evidence/functions_v01.sqlite"
    backup=db.with_name("functions_v01_before_collision_access_v01.sqlite")
    assert not backup.exists(), "Migration already prepared: inspect receipt rather than replay"
    con=sqlite3.connect(db);con.execute("pragma foreign_keys=on")
    preserved={t:con.execute("select * from "+t).fetchall() for t in ("functions","calls","function_ram_xrefs","ram_fields","ram_box_decodes")}
    with sqlite3.connect(backup) as target: con.backup(target)
    try:
        con.execute("BEGIN IMMEDIATE")
        con.execute("""CREATE TABLE runtime_collision_instructions(
          cpu_pc INTEGER PRIMARY KEY,instruction TEXT NOT NULL,
          function_id TEXT REFERENCES functions(id), opcode_mapping_status TEXT NOT NULL,
          evidence_id TEXT NOT NULL REFERENCES evidence(id))""")
        con.execute("""CREATE TABLE runtime_collision_accesses(
          id INTEGER PRIMARY KEY, cpu_pc INTEGER NOT NULL REFERENCES runtime_collision_instructions(cpu_pc),
          frame INTEGER NOT NULL,kind TEXT NOT NULL CHECK(kind IN ('READ','WRITE')),
          bus_address INTEGER NOT NULL,bus_data INTEGER NOT NULL,bus_mask INTEGER NOT NULL,
          bus_width_bits INTEGER NOT NULL CHECK(bus_width_bits=16),
          pc_register_during_access INTEGER NOT NULL,
          structure_id TEXT NOT NULL,slot INTEGER NOT NULL,state_label TEXT NOT NULL,
          snapshot_json TEXT NOT NULL,evidence_id TEXT NOT NULL REFERENCES evidence(id),
          FOREIGN KEY(structure_id,slot) REFERENCES ram_slots(structure_id,slot))""")
        con.execute("""CREATE TABLE runtime_collision_access_fields(
          access_id INTEGER NOT NULL REFERENCES runtime_collision_accesses(id),
          structure_id TEXT NOT NULL,field TEXT NOT NULL,
          PRIMARY KEY(access_id,structure_id,field),
          FOREIGN KEY(structure_id,field) REFERENCES ram_fields(structure_id,field))""")
        con.execute("""CREATE TABLE runtime_collision_issue_links(
          cpu_pc INTEGER NOT NULL REFERENCES runtime_collision_instructions(cpu_pc),
          issue_id TEXT NOT NULL REFERENCES issues(id),relationship TEXT NOT NULL,
          PRIMARY KEY(cpu_pc,issue_id))""")
        eid="collision-access-v01"
        con.execute("INSERT INTO evidence VALUES (?,?,?,?,?)",(eid,"cpu_memory_access_trace",str(trace),
          "EMULATOR_RUNTIME_PROVEN_INSTRUCTION_ACCESS_NOT_FUNCTION_OWNERSHIP",
          "HBMAME 0.289.3; CURPC, IR and debugger disassembly; exact instruction opcode-file matches at nine sites; 50 distinct samples, not total hit counts; 2940..3060-frame window; nil-return taps, guarded observer reads."))
        for site in validation["sites"]:
            pc=int(site["pc"],16)
            con.execute("INSERT INTO runtime_collision_instructions VALUES (?,?,?,?,?)",
              (pc,site["instruction"],None,"EXACT_OBSERVED_INSTRUCTION_OPCODE_FILE_MATCH",eid))
            con.execute("INSERT INTO runtime_collision_issue_links VALUES (?,?,?)",
              (pc,"hitboxes","verified_player_field_access_investigation_not_fix_or_causal_proof"))
        offsets=con.execute("select field,offset from ram_fields where structure_id='sfa3_player_pool'").fetchall()
        for seq,row in enumerate(rows,1):
            slot=int(row["player"])-1;base=0xff8400+slot*0x400
            addr=int(row["address"],16);mask=int(row["bus_mask"],16)
            accessed=bus_bytes(addr,mask)
            fields=[name for name,off in offsets if any(base+off<=a<base+off+(4 if name.startswith("box") else 1) for a in accessed)]
            assert fields,(row,accessed)
            con.execute("INSERT INTO runtime_collision_accesses VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
              (seq,int(row["curpc"],16),int(row["frame"]),row["access"],addr,int(row["bus_data"],16),mask,16,int(row["pc_register"],16),
               "sfa3_player_pool",slot,row["phase"],json.dumps(row,sort_keys=True),eid))
            for field in fields:con.execute("INSERT INTO runtime_collision_access_fields VALUES (?,?,?)",(seq,"sfa3_player_pool",field))
        for t,values in preserved.items():assert con.execute("select * from "+t).fetchall()==values,t
        assert con.execute("pragma integrity_check").fetchall()==[("ok",)]
        assert con.execute("pragma foreign_key_check").fetchall()==[]
        con.commit()
        assert con.execute("pragma integrity_check").fetchall()==[("ok",)]
        assert con.execute("pragma foreign_key_check").fetchall()==[]
        result={"status":"PASS","observations":len(rows),"read_samples":sum(x["access"]=="READ" for x in rows),
          "instruction_sites":len(validation["sites"]),"verified_function_owners":0,
          "field_links":con.execute("select count(*) from runtime_collision_access_fields").fetchone()[0],
          "functions_preserved":len(preserved["functions"]),"calls_preserved":len(preserved["calls"]),
          "function_ram_xrefs":len(preserved["function_ram_xrefs"]),"integrity":"ok","foreign_keys":"PASS","backup":str(backup),
          "trace_sha256":validation["trace_sha256"]}
        (ROOT/"evidence/collision_access_db_receipt_v01.json").write_text(json.dumps(result,indent=2))
        print(json.dumps(result))
    except Exception:
        con.rollback();raise
    finally:con.close()
if __name__=="__main__":main()
