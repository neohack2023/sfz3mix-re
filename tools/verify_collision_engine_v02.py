"""Bounded V02 evidence validation and source-authored GNU assembly parity."""
import csv,hashlib,json,re,subprocess,shutil
from pathlib import Path
ROOT=Path(r"D:\AIOS_SFZ3MIX_V032")
SHA="b5f7a1598e4f91a5113c506505b482b2cd1a19e366fe31471740e45dbd204691"
def h(x):return hashlib.sha256(x).hexdigest()
def main():
 rom=(ROOT/"tools/sz3mx.03").read_bytes();assert h(rom)==SHA
 assert h((ROOT/"tools/collision_leaf_02c19a_v01.s").read_bytes())=="c9e9bd5c0526032a8eec09d5e93bca0a533a07be2e64815229bbd02f0c0b0c90"
 launch=json.loads((ROOT/"evidence/collision_engine_v02_launch.json").read_text())
 assert launch["exit_code"]==0 and not launch["stderr_tail"] and "ENGINE_V02_COMPLETE samples=180" in launch["stdout_tail"]
 tsv=ROOT/"evidence/collision_engine_v02.tsv";txt=tsv.read_text()
 assert "# COMPLETE frames=2939..2946 samples=180" in txt
 rows=list(csv.DictReader([x for x in txt.splitlines() if not x.startswith("#")],delimiter="\t"))
 assert len(rows)==180
 decoded={}
 for tag,limit in [("02c070",0x2c090),("02c17e",0x2c1e2),("029a10",0x29ab6),("027eda",0x27efc),("02f666",0x2f68a)]:
  for line in (ROOT/f"evidence/collision_engine_v02_{tag}.txt").open():
   m=re.match(r"([0-9A-F]+): ((?:[0-9A-F]{4} +)+)(.*)",line);assert m,line
   a=int(m[1],16)
   if a>=limit:break
   raw=bytes.fromhex(m[2]);assert rom[a:a+len(raw)]==raw,(tag,hex(a),raw.hex(),rom[a:a+len(raw)].hex(),line)
   decoded[a]=dict(pc=a,size=len(raw),instruction=m[3].strip())
 for row in rows:
  pc=int(row["pc"],16);assert pc in decoded
  assert row["kind"] in ("READ","WRITE") and int(row["mask"],16) in (0xffff,0xff,0xff00)
  a=int(row["address"],16)
  if a<len(rom):
   assert row["kind"]=="READ" and int.from_bytes(rom[a:a+2],"big")==int(row["data"],16)
 trace=(ROOT/"evidence/collision_engine_v02_trace.txt").read_text()
 pcs=[int(x.split(":")[0],16) for x in trace.splitlines() if re.match(r"^[0-9A-F]{6}:",x)]
 assert pcs[0]==0x2c17e and pcs[-1]==0x2c082 and pcs.count(0x2c19a)==4 and pcs.count(0x2c1e0)==4
 assert [x for x in pcs if x in (0x2c186,0x2c18e,0x2c196)]==[0x2c186,0x2c18e,0x2c196]
 console=(ROOT/"evidence/collision_engine_v02_console.txt").read_text()
 for token in ["WRAP_CALL pc=2C07E","WRAP_RETURN pc=2C082","a6=FF8C00","a6=FF9000"]:assert token in console
 accesses=[x for x in rows if int(x["address"],16) in (0xff861c,0xff8a1c)]
 assert accesses and not [x for x in accesses if x["kind"]=="READ"]
 parity=[]
 for name,start,end in [("collision_wrapper_02c17e_v02",0x2c17e,0x2c19a),("collision_dual_records_029a42_v02",0x29a42,0x29a66),("collision_selectors_02f666_v02",0x2f666,0x2f68c)]:
  base="/mnt/d/AIOS_SFZ3MIX_V032"
  cmd=f'set -e; export LD_LIBRARY_PATH={base}/tools/.m68k_toolchain/usr/lib/x86_64-linux-gnu; {base}/tools/.m68k_toolchain/usr/bin/m68k-linux-gnu-as -m68000 -o {base}/evidence/{name}.o {base}/tools/{name}.s; {base}/tools/.m68k_toolchain/usr/bin/m68k-linux-gnu-objcopy -O binary -j .text {base}/evidence/{name}.o {base}/evidence/{name}.bin'
  p=subprocess.run(["wsl.exe","bash","-c",cmd],capture_output=True,text=True,timeout=30);assert p.returncode==0,(p.stdout,p.stderr)
  actual=(ROOT/f"evidence/{name}.bin").read_bytes();expected=rom[start:end]
  mismatches=[start+i for i in range(max(len(expected),len(actual))) if expected[i:i+1]!=actual[i:i+1]]
  rec=dict(source=f"tools/{name}.s",start=start,end_exclusive=end,source_sha256=h((ROOT/f"tools/{name}.s").read_bytes()),expected_sha256=h(expected),assembled_sha256=h(actual),size=len(actual),mismatch_addresses=mismatches,decision="PASS" if not mismatches else "FAIL")
  parity.append(rec)
  assert not mismatches,rec
 sites=[]
 descriptions={
  0x29a10:(0x29a10,0x29a18,"+CB selector of A6; zero exits to 029B3E"),
  0x29a1a:(0x29a18,0x29a22,"+CB selector of A4; zero exits to 029B3E"),
  0x29a42:(0x29a42,0x29a6a,"A6+9C pointer; D0<<3; vertical record+2 read"),
  0x29a46:(0x29a42,0x29a6a,"A4+9C pointer; D1<<3; vertical record+2 read"),
  0x27eda:(0x27eda,0x27ee4,"A1+C8 longword -> A5-5CD6; zero branch 027FDA"),
  0x27ef0:(0x27eea,0x27efc,"A1+90 + selector*8 -> A2; direct BSR 0296A6; caller ownership unresolved"),
  0x2f666:(0x2f666,0x2f68c,"longword source(A0) -> A6+C8..CB; selector writer")}
 for pc,(start,end,meaning) in descriptions.items():
  sites.append(dict(pc=pc,region_start=start,region_end_exclusive=end,function_id=None,ownership="UNRESOLVED",confidence="RUNTIME_INSTRUCTION_PROVEN_BLOCK_STATIC",meaning=meaning,instructions=[decoded[a] for a in sorted(decoded) if start<=a<end],runtime_reobserved=any(int(x["pc"],16)==pc for x in rows)))
 table_reads=[]
 for x in rows:
  a=int(x["address"],16)
  if a in (0xd65d2,0xd65d6,0xf2ae4,0xf2ae8):
   key=(int(x["pc"],16),a,int(x["data"],16))
   if key not in table_reads:table_reads.append(key)
 report=dict(schema="sfz3mix.collision_engine_recovery.v02",source_rom_sha256=SHA,preflight="READY_CONTINUE",
 wrapper=dict(id="FUNC_REC_02C17E",entry=0x2c17e,prefix_end=0x2c19a,end_exclusive=0x2c1e2,classification="RUNTIME_CALLABLE_WRAPPER_WITH_SHARED_LEAF_TAIL",incoming_call_site=0x2c07e,caller_function_id=None,return_pc=0x2c082,subcalls=[0x2c182,0x2c18a,0x2c192],shared_function_id="FUNC_REC_02C19A",runtime_receiver_slots=[0xff8400,0xff8800,0xff8c00,0xff9000],shared_blocks="all seven existing FUNC_REC_02C19A blocks",stack="BSR/RTS architectural -4/+4; debugger SP snapshots unchanged and excluded from stack ABI proof",clobbers=["A6","A0","A4","D0","D1","D2 low byte","CCR"],preserves_by_body=["A5"],instruction_trace_count=len(pcs)),
 capture=dict(rows=len(rows),frames=[2939,2946],phase="EXISTING_DETERMINISTIC_GAMEPLAY_INPUTS",cap=512,field_21c_writes=len(accesses),field_21c_reads=0,decision="BOUNDED_NEGATIVE_CONSUMER_RESULT",trace_sha256=h(tsv.read_bytes()),instruction_trace_sha256=h(trace.encode()),launch_elapsed_seconds=launch["elapsed"]),
 record_reads=[dict(pc=p,address=a,value=d,kind="READ",width=2,record=a-(2 if a in (0xd65d2,0xf2ae4) else 6),offset=2 if a in (0xd65d2,0xf2ae4) else 6) for p,a,d in table_reads],
 reader_sites=sites,assembly=parity,
 wrapper_instructions=[decoded[a] for a in sorted(decoded) if 0x2c17e<=a<0x2c19a],
 limits=["Debugger disassembly length A6 initially resolved as register; oversized local export preserved; verifier stops at explicit range; probe fixed to 0x numeric expressions","All external/indirect entries not enumerated","No +21C read observed in eight frames; consumer purpose unresolved","Two-player vertical non-overlap checks observed; horizontal overlap/correction path not runtime established","Inactive receiver slots exercised; zero selector not observed","No gameplay modification; hitboxes issue remains open","Frame_done interval numbering retained; two logical updates can occur in an interval","Bus longwords logged as two 16-bit transfers; byte masks retain lane identity"],
 next_target="Locate a scenario/static candidate reading +21C; establish callable entry for 029A10 chain and observe overlap-positive path",
 final_free_bytes=shutil.disk_usage(ROOT).free)
 (ROOT/"evidence/collision_engine_recovery_v02.json").write_text(json.dumps(report,indent=2))
 print(json.dumps(report,indent=2))
if __name__=="__main__":main()
