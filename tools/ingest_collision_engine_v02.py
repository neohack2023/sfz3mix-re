"""Add V02 proof to the existing DB, retaining shared blocks and unresolved owners."""
import csv,hashlib,json,sqlite3
from pathlib import Path
R=Path(r"D:\AIOS_SFZ3MIX_V032")
def main():
 report=R/"evidence/collision_engine_recovery_v02.json";r=json.loads(report.read_text());fid=r["wrapper"]["id"];eid="collision-engine-v02"
 assert all(x["decision"]=="PASS" for x in r["assembly"])
 assert hashlib.sha256((R/"tools/sz3mx.03").read_bytes()).hexdigest()==r["source_rom_sha256"]
 trace=R/"evidence/collision_engine_v02.tsv";assert hashlib.sha256(trace.read_bytes()).hexdigest()==r["capture"]["trace_sha256"]
 rows=list(csv.DictReader([x for x in trace.read_text().splitlines() if not x.startswith("#")],delimiter="\t"));assert len(rows)==180
 backup=R/"evidence/functions_v01_before_collision_engine_v02.sqlite";assert not backup.exists(),"Inspect prior migration; no replay"
 c=sqlite3.connect(R/"evidence/functions_v01.sqlite");c.execute("pragma foreign_keys=on")
 def checks(conn):
  assert conn.execute("pragma integrity_check").fetchall()==[("ok",)]
  assert not conn.execute("pragma foreign_key_check").fetchall()
 checks(c)
 names=[x[0] for x in c.execute("select name from sqlite_master where type='table' and name not like 'sqlite_%'")]
 before={name:c.execute('select * from "'+name+'"').fetchall() for name in names}
 with sqlite3.connect(backup) as b:c.backup(b);checks(b)
 try:
  c.execute("begin immediate")
  c.execute("insert into evidence values (?,?,?,?,?)",(eid,"runtime_control_operand_and_assembly_parity",str(report),"RUNTIME_PROVEN_WITH_BOUNDED_LIMITS","Wrapper shared tail, seven unresolved site assessments, 180 operands; no +21C reads in eight frames."))
  c.execute("insert into functions values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(fid,0x2c17e,"HBMAME :maincpu program address","sz3mx.03",0x2c17e,"EXACT_OBSERVED_REGION_OPCODE_FILE_PARITY","four_slot_edge_distance_wrapper","Three calls then shared leaf fallthrough","HIGH","RUNTIME_CALLABLE_WRAPPER_SHARED_TAIL","Live call at02C07E, wrapper entry, subcall returns and return02C082",1,1,"Shared leaf blocks retained once; all indirect entries and stack ABI unresolved"))
  c.execute("insert into function_evidence values (?,?,?)",(fid,eid,"runtime wrapper ownership and prefix parity"))
  c.execute("insert into function_issues values (?,?,?)",(fid,"hitboxes","collision_data_investigation_not_fix"))
  c.execute("create table function_shared_blocks(function_id text not null references functions(id),block_id text not null references function_basic_blocks(id),evidence_id text not null references evidence(id),primary key(function_id,block_id))")
  for block, in c.execute("select id from function_basic_blocks where function_id='FUNC_REC_02C19A'").fetchall():
   c.execute("insert into function_shared_blocks values (?,?,?)",(fid,block,eid))
  for start,end in [(0x2c17e,0x2c186),(0x2c186,0x2c18e),(0x2c18e,0x2c196),(0x2c196,0x2c19a)]:
   bid=f"BB_{start:06X}"
   c.execute("insert into function_basic_blocks values (?,?,?,?,?)",(bid,fid,start,end,eid))
   for i in r["wrapper_instructions"]:
    if start<=i["pc"]<end:
     c.execute("insert into function_instructions values (?,?,?,?,?,?,?,?)",(fid,i["pc"],bid,i["size"],i["instruction"],1,"HBMAME_FILE_AND_SOURCE_ASSEMBLY_PARITY",eid))
  for pc in (0x2c182,0x2c18a,0x2c192):
   assert c.execute("select caller_id,callee_id from calls where site_address=?",(pc,)).fetchall()==[(None,"FUNC_REC_02C19A")]
   c.execute("update calls set caller_id=?,kind=?,confidence=?,evidence_id=? where site_address=?",(fid,"runtime_direct_call","RUNTIME_PROVEN",eid,pc))
  c.execute("insert into calls(caller_id,callee_id,site_address,target_address,kind,confidence,evidence_id) values (?,?,?,?,?,?,?)",(None,fid,0x2c07e,0x2c17e,"runtime_direct_call","RUNTIME_PROVEN",eid))
  c.execute("create table function_control_relationships(site_pc integer,target_pc integer,kind text,caller_id text references functions(id),callee_id text references functions(id),runtime_proven integer,evidence_id text references evidence(id),primary key(site_pc,target_pc,kind))")
  for pc,target,kind,caller,callee,live in [(0x2c07e,0x2c17e,"call",None,fid,1),(0x2c182,0x2c19a,"call",fid,"FUNC_REC_02C19A",1),(0x2c18a,0x2c19a,"call",fid,"FUNC_REC_02C19A",1),(0x2c192,0x2c19a,"call",fid,"FUNC_REC_02C19A",1),(0x2c196,0x2c19a,"fallthrough_shared",fid,"FUNC_REC_02C19A",1),(0x27ef8,0x296a6,"call",None,None,0)]:
   c.execute("insert into function_control_relationships values (?,?,?,?,?,?,?)",(pc,target,kind,caller,callee,live,eid))
  c.execute("create table collision_reader_assessments(cpu_pc integer primary key references runtime_collision_instructions(cpu_pc),region_start integer,region_end_exclusive integer,function_id text references functions(id),confidence text,details_json text,evidence_id text references evidence(id))")
  for x in r["reader_sites"]:c.execute("insert into collision_reader_assessments values (?,?,?,?,?,?,?)",(x["pc"],x["region_start"],x["region_end_exclusive"],None,x["confidence"],json.dumps(x),eid))
  c.execute("create table runtime_collision_dependencies(id integer primary key,cpu_pc integer,function_id text references functions(id),frame integer,kind text,address integer,bus_data integer,bus_mask integer,snapshot_json text,evidence_id text references evidence(id))")
  for seq,x in enumerate(rows,1):
   pc=int(x["pc"],16);owner="FUNC_REC_02C19A" if pc==0x2c1dc else None
   c.execute("insert into runtime_collision_dependencies values (?,?,?,?,?,?,?,?,?,?)",(seq,pc,owner,int(x["frame"]),x["kind"],int(x["address"],16),int(x["data"],16),int(x["mask"],16),json.dumps(x,sort_keys=True),eid))
  c.execute("create table collision_data_dependencies(cpu_pc integer,address integer,record_address integer,record_offset integer,width_bytes integer,value integer,function_id text references functions(id),evidence_id text references evidence(id),primary key(cpu_pc,address))")
  for x in r["record_reads"]:c.execute("insert into collision_data_dependencies values (?,?,?,?,?,?,?,?)",(x["pc"],x["address"],x["record"],x["offset"],x["width"],x["value"],None,eid))
  c.execute("create table assembly_region_reconstructions(start_address integer primary key,end_exclusive integer,source_path text,source_sha256 text,expected_sha256 text,assembled_sha256 text,parity_status text,evidence_id text references evidence(id))")
  for x in r["assembly"]:c.execute("insert into assembly_region_reconstructions values (?,?,?,?,?,?,?,?)",(x["start"],x["end_exclusive"],x["source"],x["source_sha256"],x["expected_sha256"],x["assembled_sha256"],x["decision"],eid))
  c.execute("create table function_contracts(function_id text primary key references functions(id),contract_json text,evidence_id text references evidence(id))")
  c.execute("insert into function_contracts values (?,?,?)",(fid,json.dumps(r["wrapper"]),eid))
  # Preserve every previous row; only the three explicitly proven call owners change.
  for name,old in before.items():
   now=c.execute('select * from "'+name+'"').fetchall()
   if name=="calls":
    byid={x[0]:x for x in now}
    for x in old:
     if x[3] in (0x2c182,0x2c18a,0x2c192):
      y=byid[x[0]];assert y[1]==fid and y[2:5]==x[2:5]
     else:assert byid[x[0]]==x
   else:assert all(x in now for x in old),name
  assert c.execute("select count(*) from functions").fetchone()[0]==61
  assert c.execute("select count(*) from calls").fetchone()[0]==80
  checks(c);c.commit();checks(c)
  result=dict(status="PASS",functions=61,calls=80,shared_blocks=7,new_wrapper_blocks=4,new_operand_rows=180,reader_site_assessments=7,remaining_unowned_sites=7,assembly_regions=3,integrity="ok",foreign_key_errors=[],backup=str(backup),preservation="Every previous row retained except three proven call ownership/confidence/evidence updates")
  (R/"evidence/collision_engine_db_receipt_v02.json").write_text(json.dumps(result,indent=2));print(json.dumps(result))
 except Exception:c.rollback();raise
 finally:c.close()
if __name__=="__main__":main()
