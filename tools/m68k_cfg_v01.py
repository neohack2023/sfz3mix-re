#!/usr/bin/env python3
"""Instruction-aware bounded Motorola 68000 CFG discovery for SFZ3 Mix v0.32.

Conservative static candidates, NOT proof of runtime execution or opcode decrypt parity.
Authoritative source is local original ZIP; never writes ROM members.
"""
import argparse
from collections import Counter, deque
import hashlib
import json
from pathlib import Path
import re
import sys
from zipfile import ZipFile

VENDOR=Path(__file__).resolve().parent/".vendor"
sys.path.insert(0,str(VENDOR))
from capstone import Cs,CS_ARCH_M68K,CS_MODE_M68K_000,CS_MODE_BIG_ENDIAN
SHA="867b8356872a034ec7e06f776bf757ec2095fee7616931b71f720f30369806ab"
DIRECT_RE=re.compile(r"\$([0-9a-f]+)\s*$",re.IGNORECASE)
END={"rts","rte","rtr","stop","illegal","reset"}
TRAP={"trap","trapv"}
# Earlier HBMAME debugger disassembly at these addresses supports decoding consistency.
OBSERVED_SEEDS={0x00331C:"prior_hbmame_debug_disassembly",0x025C40:"prior_hbmame_debug_disassembly",0x025CC0:"prior_hbmame_debug_disassembly",0x026438:"prior_hbmame_debug_disassembly"}

def sha(data):return hashlib.sha256(data).hexdigest()

