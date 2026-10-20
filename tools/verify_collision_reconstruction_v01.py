"""Validate a source-authored bounded callable region; emit no ROM bytes."""
import csv, hashlib, json, re, sqlite3
from pathlib import Path
ROOT=Path(r"D:\AIOS_SFZ3MIX_V032")
ENTRY,END=0x2c19a,0x2c1e2
SHA="b5f7a1598e4f91a5113c506505b482b2cd1a19e366fe31471740e45dbd204691"
def digest(data):return hashlib.sha256(data).hexdigest()
def compare(expected,actual,start):
    return [start+i for i in range(max(len(expected),len(actual))) if expected[i:i+1]!=actual[i:i+1]]
def main():
    assert compare(b"abc",b"axc",0x100)==[0x101]
    assert compare(b"ab",b"abc",0x100)==[0x102]
    rom=(ROOT/"tools/sz3mx.03").read_bytes();assert digest(rom)==SHA
    expected=rom[ENTRY:END];actual=(ROOT/"evidence/collision_leaf_02c19a_v01.bin").read_bytes()
    mismatch=compare(expected,actual,ENTRY)
    parity={"schema":"sfz3mix.assembly_parity.v01","cpu_start":ENTRY,"cpu_end_exclusive":END,
      "source_rom_sha256":SHA,"assembly_source":"tools/collision_leaf_02c19a_v01.s",
      "assembler":"GNU m68k-linux-gnu-as 2.38 -m68000",
      "source_assembly_sha256":digest((ROOT/"tools/collision_leaf_02c19a_v01.s").read_bytes()),
      "expected_size":len(expected),"assembled_size":len(actual),"expected_original_bytes_sha256":digest(expected),
      "assembled_bytes_sha256":digest(actual),"mismatch_cpu_addresses":mismatch,"decision":"PASS" if not mismatch else "FAIL"}
    (ROOT/"evidence/collision_assembly_parity_v01.json").write_text(json.dumps(parity,indent=2))
    assert not mismatch,parity
    launch=json.loads((ROOT/"evidence/collision_recovery_launch_v02.json").read_text())
    assert launch["exit_code"]==0 and not launch["stderr_tail"]
    tsv=ROOT/"evidence/collision_recovery_v02.tsv";text=tsv.read_text()
    rows=list(csv.DictReader([l for l in text.splitlines() if not l.startswith("#")],delimiter="\t"))
    assert len(rows)==44 and "# COMPLETE frame=2940 samples=44" in text
    old=ROOT/"evidence/collision_access_v01.tsv"
    assert digest(old.read_bytes())=="4c099e68554cc200d265b6ea4d108e23136a38f6df6b61577384655917b5762f"
    decoded=[]
    for line in (ROOT/"evidence/collision_recovery_disasm_v02.txt").read_text().splitlines():
        m=re.match(r"([0-9A-F]+): ((?:[0-9A-F]{4} )+)(.*)",line)
        assert m,line
        pc=int(m[1],16);raw=bytes.fromhex(m[2]);assert rom[pc:pc+len(raw)]==raw
        decoded.append({"pc":pc,"size":len(raw),"instruction":m[3].strip()})
    ins=[x for x in decoded if ENTRY<=x["pc"]<END]
    assert sum(x["size"] for x in ins)==72 and ins[-1]["instruction"]=="rts"
    bypc={x["pc"]:x for x in ins}
    pcs=[int(m[1],16) for m in re.finditer(r"(?m)^([0-9A-F]{6}):",(ROOT/"evidence/collision_recovery_trace_v02.txt").read_text())]
    assert pcs[0]==ENTRY+2 and pcs[-1]==0x2c1e0
    runtime_edges=set(zip([ENTRY]+pcs,pcs))
    leaders={ENTRY};edges=[]
    for item in ins:
        pc=item["pc"];fall=pc+item["size"];mn=item["instruction"].split()[0]
        if mn in ("beq","bpl"):
            target=int(re.search(r"\$([0-9a-f]+)",item["instruction"])[1],16)
            assert target in bypc and fall in bypc
            leaders.update((target,fall))
            edges.extend([{"source":pc,"target":target,"kind":"conditional_taken","runtime_observed":(pc,target) in runtime_edges},
                          {"source":pc,"target":fall,"kind":"conditional_fallthrough","runtime_observed":(pc,fall) in runtime_edges}])
        elif mn!="rts":edges.append({"source":pc,"target":fall,"kind":"fallthrough","runtime_observed":(pc,fall) in runtime_edges})
    assert all((a,b) in {(e["source"],e["target"]) for e in edges} for a,b in runtime_edges)
    starts=sorted(leaders);blocks=[]
    for n,start in enumerate(starts):
        end=starts[n+1] if n+1<len(starts) else END
        blocks.append({"id":f"BB_{start:06X}","start":start,"end_exclusive":end,
          "instruction_addresses":[i["pc"] for i in ins if start<=i["pc"]<end]})
    console=(ROOT/"evidence/collision_recovery_console_v02.txt").read_text()
    assert "REC_ENTRY pc=2C19A" in console and "REC_RTS pc=2C1E0" in console and "REC_RETURN pc=2C186" in console
    groups=[];group=None
    for row in rows:
        pc=int(row["pc"],16)
        if pc==0x2c19c:
            if group:groups.append(group)
            group=[]
        assert group is not None;group.append(row)
    if group:groups.append(group)
    records=[];checks=[]
    for group in groups:
        def at(pc):return [r for r in group if int(r["pc"],16)==pc]
        receiver=int(group[0]["a6"],16)&0xffffff
        other=int(at(0x2c1ac)[0]["a4"],16)&0xffffff
        ptrrows=at(0x2c1ac);assert len(ptrrows)==2
        pointer=(int(ptrrows[0]["data"],16)<<16)|int(ptrrows[1]["data"],16)
        selector=int(at(0x2c1a6)[0]["data"],16)&0xff
        record=pointer+selector*8
        radiusrow=at(0x2c1b6)[0];xrow=at(0x2c1bc)[0]
        assert int(radiusrow["a0"],16)==record and int(radiusrow["address"],16)==record+4
        assert int(xrow["address"],16)==record
        radius=int(radiusrow["data"],16);x=int(xrow["data"],16);x=x if x<0x8000 else x-0x10000
        assert int.from_bytes(rom[record:record+2],"big",signed=True)==x
        assert int.from_bytes(rom[record+4:record+6],"big")==radius
        # Reproduce exact 16-bit arithmetic from observed path; not visual collision proof.
        orient=int(at(0x2c1be)[0]["data"],16)&0xff
        edge=x-radius if orient==1 else -x+radius
        otherx=int(at(0x2c1ce)[0]["data"],16);ownx=int(at(0x2c1d2)[0]["data"],16)
        delta=(ownx-(otherx+edge))&0xffff
        result=((-delta)&0xffff) if delta&0x8000 else delta
        write=at(0x2c1dc)[0]
        assert int(write["address"],16)==receiver+0x21c and int(write["data"],16)==result
        records.append({"receiver":receiver,"opponent":other,"pointer":pointer,"selector":selector,
          "record_address":record,"read_offsets":[0,4],"x_offset":x,"x_radius":radius,
          "index_status":"RUNTIME_POINTER_SELECTOR_RECORD_READ_CHAIN","width_bytes":8})
        checks.append({"receiver":receiver,"stored_distance":result,"arithmetic":"PASS"})
    con=sqlite3.connect((ROOT/"evidence/functions_v01.sqlite").as_uri()+"?mode=ro",uri=True)
    oldfn=con.execute("select id from functions where cpu_address=?",(ENTRY,)).fetchone()
    fid=oldfn[0] if oldfn else "FUNC_REC_02C19A"
    con.close()
    unique={r["record_address"]:r for r in records}
    result={"schema":"sfz3mix.collision_reconstruction.v01","function_id":fid,"cpu_entry":ENTRY,"cpu_end_exclusive":END,
      "source_rom_sha256":SHA,"name":"push_edge_distance_candidate","confidence":"HIGH_FOR_BOUNDED_CALLABLE_REGION",
      "status":"RUNTIME_CALLABLE_ENTRY_CFG_AND_ASSEMBLY_PARITY_VERIFIED",
      "bounds_basis":"direct BSR target + live entry, closed direct CFG to RTS, runtime return to 0x02C186; shared tail with wrapper at 0x02C17E",
      "ownership_limit":"entry-bounded region, not exclusive ownership; all external/indirect incoming paths not enumerated",
      "incoming_calls":[{"site":a,"target":ENTRY,"caller_id":None,"status":"STATIC_OPCODE_VERIFIED_RUNTIME_RETURN_CORROBORATED" if a==0x2c182 else "STATIC_OPCODE_VERIFIED"} for a in (0x2c182,0x2c18a,0x2c192)],
      "tail_fallthrough":{"source":0x2c196,"target":ENTRY,"status":"STATIC_OPCODE_VERIFIED"},
      "outgoing_calls":[],"instructions":ins,"blocks":blocks,"edges":edges,
      "runtime_visited_instruction_addresses":[ENTRY]+pcs,"runtime_access_rows":len(rows),
      "table_records":list(unique.values()),"arithmetic_checks":checks,"parity":parity,
      "calling_convention":{"input":["A6 receiver object"],"clobbers":["A0","A4","D0","D1","D2 low byte","CCR"],
        "preserved_by_body":["A5","A6"],"opponent":"sign-extended word at receiver+0x38; mask to 24-bit bus",
        "stack_caveat":"debugger SP/d@SP snapshots inconclusive; not used to prove return address or stack ABI"},
      "evidence":{"old_trace_sha256":digest(old.read_bytes()),"operand_trace_sha256":digest(tsv.read_bytes()),
         "instruction_trace_sha256":digest((ROOT/"evidence/collision_recovery_trace_v02.txt").read_bytes())},
      "issue":"hitboxes","issue_status":"INVESTIGATION_NOT_FIXED",
      "limitations":["Only active first-two-player examples tested; no projectile test","Unobserved branch paths statically byte-verified, not runtime-exercised","Higher gameplay/visual hitbox restoration semantics unproved","V01 operand callback lost rows due missing A7 state; preserved as failed instrumentation attempt"] }
    (ROOT/"evidence/collision_reconstruction_v01.json").write_text(json.dumps(result,indent=2))
    print(json.dumps({"status":"PASS","function_id":fid,"entry":hex(ENTRY),"end":hex(END),"instructions":len(ins),"blocks":len(blocks),"operand_rows":len(rows),"records":list(map(hex,unique)),"parity":parity,"arithmetic_checks":checks},indent=2))
if __name__=="__main__":main()
