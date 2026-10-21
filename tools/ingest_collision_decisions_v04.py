"""Transactional V04 callable/caller/state claims; no old evidence is overwritten."""
import hashlib,json,shutil,sqlite3
from pathlib import Path
R=Path(r"D:\AIOS_SFZ3MIX_V032")
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 assert shutil.disk_usage(R).free>=12*1024*1024,"Insufficient migration/rollback margin"
 report=R/"evidence/collision_decisions_v04.json";r=json.loads(report.read_text());eid="collision-decisions-v04";fid="FUNC_REC_037A46"
 assert all(x["status"]=="PASS" for x in r["assembly"])
 assert sha(R/"tools/sz3mx.03")==r["rom_sha256"]
 checks=[("tools/collision_leaf_02c19a_v01.s","c9e9bd5c0526032a8eec09d5e93bca0a533a07be2e64815229bbd02f0c0b0c90")]
 old=json.loads((R/"evidence/collision_engine_recovery_v02.json").read_text());checks += [(x["source"],x["source_sha256"]) for x in old["assembly"]]
 v3=json.loads((R/"evidence/collision_consumer_v03.json").read_text());checks.append((v3["consumer"]["parity"]["source"],v3["consumer"]["parity"]["source_sha256"]))
 for p,h in checks:assert sha(R/p)==h
 c=sqlite3.connect(R/"evidence/functions_v01.sqlite");c.execute("pragma foreign_keys=on")
 def integrity(db):
  assert db.execute("pragma integrity_check").fetchall()==[("ok",)]
  assert not db.execute("pragma foreign_key_check").fetchall()
 integrity(c)
 names=[x[0] for x in c.execute("select name from sqlite_master where type='table' and name not like 'sqlite_%'")]
 before={n:c.execute('select * from "'+n+'"').fetchall() for n in names}
 assert not c.execute("select id from functions where cpu_address=0x37a46").fetchall(),"Reconcile existing identity; do not duplicate"
 backup=R/"evidence/functions_v01_before_collision_decisions_v04.sqlite";assert not backup.exists(),"No migration replay"
 with sqlite3.connect(backup) as b:c.backup(b);integrity(b)
 try:
  c.execute("begin immediate")
  c.execute("insert into evidence values (?,?,?,?,?)",(eid,"runtime_calls_threshold_negatives_visual_correlation_assembly_parity",str(report),"VERIFIED_BOUNDED_RESULTS_SUCCESS_UNREACHED","Callable37A46, caller379B4, five parity regions; near success remains unresolved"))
  c.execute("insert into functions values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(fid,0x37a46,"HBMAME :maincpu program address","sz3mx.03",0x37a46,"REGION_SOURCE_PARITY_WITH_LIVE_CALL_CONTROL","opponent_grounded_near_predicate","Boolean predicate used by a decision selector; named mechanic unresolved","HIGH","RUNTIME_CALLABLE_ENTRY_SHARED_BODY_PROVEN","BSR379B4, traced entry/helper/return379B8; source parity",1,1,"Nonexclusive body reuses V03 region; helper shares false return blocks; positive path not observed"))
  c.execute("insert into function_evidence values (?,?,?)",(fid,eid,"live callable entry/return, caller flags, shared region"))
  c.execute("insert into function_issues values (?,?,?)",(fid,"hitboxes","investigation_not_fix_no_causal_link"))
  c.execute("create table function_consumer_region_memberships(function_id text references functions(id),region_id text references collision_consumer_regions(id),evidence_id text references evidence(id),primary key(function_id,region_id))")
  c.execute("insert into function_consumer_region_memberships values (?,?,?)",(fid,"REGION_037A56",eid))
  c.execute("create table collision_region_ownership_claims(region_id text primary key references collision_consumer_regions(id),function_id text references functions(id),confidence text,evidence_id text references evidence(id))")
  c.execute("insert into collision_region_ownership_claims values (?,?,?,?)",("REGION_037A56",fid,"VERIFIED_ENTRY_BOUNDED_MEMBERSHIP_NOT_EXCLUSIVE",eid))
  for a,b in [(0x37a46,0x37a4a),(0x37a4a,0x37a4c),(0x37a4c,0x37a56)]:
   bid=f"BB_{a:06X}";c.execute("insert into function_basic_blocks values (?,?,?,?,?)",(bid,fid,a,b,eid))
   for i in r["callable"]["instructions"]:
    if a<=i["pc"]<b:c.execute("insert into function_instructions values (?,?,?,?,?,?,?,?)",(fid,i["pc"],bid,i["size"],i["instruction"],1,"SOURCE_PARITY_AND_RUNTIME_CONTROL_TRACE",eid))
  for site,target,callee,caller,kind,confidence in [(0x379b4,0x37a46,fid,None,"runtime_direct_call","RUNTIME_CALL_RETURN"),(0x37a46,0x37a82,None,fid,"runtime_direct_call","RUNTIME_HELPER_CALL_RETURN"),(0x2c584,0x3797e,None,None,"static_direct_call","STATIC_JSR_LIVE_POSTCALL_RETURN")]:
   assert not c.execute("select 1 from calls where site_address=?",(site,)).fetchone()
   c.execute("insert into calls(caller_id,callee_id,site_address,target_address,kind,confidence,evidence_id) values (?,?,?,?,?,?,?)",(caller,callee,site,target,kind,confidence,eid))
   c.execute("insert into function_control_relationships values (?,?,?,?,?,?,?)",(site,target,"call",caller,callee,int(kind=="runtime_direct_call"),eid))
  for p in r["assembly"]:
   c.execute("insert into assembly_region_reconstructions values (?,?,?,?,?,?,?,?)",(p["start"],p["end_exclusive"],p["source"],p["source_sha256"],p["expected_sha256"],p["assembled_sha256"],"PASS",eid))
  p=r["assembly"][0]
  c.execute("insert into function_reconstructions values (?,?,?,?,?,?,?,?)",(fid,0x37a82,p["source"],"PASS",str(report),p["expected_sha256"],p["assembled_sha256"],json.dumps(r["limits"])))
  c.execute("insert into function_contracts values (?,?,?)",(fid,json.dumps(r["callable"]),eid))
  c.execute("create table collision_decision_trials(id text primary key,status text,details_json text,evidence_id text references evidence(id))")
  added=0
  for t in r["trials"]:
   path=R/f'evidence/{t["stem"]}.jsonl';assert sha(path)==t["sha256"]
   c.execute("insert into collision_decision_trials values (?,?,?,?)",(t["stem"],t["status"],json.dumps(t),eid))
   if t["status"]!="COMPLETE_BOUNDED_NEGATIVE":continue
   for x in (json.loads(l) for l in path.read_text().splitlines()):
    if x["type"]!="CPU":continue
    owner="FUNC_REC_02C19A" if x["pc"]==0x2c1dc else fid if 0x37a46<=x["pc"]<0x37a82 else None
    x["trial_id"]=t["stem"]
    c.execute("insert into runtime_collision_dependencies(cpu_pc,function_id,frame,kind,address,bus_data,bus_mask,snapshot_json,evidence_id) values (?,?,?,?,?,?,?,?,?)",(x["pc"],owner,x["frame"],x["kind"],x["address"],x["data"],x["mask"],json.dumps(x,sort_keys=True),eid));added+=1
  c.execute("create table collision_state_move_observations(id text primary key,observation_json text,evidence_id text references evidence(id))")
  c.execute("insert into collision_state_move_observations values (?,?,?)",("ryu-standing-button1-punch-interval3349",json.dumps(dict(move=r["move_observation"],visual=r["visual_evidence"])),eid))
  c.execute("create table collision_decision_dataflow(id text primary key,relation_json text,evidence_id text references evidence(id))")
  c.execute("insert into collision_decision_dataflow values (?,?,?)",("predicate-to-selector-apply",json.dumps(r["result_use"]),eid))
  for n,rows in before.items():
   now=c.execute('select * from "'+n+'"').fetchall();assert all(x in now for x in rows),n
  assert c.execute("select count(*) from functions").fetchone()[0]==62 and c.execute("select count(*) from calls").fetchone()[0]==83
  integrity(c);c.commit();integrity(c)
  for p,h in checks:assert sha(R/p)==h
  result=dict(status="PASS",functions=62,calls=83,assembly_regions_added=5,source_bytes_reassembled=112,new_unique_bytes=68,protected_old_sources=5,all_old_rows_preserved=True,added_cpu_observations=added,success_return_observed=False,integrity="ok",foreign_key_errors=[],backup=str(backup))
  (R/"evidence/collision_decisions_db_receipt_v04.json").write_text(json.dumps(result,indent=2));print(json.dumps(result))
 except Exception:c.rollback();raise
 finally:c.close()
if __name__=="__main__":main()