def discover(rom,max_insns=25000,max_per_block=1024):
    cs=Cs(CS_ARCH_M68K, CS_MODE_M68K_000|CS_MODE_BIG_ENDIAN)
    cs.detail=True
    seeds={int.from_bytes(rom[4:8],"big"):"reset_pc_structural"}
    # Use only first 32 M68K vector longwords as conservative startup seeds.
    # Later bytes include instruction-like content; reject blanket vector classification.
    for i in range(2,32):
        a=int.from_bytes(rom[4*i:4*i+4],"big")
        if a >= 0x80 and a<len(rom) and a%2==0:
            seeds.setdefault(a,"vector_longword_candidate")
    seeds.update(OBSERVED_SEEDS)
    queue=deque((a,None,"seed") for a in sorted(seeds) if 0<=a<len(rom) and a%2==0)
    instructions={}
    used_bytes={}
    edges=[]
    rejected=[]
    candidates=dict((f"{a:06X}",{"entry":f"{a:06X}","reason":name}) for a,name in seeds.items())
    functions_from_calls=set()
    max_queue=90000
    processed=0
    while queue and len(instructions)<max_insns and processed<max_queue:
        start,source,edge_type=queue.popleft()
        processed+=1
        if start<0 or start>=len(rom) or start%2:continue
        pc=start
        count=0
        while count<max_per_block and len(instructions)<max_insns:
            if pc in instructions:break
            if pc<0 or pc>=len(rom)-1 or pc%2:break
            if pc in used_bytes:
                rejected.append({"address":f"{pc:06X}","reason":"overlap_into_existing_instruction"})
                break
            # Repeated zeroes / FF are deliberately NOT interpreted as infinite instructions.
            if len(rom)-pc >= 32 and (rom[pc:pc+32] == b"\0"*32 or rom[pc:pc+32] == b"\xff"*32):
                rejected.append({"address":f"{pc:06X}","reason":"repeated_padding_candidate"})
                break
            decoded=list(cs.disasm(rom[pc:pc+22],pc,count=1))
            if not decoded:
                rejected.append({"address":f"{pc:06X}","reason":"decoder_stopped"})
                break
            op=decoded[0]
            if op.size==0 or pc+op.size>len(rom):
                rejected.append({"address":f"{pc:06X}","reason":"invalid_instruction_length"})
                break
            if any(x in used_bytes for x in range(pc,pc+op.size)):
                rejected.append({"address":f"{pc:06X}","reason":"instruction_overlaps_prior"})
                break
            for x in range(pc,pc+op.size):used_bytes[x]=pc
            inst={"address":f"{pc:06X}","size":op.size,"bytes":op.bytes.hex(),
                  "mnemonic":op.mnemonic,"operands":op.op_str,"status":"static_code_candidate"}
            instructions[pc]=inst
            count+=1
            m=op.mnemonic.lower().split(".")[0]
            nxt=pc+op.size
            if m in END or m in TRAP:break
            is_branch=(m in {"bra","bsr","bhi","bls","bcc","bcs","bne","beq",
                           "bvc","bvs","bpl","bmi","bge","blt","bgt","ble",
                           "jmp","jsr"} or m.startswith("db"))
            if is_branch:
                match=DIRECT_RE.search(op.op_str)
                target=int(match.group(1),16) if match else None
                t_valid=target is not None and 0<=target<len(rom) and target%2==0
                is_call=m.startswith("bsr") or m=="jsr"
                unconditional=m.startswith("bra") or m=="jmp"
                if t_valid:
                    edges.append({"from":f"{pc:06X}","to":f"{target:06X}",
                                  "kind":"call" if is_call else "branch"})
                    queue.append((target,pc,"call" if is_call else "branch"))
                    if is_call:
                        functions_from_calls.add(target)
                        candidates.setdefault(f"{target:06X}",{"entry":f"{target:06X}",
                            "reason":"static_direct_call_target"})
                else:
                    edges.append({"from":f"{pc:06X}","to":None,
                                  "kind":"indirect_or_unresolved_control_flow",
                                  "instruction":m,"operands":op.op_str})
                if not unconditional:
                    edges.append({"from":f"{pc:06X}","to":f"{nxt:06X}",
                                  "kind":"fallthrough"})
                    queue.append((nxt,pc,"fallthrough"))
                break
            pc=nxt
        if count==max_per_block:
            rejected.append({"address":f"{start:06X}","reason":"block_budget_reached"})
    page_counts=Counter((addr//4096) for addr in used_bytes)
    pages=[]
    for page in range((len(rom)+4095)//4096):
        block=rom[page*4096:(page+1)*4096]
        count=page_counts[page]
        if count:
            label="candidate_code_mixed_or_overlapping_data"
        elif block==bytes([block[0]])*len(block):
            label="uniform_padding_candidate"
        else:
            label="unresolved_not_proven_data"
        pages.append({"index":page,"file_offset":page*4096,"candidate_code_bytes":count,
                      "label":label})
    summary={"cpu_bytes":len(rom),"static_candidate_instruction_count":len(instructions),
             "static_candidate_code_bytes":len(used_bytes),
             "candidate_code_fraction_pct":round(100*len(used_bytes)/len(rom),3),
             "other_bytes_not_verified_as_code":len(rom)-len(used_bytes),
             "direct_calls_found":sum(e["kind"]=="call" for e in edges),
             "candidate_function_entry_count":len(candidates),
             "control_flow_edges":len(edges),"rejected_walk_events":len(rejected),
             "queue_entries_remaining":len(queue),"instruction_budget":max_insns,
             "budget_hit":len(instructions)>=max_insns or processed>=max_queue,
             "classification_semantics":"static candidates, not proof of code/data or executed instructions"}
    return {"schema":"sfz3mix.m68k_cfg.v01","source_archive_sha256":SHA,
            "cpu_sha256":sha(rom),"decoder":"Capstone M68K 68000 big endian 5.0.6",
            "limitations":["CPU opcode path may differ from data read path; compare HBMAME instruction decode",
                           "CFG is conservative, bounded and does not resolve indirect control flow",
                           "Unvisited bytes remain unresolved, not assumed data",
                           "Function entry labels are leads; no validated function boundaries"],
            "summary":summary,"function_entry_candidates":sorted(candidates.values(),key=lambda e:e["entry"]),
            "edges":edges,"rejected":rejected[:800],
            "page_labels":pages,"instructions":[instructions[k] for k in sorted(instructions)]}

def write_snippets(report, output):
    insns={int(i["address"],16):i for i in report["instructions"]}
    addresses=[0x000976,0x0000C0,0x00331C,0x025C40,0x026438]
    lines=["; SFZ3 Mix v0.32 — diagnostic instruction-aware snippets",
           "; Machine words are byte-exact original data, annotated with Capstone mnemonics.",
           "; Do NOT treat comments as assembler instructions or this listing as a full reassembly.",""]
    for start in addresses:
        lines.append(f"; --- candidate entry {start:06X} ---")
        pc=start
        for _ in range(16):
            inst=insns.get(pc)
            if not inst:break
            lines.append(f"; {pc:06X}: {inst['mnemonic']} {inst['operands']}")
            words=[inst["bytes"][i:i+4] for i in range(0,len(inst["bytes"]),4)]
            for word in words:
                if len(word)==4:lines.append(f"    .word 0x{word}")
                else: lines.append(f"    .byte 0x{word}")
            pc+=inst["size"]
        lines.append("")
    output.write_text("\n".join(lines)+"\n",encoding="utf-8")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--archive",type=Path,required=True)
    p.add_argument("--report",type=Path,required=True)
    p.add_argument("--asm-snippets",type=Path,required=True)
    p.add_argument("--max-insns",type=int,default=25000)
    a=p.parse_args()
    if a.report.exists() or a.asm_snippets.exists():raise FileExistsError("Refuse overwriting prior receipt")
    if sha(a.archive.read_bytes())!=SHA:raise ValueError("Archive SHA mismatch")
    with ZipFile(a.archive) as z:rom=z.read("sz3mx.03")
    report=discover(rom,a.max_insns)
    a.report.write_text(json.dumps(report,separators=(",",":"))+"\n",encoding="utf-8")
    write_snippets(report,a.asm_snippets)
    print(json.dumps(report["summary"],indent=2))

if __name__=="__main__":main()
