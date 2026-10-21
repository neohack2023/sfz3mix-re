"""V04 caller proof, controlled negative cases, visual correlation and exact assembly."""
import hashlib,json,re,subprocess,shutil
from pathlib import Path
from bounded_m68k_export_v01 import decode,fixture
R=Path(r"D:\AIOS_SFZ3MIX_V032")
SHA="b5f7a1598e4f91a5113c506505b482b2cd1a19e366fe31471740e45dbd204691"
def h(x):return hashlib.sha256(x).hexdigest()
def main():
 rom=(R/"tools/sz3mx.03").read_bytes();assert h(rom)==SHA;fixture()
 protected=json.loads((R/"evidence/collision_consumer_v03.json").read_text())
 assert h((R/protected["consumer"]["parity"]["source"]).read_bytes())==protected["consumer"]["parity"]["source_sha256"]
 trials=[]
 for stem,console,complete in [("collision_decisions_v04","decision_v04",False),("collision_decisions_controlled_v04","decision_controlled_v04",True),("collision_decisions_crouch_v04","decision_crouch_v04",True)]:
  path=R/f"evidence/{stem}.jsonl";rows=[json.loads(x) for x in path.read_text().splitlines()]
  launch=json.loads((R/f"evidence/{stem}_launch.json").read_text());assert launch["exit_code"]==0 and not launch["stderr"]
  assert path.stat().st_size<900000
  assert (rows[-1]["type"]=="COMPLETE")==complete
  con=(R/f"evidence/{console}_console.txt").read_text()
  assert not re.search(r"(?:DEC_RETURN|VALID_NEAR_RETURN)[^\n]*d0=1(?: |$)",con)
  near=[x for x in rows if x.get("pc")==0x37a56 and x.get("kind")=="READ" and x["data"]<48]
  far=[x for x in rows if x.get("pc")==0x37a56 and x.get("kind")=="READ" and x["data"]>=48]
  stores=[x for x in rows if x.get("pc")==0x37a3e and x.get("kind")=="WRITE"]
  assert not stores
  if complete:assert near and far and all(x["p1"]["a9"]==0 for x in near)
  trials.append(dict(stem=stem,status="COMPLETE_BOUNDED_NEGATIVE" if complete else "PARTIAL_LOG_CAP_REACHED_CONTROL_TRACES_VALID",events=len(rows),bytes=path.stat().st_size,sha256=h(path.read_bytes()),last_logged_frame=rows[-1]["frame"],near_reads=[dict(frame=x["frame"],value=x["data"],opponent_a9=x["p1"]["a9"],receiver_state4=x["p2"]["state4"],receiver_state6=x["p2"]["state6"],opponent_state4=x["p1"]["state4"]) for x in near],far_sample_values=sorted(set(x["data"] for x in far)),success_stores=0,positive_returns=0,phases=[dict(frame=x["frame"],phase=x["phase"],p1=x["p1"],p2=x["p2"]) for x in rows if x["type"]=="PHASE"]))
 far=(R/"evidence/decision_v04_far.txt").read_text();near=(R/"evidence/decision_v04_near.txt").read_text()
 pcs=lambda s:[int(x.split(":")[0],16) for x in s.splitlines()]
 assert pcs(far)[0]==0x37a46 and pcs(far)[-1]==0x379b8 and 0x37a56 in pcs(far)
 assert pcs(near)==[0x37a46,0x37a82,0x37a88,0x37a8a,0x37a90,0x37a7a,0x37a7c,0x37a4a,0x37a7a,0x37a7c,0x379b8]
 base="/mnt/d/AIOS_SFZ3MIX_V032";parity=[]
 for name,start,end in [("collision_predicate_037a46_v04",0x37a46,0x37a82),("collision_caller_0379ae_v04",0x379ae,0x379bc),("collision_success_037a3e_v04",0x37a3e,0x37a46),("collision_apply_037ad2_v04",0x37ad2,0x37ae0),("collision_outer_02c584_v04",0x2c584,0x2c594)]:
  cmd=f"set -e; cd {base}; export LD_LIBRARY_PATH={base}/tools/.m68k_toolchain/usr/lib/x86_64-linux-gnu; {base}/tools/.m68k_toolchain/usr/bin/m68k-linux-gnu-as -m68000 -o evidence/{name}.o tools/{name}.s; {base}/tools/.m68k_toolchain/usr/bin/m68k-linux-gnu-objcopy -O binary -j .text evidence/{name}.o evidence/{name}.bin"
  run=subprocess.run(["wsl.exe","bash","-c",cmd],capture_output=True,text=True,timeout=30);assert run.returncode==0,(run.stdout,run.stderr)
  actual=(R/f"evidence/{name}.bin").read_bytes();expected=rom[start:end]
  mismatch=[start+i for i in range(max(len(actual),len(expected))) if actual[i:i+1]!=expected[i:i+1]]
  rec=dict(source=f"tools/{name}.s",start=start,end_exclusive=end,size=len(actual),source_sha256=h((R/f"tools/{name}.s").read_bytes()),expected_sha256=h(expected),assembled_sha256=h(actual),mismatch_addresses=mismatch,status="PASS" if not mismatch else "FAIL")
  parity.append(rec);assert not mismatch,rec
 instructions=decode(rom,0x37a46,60)
 for x in instructions:x.pop("opcode")
 controlled=[json.loads(x) for x in (R/"evidence/collision_decisions_controlled_v04.jsonl").read_text().splitlines()]
 correlated=next(x for x in controlled if x["frame"]==3349 and x["p1"]["a9"]==1)
 pictures=[]
 for file,label,frame in [("decision_controlled_v04_punch_2.png","Ryu standing Button1 punch; Sakura airborne reaction pose",3349),("decision_crouch_v04_punch_1.png","Ryu crouching pose with Button1 input; strike identity unresolved",3053)]:
  p=R/"evidence"/file;assert p.read_bytes()[:8]==b"\x89PNG\r\n\x1a\n"
  pictures.append(dict(local_path=str(p),sha256=h(p.read_bytes()),frame_done_interval=frame,visual_observation=label,identity_source="HUD RYU and SAKURA",timing_limit="Screenshot and CPU snapshot share interval labels, not an atomic state sample"))
 report=dict(schema="sfz3mix.collision_decisions.v04",preflight="READY_CONTINUE",rom_sha256=SHA,
 decision="PARTIAL_MILESTONE_SUCCESS_PATH_NOT_REACHED",trials=trials,assembly=parity,
 callable=dict(function_id="FUNC_REC_037A46",entry=0x37a46,end_exclusive=0x37a82,instructions=instructions,caller_site=0x379b4,return_pc=0x379b8,helper_target=0x37a82,shared_region_id="REGION_037A56",exclusive_ownership=False,entry_proof="Actual caller breakpoint, traced entry/helper/RTS and return;60-byte source parity",status="RUNTIME_CALLABLE_ENTRY_AND_SHARED_BODY_CONFIRMED",clobbers=["D0","A4","CCR"],preserves_by_examined_body=["A6","D5","D6"],stack="No live SP assertion; BSR/RTS control flow verified"),
 call_chain=[dict(site=0x2c584,target=0x3797e,status="STATIC_JSR_WITH_RUNTIME_POSTCALL_RETURN"),dict(site=0x379b4,target=0x37a46,status="RUNTIME_CALL_AND_RETURN_PROVEN"),dict(site=0x37a46,target=0x37a82,status="RUNTIME_HELPER_CALL_AND_RETURN_PROVEN"),dict(site=0x2c58c,target=0x37ad2,status="STATIC_SUCCESS_ONLY_NOT_OBSERVED")],
 result_use=dict(caller_branch_pc=0x379b8,condition="BNE tests Z flag from MOVEQ0/MOVEQ1 return",success_destination=0x37a3e,selector_field=0x21e,selector_value=0,outer_branch_pc=0x2c58a,apply_target=0x37ad2,apply_writes=[dict(offset=0x204,value=6,width=1),dict(offset=0x200,value=0,width=4)],dispatch=0x35a50,dispatch_mode6_target=0x35b2a,evidence="BYTE_VERIFIED_STATIC_SUCCESS_DATAFLOW; runtime observed false returns only",named_mechanic="UNRESOLVED"),
 branch_evidence=dict(far_path=pcs(far),close_early_reject_path=pcs(near),far_trace_sha256=h(far.encode()),close_trace_sha256=h(near.encode()),near_gate="Complete trials observed distance<48 with opponent+A9=0; no 037A64 breakpoint hit",success_conditions="Receiver word+4==0200 and state+6 not06/0A/0E/10; grounded opponent+31==0; distance<48; opponent+A9!=0; opponent word+4==0200; animation+8 longword!=0"),
 move_observation=dict(character="Ryu",label="standing Button1 punch",strength_label="UNVERIFIED",frame_done_interval=3349,animation_cell=correlated["p1"]["animation"],state4=correlated["p1"]["state4"],state6=correlated["p1"]["state6"],a9=correlated["p1"]["a9"],animation8=correlated["p1"]["animation8"],confidence="INPUT_VISUAL_AND_SAME_INTERVAL_RAM_CORRELATION_NOT_GLOBAL_MOVE_MAP"),
 visual_evidence=pictures,
 limits=["Successful returnD0=1, selector0 store and application behavior not observed; no named defensive mechanic proved","First prototype reached its600-event cap; only complete controlled/crouch trials eligible for new operand ingestion","Input and visual pose association does not establish an entire animation family or move-strength mapping","The unchanged V03 consumer blocks and helper share return code; ownership remains nonexclusive","Static21E readers/dispatch do not establish a runtime successful reaction","No gameplay patches or community hitbox-fix claim"],
 next_target="Find a natural gameplay state combining opponent+A9!=0 with receiver eligibility before hit reaction/airborne rejection; then follow selector0 through37AD2/35B2A to its actual action.",
 free_bytes=shutil.disk_usage(R).free)
 (R/"evidence/collision_decisions_v04.json").write_text(json.dumps(report,indent=2))
 print(json.dumps(dict(status="PASS_FOR_BOUNDED_RESULTS",decision=report["decision"],trial_events=[x["events"] for x in trials],near_values=[[x["value"] for x in t["near_reads"]] for t in trials],parity=parity,move=report["move_observation"],free=report["free_bytes"]),indent=2))
if __name__=="__main__":main()
