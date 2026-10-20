"""Transactional additive migration for a validated collision callable region."""
import csv,hashlib,json,sqlite3
from pathlib import Path
ROOT=Path(r"D:\AIOS_SFZ3MIX_V032")
def main():
    report=ROOT/"evidence/collision_reconstruction_v01.json"
    r=json.loads(report.read_text());fid=r["function_id"];entry=r["cpu_entry"];end=r["cpu_end_exclusive"]
    assert r["parity"]["decision"]=="PASS" and r["runtime_access_rows"]==44
    trace=ROOT/"evidence/collision_recovery_v02.tsv"
    assert hashlib.sha256(trace.read_bytes()).hexdigest()==r["evidence"]["operand_trace_sha256"]
    assert hashlib.sha256((ROOT/"tools/sz3mx.03").read_bytes()).hexdigest()==r["source_rom_sha256"]
    rows=list(csv.DictReader([l for l in trace.read_text().splitlines() if not l.startswith("#")],delimiter="\t"))
    assert len(rows)==44
    db=ROOT/"evidence/functions_v01.sqlite"
    backup=ROOT/"evidence/functions_v01_before_collision_reconstruction_v01.sqlite"
    assert not backup.exists(),"Inspect existing migration; do not replay"
    c=sqlite3.connect(db);c.execute("pragma foreign_keys=on")
    original_functions=c.execute("select * from functions").fetchall()
    original_calls=c.execute("select * from calls").fetchall()
    original_boxes=c.execute("select * from ram_box_decodes").fetchall()
    assert c.execute("pragma integrity_check").fetchall()==[("ok",)] and not c.execute("pragma foreign_key_check").fetchall()
    assert not c.execute("select 1 from functions where cpu_address=?",(entry,)).fetchone(),"Existing identity must be reconciled before migration"
    with sqlite3.connect(backup) as b:c.backup(b)
    try:
        c.execute("begin immediate")
        c.execute("""create table function_basic_blocks(
          id text primary key,function_id text not null references functions(id),
          start_address integer not null,end_exclusive integer not null,evidence_id text not null references evidence(id))""")
        c.execute("""create table function_instructions(
          function_id text not null references functions(id),cpu_pc integer not null,
          block_id text not null references function_basic_blocks(id),size_bytes integer not null,instruction text not null,
          runtime_visited integer not null,opcode_mapping_status text not null,evidence_id text not null references evidence(id),
          primary key(function_id,cpu_pc))""")
        c.execute("""create table function_cfg_edges(
          function_id text not null,source_pc integer not null,target_pc integer not null,kind text not null,runtime_observed integer not null,
          primary key(function_id,source_pc,target_pc,kind),
          foreign key(function_id,source_pc) references function_instructions(function_id,cpu_pc),
          foreign key(function_id,target_pc) references function_instructions(function_id,cpu_pc))""")
        c.execute("""create table function_reconstructions(
          function_id text primary key references functions(id),end_exclusive integer not null,
          assembly_source text not null,parity_status text not null,parity_receipt text not null,
          expected_bytes_sha256 text not null,assembled_bytes_sha256 text not null,limitations_json text not null)""")
        c.execute("""create table function_operand_accesses(
          id integer primary key,function_id text not null,cpu_pc integer not null,frame integer not null,
          kind text not null check(kind in ('READ','WRITE')),address integer not null,bus_data integer not null,bus_mask integer not null,
          bus_width_bits integer not null check(bus_width_bits=16),snapshot_json text not null,evidence_id text not null references evidence(id),
          foreign key(function_id,cpu_pc) references function_instructions(function_id,cpu_pc))""")
        c.execute("""create table function_data_xrefs(
          function_id text not null,cpu_pc integer not null,record_address integer not null,record_offset integer not null,
          data_kind text not null,access_bytes integer not null,evidence_id text not null references evidence(id),
          primary key(function_id,cpu_pc,record_address,record_offset),
          foreign key(function_id,cpu_pc) references function_instructions(function_id,cpu_pc))""")
        for eid,typ,uri,status,desc in [
          ("collision-recovery-v02","runtime_control_and_operand_trace",str(trace),"RUNTIME_PROVEN","One-frame 44 operand accesses; entry/RTS/return trace; SP expressions inconclusive and excluded from proof."),
          ("collision-leaf-parity-v01","source_authored_assembly_parity",str(ROOT/"evidence/collision_assembly_parity_v01.json"),"ASSEMBLY_PARITY_PASS","72 source-authored bytes match source ROM hash; no raw code stored in DB."),
          ("collision-reconstruction-v01","bounded_callable_cfg",str(report),"RUNTIME_ENTRY_STATIC_CFG_PARITY_VERIFIED","Direct BSR entry + closed CFG to RTS; shared tail with wrapper; not exclusive ownership or exhaustive incoming-call proof.")]:
            c.execute("insert into evidence values (?,?,?,?,?)",(eid,typ,uri,status,desc))
        note=r["bounds_basis"]+"; "+r["ownership_limit"]
        c.execute("insert into functions values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(fid,entry,"HBMAME :maincpu program address","sz3mx.03",entry,
          "EXACT_OBSERVED_REGION_OPCODE_FILE_PARITY","push_edge_distance_candidate","Observed opponent-edge distance using +9C/+CB; higher gameplay semantics unproved","HIGH",
          r["status"],"direct BSR target and runtime entry/RTS/return",1,1,note))
        for eid in ("collision-recovery-v02","collision-leaf-parity-v01","collision-reconstruction-v01"):
            c.execute("insert into function_evidence values (?,?,?)",(fid,eid,"entry/region reconstruction evidence; no gameplay fix"))
        c.execute("insert into function_issues values (?,?,?)",(fid,"hitboxes","verified_collision_data_reader_investigation_not_fix"))
        for b in r["blocks"]:
            c.execute("insert into function_basic_blocks values (?,?,?,?,?)",(b["id"],fid,b["start"],b["end_exclusive"],"collision-reconstruction-v01"))
        visited=set(r["runtime_visited_instruction_addresses"])
        for i in r["instructions"]:
            block=next(b["id"] for b in r["blocks"] if i["pc"] in b["instruction_addresses"])
            c.execute("insert into function_instructions values (?,?,?,?,?,?,?,?)",(fid,i["pc"],block,i["size"],i["instruction"],int(i["pc"] in visited),
               "HBMAME_DISASSEMBLY_FILE_MATCH_REGION_PARITY","collision-reconstruction-v01"))
        for e in r["edges"]:c.execute("insert into function_cfg_edges values (?,?,?,?,?)",(fid,e["source"],e["target"],e["kind"],int(e["runtime_observed"])))
        for call in r["incoming_calls"]:
            assert not c.execute("select 1 from calls where site_address=?",(call["site"],)).fetchone()
            c.execute("insert into calls(caller_id,callee_id,site_address,target_address,kind,confidence,evidence_id) values (?,?,?,?,?,?,?)",
              (None,fid,call["site"],entry,"static_direct_call",call["status"],"collision-reconstruction-v01"))
        c.execute("insert into function_reconstructions values (?,?,?,?,?,?,?,?)",(fid,end,r["parity"]["assembly_source"],"PASS",
          "evidence/collision_assembly_parity_v01.json",r["parity"]["expected_original_bytes_sha256"],r["parity"]["assembled_bytes_sha256"],json.dumps(r["limitations"]+[r["ownership_limit"],r["calling_convention"]["stack_caveat"]])))
        source="docs/COLLISION_RECONSTRUCTION_V01.json"
        for field,off,meaning in [("active_marker",0,"Active-byte gate observed"),("opponent_word",0x38,"Word sign-extended into A4; 24-bit bus mask"),
             ("edge_orientation",0x2c9,"Byte tested against 1; visual facing semantics not proved"),("edge_distance",0x21c,"Observed 16-bit absolute delta to computed opponent edge")]:
            c.execute("insert into ram_fields values (?,?,?,?,?,?)",("sfa3_player_pool",field,off,meaning,"RUNTIME_INSTRUCTION_AND_VALUE_FLOW_PROVEN",source))
        for pc,field,kind in [(0x2c19c,"active_marker","READ"),(0x2c1a0,"opponent_word","READ"),(0x2c1a6,"id_cb","READ"),(0x2c1ac,"box9c","READ"),
              (0x2c1be,"edge_orientation","READ"),(0x2c1ce,"pos_x","READ"),(0x2c1d2,"pos_x","READ"),(0x2c1dc,"edge_distance","WRITE")]:
            c.execute("insert into function_ram_xrefs values (?,?,?,?,?,?,?)",(fid,"sfa3_player_pool",field,pc,kind,str(trace),"RUNTIME_PROVEN_WITHIN_VERIFIED_ENTRY_REGION"))
        for seq,row in enumerate(rows,1):
            c.execute("insert into function_operand_accesses values (?,?,?,?,?,?,?,?,?,?,?)",(seq,fid,int(row["pc"],16),int(row["frame"]),row["kind"],int(row["address"],16),int(row["data"],16),int(row["mask"],16),16,json.dumps(row,sort_keys=True),"collision-recovery-v02"))
        for rec in r["table_records"]:
            for pc,off,kind in [(0x2c1b6,4,"x_radius_u16"),(0x2c1bc,0,"x_offset_s16")]:
                c.execute("insert into function_data_xrefs values (?,?,?,?,?,?,?)",(fid,pc,rec["record_address"],off,kind,2,"collision-recovery-v02"))
        updated=c.execute("update runtime_collision_instructions set function_id=? where cpu_pc>=? and cpu_pc<? and function_id is null",(fid,entry,end)).rowcount
        assert updated==2
        assert c.execute("select * from functions where id!=?",(fid,)).fetchall()==original_functions
        assert c.execute("select * from calls where id<=?",(max(x[0] for x in original_calls),)).fetchall()==original_calls
        assert c.execute("select * from ram_box_decodes").fetchall()==original_boxes
        assert c.execute("pragma integrity_check").fetchall()==[("ok",)] and not c.execute("pragma foreign_key_check").fetchall()
        c.commit()
        assert c.execute("pragma integrity_check").fetchall()==[("ok",)] and not c.execute("pragma foreign_key_check").fetchall()
        receipt={"status":"PASS","function_id":fid,"total_functions":c.execute("select count(*) from functions").fetchone()[0],
          "original_functions_preserved":len(original_functions),"total_calls":c.execute("select count(*) from calls").fetchone()[0],
          "blocks":len(r["blocks"]),"instructions":len(r["instructions"]),"operand_accesses":len(rows),
          "ram_xrefs":c.execute("select count(*) from function_ram_xrefs where function_id=?",(fid,)).fetchone()[0],
          "data_xrefs":4,"prior_instruction_owners_resolved":updated,"backup":str(backup),"integrity":"ok","foreign_keys":"PASS"}
        (ROOT/"evidence/collision_reconstruction_db_receipt_v01.json").write_text(json.dumps(receipt,indent=2))
        print(json.dumps(receipt))
    except Exception:c.rollback();raise
    finally:c.close()
if __name__=="__main__":main()
