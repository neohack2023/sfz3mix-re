"""Append V03 consumer proof; preserve every previous SQLite row and assembly source."""
import hashlib,json,sqlite3
from pathlib import Path
R=Path(r"D:\AIOS_SFZ3MIX_V032")
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 report=R/"evidence/collision_consumer_v03.json";r=json.loads(report.read_text());eid="collision-consumer-v03"
 assert r["consumer"]["parity"]["decision"]=="PASS"
 assert sha(R/"tools/sz3mx.03")==r["rom_sha256"]
 assert sha(R/"evidence/collision_scenarios_v03.jsonl")==r["scenarios"]["trace_sha256"]
 old=json.loads((R/"evidence/collision_engine_recovery_v02.json").read_text())
 protected=[("tools/collision_leaf_02c19a_v01.s","c9e9bd5c0526032a8eec09d5e93bca0a533a07be2e64815229bbd02f0c0b0c90")]+[(x["source"],x["source_sha256"]) for x in old["assembly"]]
 for p,h in protected:assert sha(R/p)==h
 backup=R/"evidence/functions_v01_before_collision_consumer_v03.sqlite";assert not backup.exists(),"No replay over a retained rollback backup"
 c=sqlite3.connect(R/"evidence/functions_v01.sqlite");c.execute("pragma foreign_keys=on")
 def check(db):
  assert db.execute("pragma integrity_check").fetchall()==[("ok",)]
  assert not db.execute("pragma foreign_key_check").fetchall()
 check(c)
 names=[x[0] for x in c.execute("select name from sqlite_master where type='table' and name not like 'sqlite_%'")]
 before={n:c.execute('select * from "'+n+'"').fetchall() for n in names}
 with sqlite3.connect(backup) as b:c.backup(b);check(b)
 events=[json.loads(x) for x in (R/"evidence/collision_scenarios_v03.jsonl").read_text().splitlines()]
 try:
  c.execute("begin immediate")
  c.execute("insert into evidence values (?,?,?,?,?)",(eid,"targeted_gameplay_reads_branch_trace_assembly_parity",str(report),"RUNTIME_CONSUMER_AND_PARITY_PROVEN","147 actual +21C reads,40 value-formula checks,44-byte parity; near-success path/caller semantics unresolved"))
  c.execute("create table collision_consumer_regions(id text primary key,start_address integer,end_exclusive integer,function_id text references functions(id),issue_id text references issues(id),semantics text,confidence text,evidence_id text references evidence(id))")
  c.execute("insert into collision_consumer_regions values (?,?,?,?,?,?,?,?)",("REGION_037A56",0x37a56,0x37a82,None,"hitboxes",r["consumer"]["semantics"],"RUNTIME_READ_FAR_BRANCH_AND_ASSEMBLY_PARITY",eid))
  c.execute("create table collision_consumer_instructions(region_id text references collision_consumer_regions(id),cpu_pc integer,size_bytes integer,instruction text,evidence_id text references evidence(id),primary key(region_id,cpu_pc))")
  for x in r["consumer"]["instructions"]:c.execute("insert into collision_consumer_instructions values (?,?,?,?,?)",("REGION_037A56",x["pc"],x["size"],x["instruction"],eid))
  c.execute("create table collision_consumer_blocks(id text primary key,region_id text references collision_consumer_regions(id),start_address integer,end_exclusive integer,evidence_id text references evidence(id))")
  for a,b in [(0x37a56,0x37a5e),(0x37a5e,0x37a64),(0x37a64,0x37a6c),(0x37a6c,0x37a7a),(0x37a7a,0x37a7e),(0x37a7e,0x37a82)]:
   c.execute("insert into collision_consumer_blocks values (?,?,?,?,?)",(f"BB_CONSUMER_{a:06X}","REGION_037A56",a,b,eid))
  c.execute("create table collision_consumer_edges(region_id text references collision_consumer_regions(id),source_pc integer,target_pc integer,kind text,runtime_proven integer,evidence_id text references evidence(id),primary key(region_id,source_pc,target_pc,kind))")
  ins=r["consumer"]["instructions"]
  branches={0x37a5c:(0x37a7a,0x37a5e),0x37a62:(0x37a7a,0x37a64),0x37a6a:(0x37a7a,0x37a6c),0x37a78:(0x37a7e,0x37a7a)}
  for x in ins:
   pc=x["pc"]
   if pc in branches:
    for kind,target in zip(("conditional_taken","conditional_fallthrough"),branches[pc]):
     c.execute("insert into collision_consumer_edges values (?,?,?,?,?,?)",("REGION_037A56",pc,target,kind,int(pc==0x37a5c and target==0x37a7a),eid))
   elif not x["instruction"].startswith("rts"):
    target=pc+x["size"];c.execute("insert into collision_consumer_edges values (?,?,?,?,?,?)",("REGION_037A56",pc,target,"fallthrough",int(pc in (0x37a56,0x37a7a)),eid))
  c.execute("create table collision_consumer_sites(cpu_pc integer primary key,function_id text references functions(id),region_id text references collision_consumer_regions(id),summary_json text,evidence_id text references evidence(id))")
  for x in r["scenarios"]["read_sites"]:
   c.execute("insert into collision_consumer_sites values (?,?,?,?,?)",(x["pc"],None,"REGION_037A56" if x["pc"]==0x37a56 else None,json.dumps(x),eid))
  c.execute("create table collision_scenario_summaries(phase text primary key,summary_json text,evidence_id text references evidence(id))")
  for x in r["scenarios"]["phase_summary"]:c.execute("insert into collision_scenario_summaries values (?,?,?)",(x["phase"],json.dumps(x),eid))
  for x in events:
   if x["type"]!="CPU":continue
   owner="FUNC_REC_02C19A" if x["kind"]=="WRITE" and x["pc"]==0x2c1dc else None
   c.execute("insert into runtime_collision_dependencies(cpu_pc,function_id,frame,kind,address,bus_data,bus_mask,snapshot_json,evidence_id) values (?,?,?,?,?,?,?,?,?)",(x["pc"],owner,x["frame"],x["kind"],x["address"],x["data"],x["mask"],json.dumps(x,sort_keys=True),eid))
  p=r["consumer"]["parity"]
  c.execute("insert into assembly_region_reconstructions values (?,?,?,?,?,?,?,?)",(0x37a56,0x37a82,p["source"],p["source_sha256"],p["expected_sha256"],p["assembled_sha256"],"PASS",eid))
  c.execute("insert into function_evidence values (?,?,?)",("FUNC_REC_02C19A",eid,"40 targeted output writes match reconstructed arithmetic; first downstream consumer verified separately"))
  for n,rows in before.items():
   now=c.execute('select * from "'+n+'"').fetchall();assert all(x in now for x in rows),n
  assert c.execute("select count(*) from functions").fetchone()[0]==61
  assert c.execute("select count(*) from calls").fetchone()[0]==80
  check(c);c.commit();check(c)
  result=dict(status="PASS",backup=str(backup),all_previous_rows_preserved=True,protected_assembly_sources=len(protected),consumer_regions=1,consumer_sites=10,consumer_instructions=14,consumer_blocks=6,new_cpu_observations=187,functions=61,calls=80,integrity="ok",foreign_key_errors=[])
  (R/"evidence/collision_consumer_db_receipt_v03.json").write_text(json.dumps(result,indent=2));print(json.dumps(result))
 except Exception:c.rollback();raise
 finally:c.close()
if __name__=="__main__":main()
