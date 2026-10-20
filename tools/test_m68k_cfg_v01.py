#!/usr/bin/env python3
"""Unit test for 68000 CFG: explicit direct call, conditional branch and two returns."""
from m68k_cfg_v01 import discover
raw=bytearray(1024)
raw[4:8]=(0x200).to_bytes(4,"big")
raw[0x200:0x20A]=bytes.fromhex("6100000667024e754e75")
graph=discover(bytes(raw),100)
ins={int(x["address"],16) for x in graph["instructions"]}
assert {0x200,0x204,0x206,0x208} <= ins, [hex(x) for x in sorted(ins)]
edges={(int(e["from"],16),int(e["to"],16),e["kind"]) for e in graph["edges"] if e["to"]}
assert (0x200,0x208,"call") in edges,edges
assert (0x200,0x204,"fallthrough") in edges,edges
assert (0x204,0x208,"branch") in edges,edges
assert (0x204,0x206,"fallthrough") in edges,edges
assert "000208" in {x["entry"] for x in graph["function_entry_candidates"]}
print("SELFTEST_PASS: BSR, BEQ, call target, both fallthrough paths, RTS, entries")
