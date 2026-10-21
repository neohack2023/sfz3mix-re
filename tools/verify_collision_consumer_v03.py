"""Verify saved state observations, exact consumer parity and bounded branch proof."""
import csv,hashlib,json,subprocess,shutil
from pathlib import Path
from bounded_m68k_export_v01 import fixture,decode
R=Path(r"D:\AIOS_SFZ3MIX_V032")
SHA="b5f7a1598e4f91a5113c506505b482b2cd1a19e366fe31471740e45dbd204691"
def h(x):return hashlib.sha256(x).hexdigest()
def s16(x):return (x+0x8000)%0x10000-0x8000
def main():
 rom=(R/"tools/sz3mx.03").read_bytes();assert h(rom)==SHA
 fixtures=fixture()
 oldfile=R/"evidence/collision_engine_v02.tsv";assert h(oldfile.read_bytes())=="e02c8ab5a5ceb3edcc9fdff2f159ff0ae81c806359907323d7cbf4846bc8f0bf"
 old=list(csv.DictReader([x for x in oldfile.read_text().splitlines() if not x.startswith("#")],delimiter="\t"));assert len(old)==180
 path=R/"evidence/collision_scenarios_v03.jsonl";events=[json.loads(x) for x in path.read_text().splitlines()]
 assert len(events)==226 and events[-1]["type"]=="COMPLETE" and path.stat().st_size<900000
 launch=json.loads((R/"evidence/collision_scenarios_v03_launch.json").read_text());assert launch["exit_code"]==0 and not launch["stderr"]
 cpu=[x for x in events if x["type"]=="CPU"];reads=[x for x in cpu if x["kind"]=="READ"];writes=[x for x in cpu if x["kind"]=="WRITE"]
 assert len(reads)==147 and reads[0]["pc"]==0x37a56 and reads[0]["data"]==273 and reads[0]["ir"]==int.from_bytes(rom[0x37a56:0x37a58],"big")
 arith=[]
 for x in writes:
  a=x["p1"] if x["address"]==0xff861c else x["p2"];b=x["p2"] if a["base"]==0xff8400 else x["p1"]
  sel=b["selectors"]&255;d0=d1=0
  if a["active"]:
   if sel:
    record=b["pointer9c"]+sel*8;d0=int.from_bytes(rom[record:record+2],"big");d1=-int.from_bytes(rom[record+4:record+6],"big")
    if a["orientation"]^1:d0=-d0;d1=-d1
   d0=(d0+d1+b["x"])&0xffff;expected=abs(s16(a["x"]-d0))&0xffff
  else:expected=0
  assert expected==x["data"],(x,expected)
  arith.append(dict(frame=x["frame"],phase=x["phase"],receiver=a["base"],old_value=a["edge"],new_value=x["data"],receiver_x=a["x"],opponent_x=b["x"],selector=sel,animation=a["animation"],state4=a["state4"]))
 first_old=[(int(x["address"],16),int(x["data"],16)) for x in old if x["kind"]=="WRITE"][:8]
 first_new=[(x["address"],x["data"]) for x in writes if x["phase"]=="BASELINE"]
 assert first_old==first_new
 phases=[]
 for p in ["BASELINE","APPROACH","ATTACK","RETREAT","RELEASE"]:
  xs=[x for x in events if x["phase"]==p];start=next(x for x in xs if x["type"]=="PHASE")
  phases.append(dict(phase=p,start_frame=start["frame"],sampled_last_frame=xs[-1]["frame"],p1_x_range=[min(x["p1"]["x"] for x in xs),max(x["p1"]["x"] for x in xs)],p2_x_range=[min(x["p2"]["x"] for x in xs),max(x["p2"]["x"] for x in xs)],p1_edge_range=[min(x["p1"]["edge"] for x in xs),max(x["p1"]["edge"] for x in xs)],p1_state4=sorted(set(x["p1"]["state4"] for x in xs)),p1_animations=sorted(set(x["p1"]["animation"] for x in xs)),reads=sum(x.get("kind")=="READ" for x in xs)))
 base="/mnt/d/AIOS_SFZ3MIX_V032";name="collision_consumer_037a56_v03"
 cmd=f"set -e; export LD_LIBRARY_PATH={base}/tools/.m68k_toolchain/usr/lib/x86_64-linux-gnu; {base}/tools/.m68k_toolchain/usr/bin/m68k-linux-gnu-as -m68000 -o {base}/evidence/{name}.o {base}/tools/{name}.s; {base}/tools/.m68k_toolchain/usr/bin/m68k-linux-gnu-objcopy -O binary -j .text {base}/evidence/{name}.o {base}/evidence/{name}.bin"
 run=subprocess.run(["wsl.exe","bash","-c",cmd],capture_output=True,text=True,timeout=30);assert run.returncode==0,(run.stdout,run.stderr)
 actual=(R/f"evidence/{name}.bin").read_bytes();expected=rom[0x37a56:0x37a82]
 mismatch=[0x37a56+i for i in range(max(len(actual),len(expected))) if actual[i:i+1]!=expected[i:i+1]]
 assert not mismatch,mismatch
 cf=json.loads((R/"evidence/collision_scenarios_cf_v03_launch.json").read_text());assert cf["exit_code"]==0 and not cf["stderr"]
 trace=(R/"evidence/consumer_cf_v03_far.txt").read_text();pcs=[int(x.split(":")[0],16) for x in trace.splitlines()]
 assert pcs==[0x37a5c,0x37a7a,0x37a7c]
 console=(R/"evidence/consumer_cf_v03_console.txt").read_text();assert "PREDICATE_RETURN pc=37A7C d0=0" in console
 instructions=decode(rom,0x37a56,44)
 # Registry omits original machine-code bytes; keep those only in local export.
 for x in instructions:x.pop("opcode")
 site_summary=[]
 for pc in sorted(set(x["pc"] for x in reads)):
  xs=[x for x in reads if x["pc"]==pc]
  site_summary.append(dict(pc=pc,count=len(xs),values=sorted(set(x["data"] for x in xs)),phases=sorted(set(x["phase"] for x in xs)),function_id=None))
 oldwrites=[dict(frame=int(x["frame"]),receiver=int(x["address"],16)-0x21c,new_value=int(x["data"],16),computed_opponent_edge=int(x["d0"],16)) for x in old if x["kind"]=="WRITE"]
 report=dict(schema="sfz3mix.collision_consumer.v03",preflight="READY_CONTINUE",rom_sha256=SHA,exporter_fixture=fixtures,
 old_observations=dict(rows=180,writes=oldwrites,p1_values=[x["new_value"] for x in oldwrites if x["receiver"]==0xff8400],p2_values=[x["new_value"] for x in oldwrites if x["receiver"]==0xff8800],state_limit="No original state/animation/input snapshots; no precise named attack state recoverable",baseline_reproduction="First eight game-originated writes reproduced exactly with added state/coordinate snapshots"),
 scenarios=dict(events=len(events),cpu_reads=len(reads),cpu_writes=len(writes),bytes=path.stat().st_size,phase_summary=phases,write_arithmetic_checks=len(arith),write_transitions=arith,read_sites=site_summary,trace_sha256=h(path.read_bytes())),
 consumer=dict(region_id="REGION_037A56",start=0x37a56,end_exclusive=0x37a82,function_id=None,entry_status="RUNTIME_READER_ANCHORED_REGION_NOT_VERIFIED_FUNCTION_ENTRY",first_read=dict(frame=reads[0]["frame"],phase=reads[0]["phase"],pc=reads[0]["pc"],receiver=reads[0]["a6"],address=reads[0]["address"],value=reads[0]["data"],width_bytes=2,ir=reads[0]["ir"]),instructions=instructions,
 semantics="Unsigned distance >=48 returns D0=0. Otherwise require opponent+A9 nonzero, opponent+4==0200, and opponent animation+8 longword nonzero to return D0=1. A4 must be the opponent on entry; broader caller purpose unresolved.",
 branch_runtime=dict(path=pcs,result_d0=0,near_path_observed=False,trace_sha256=h(trace.encode())),parity=dict(source=f"tools/{name}.s",source_sha256=h((R/f"tools/{name}.s").read_bytes()),size=len(actual),expected_sha256=h(expected),assembled_sha256=h(actual),mismatch_addresses=mismatch,decision="PASS")),
 evidence=dict(original_observations_sha256=h(oldfile.read_bytes()),original_scenario_path=str(path),control_trace_path=str(R/"evidence/consumer_cf_v03_far.txt")),
 limits=["Input phases are controlled attempts, not validated animation-name classifications","Observer snapshots are not CPU reads; write snapshots precede the game write","IR matched first consumer opcode; IR at other bus callbacks may be prefetched and must not be treated as their opcode","Close-case input phase reached edge24 but first predicate's near-return path was not observed","All ten consumer-site containing function owners remain null","No physical pushbox correction or hitbox restoration cause established","Static pattern matches include false positives and are not promoted","All V01/V02 sources and SQLite rows retained; no extra large exports"],
 final_free_bytes=shutil.disk_usage(R).free)
 (R/"evidence/collision_consumer_v03.json").write_text(json.dumps(report,indent=2))
 print(json.dumps(dict(status="PASS",phases=phases,consumer=report["consumer"],cpu_reads=len(reads),cpu_writes=len(writes),free=report["final_free_bytes"]),indent=2))
if __name__=="__main__":main()
