# Collision consumer recovery V03

## Verified result
A real downstream CPU consumer of receiver+0x21C is now confirmed at **0x037A56**.
It compares the word with48 and returns D0=0 on the unsigned >=48 path.
This is a runtime-reader-anchored region, not a newly proven function entry.
[Machine-readable receipt](COLLISION_CONSUMER_V03.json), [editable assembly](../tools/collision_consumer_037a56_v03.s).

Canonical scope github:neohack2023/sfz3mix-re; existing Host02/workspace unchanged.
Canonical preflight returned READY_CONTINUE for accepted fixture, gameplay, verification, export and migration commands.
Source ROM SHA-256 before/after:
b5f7a1598e4f91a5113c506505b482b2cd1a19e366fe31471740e45dbd204691.
No ROM modification, ZIP extraction, clone or gameplay patch.

## What the existing180 observations actually establish
The retained V02 TSV contains20 output writes and160 operand reads across frame_done intervals2939..2946.
P1 output sequence: 173, 179, 186, 192, 199, 205, 211, 217, 223, 229.
P2 output sequence: 171, 177, 184, 190, 197, 203, 209, 215, 221, 227.
Every successive observed output changes. Opponent-edge D0 rises for P1 while P2's computed opponent edge stays296; the pair remains two units apart.
The +CB selectors and indexed records remain fixed in this interval. P1 vertical coordinate stays40; P2 is47,50,53,55,57,58,59,60,60,59 at the ten updates.
This supports changing spatial separation rather than a table-selector transition.

The old TSV does **not** contain input/state/animation snapshots. It cannot establish exact named jump, attack or knockback states. The old phrase “attack window” was a harness label, not verified attack-state evidence.
V03 reproduced the first eight old writes exactly, adding snapshots: P1 raw +4 word0202, P2 raw +4 word0200; active bytes1; P1 x272 and y40, while P2 moves right/up.
These raw states and animation pointers are reported without assigning unverified move names. Later inputs deliberately change the scenario, so V03 is not substituted as a replay of the entire old interval.

## Triggered gameplay phases
Existing boot/select inputs are reused, then:
baseline8 intervals; approach toward the opponent until edge<=48 (or150 interval cap);
two four-interval Button1 presses in a28-interval attack phase;
retreat48 intervals; release8 intervals.
Input names denote issued controls, not validated animation-state names.

| Phase | Start interval | Sampled P1 X range | Sampled P1 +21C range | Captured CPU reads |
|---|---:|---:|---:|---:|
| BASELINE | 2939 | 272–272 | 166–223 | 0 |
| APPROACH | 2946 | 272–329 | 62–280 | 63 |
| ATTACK | 2988 | 338–341 | 24–58 | 19 |
| RETREAT | 3016 | 272–341 | 58–183 | 55 |
| RELEASE | 3064 | 272–272 | 159–159 | 10 |

P1 moved toward the opponent and then back. During the attack-input phase, its animation pointer changed and +21C reached24; a named attack/hit event is not proven.
Raw +4 transitions0202→0200 and the observed animation addresses are in the JSON.
Phase ranges are sampled values, not complete extrema for every CPU update.

First experiment:226 JSONL events,147 actual CPU reads,40 CPU writes,115370 bytes total; exit0, stderr empty,13.14s.
Output limit600 events /900000bytes; taps watch only FF861C..1D and FF8A1C..1D.
Observer snapshots use an explicit reentrancy guard. They are not counted as CPU reads.
Write snapshots occur **before** the game's write; bus_data is the new value and snapshot.edge is the previous stored value.
CPU writes are sampled at most four times per address/phase; reads at most12 per PC/address/phase. Counts are captured samples, not exhaustive access totals.

All40 logged writes match the V01 arithmetic using the receiver/opponent X values, selector, ROM record X-offset/radius, and receiver orientation-condition flag.
This establishes **absolute16-bit horizontal distance from the receiver X to a computed opponent edge**, rather than center-to-center or both-box-edge separation.
Movement, selector changes and orientation can affect it; animation-pointer changes alone do not establish causation.
No physical push correction is performed by the recovered writer or this consumer region.

## First confirmed consumer and control flow
First actual read: interval2955, APPROACH phase, CPU PC037A56, A6=FF8800, addressFF8A1C, word273.
Observed IR0C6E matches the source cmpi.w opcode at this PC.
At other callback sites IR can be prefetched/advanced; those IR values are not promoted as their opcode proof.

Region [037A56,037A82),14 instructions /6 blocks:
- Unsigned distance>=48 → false exit037A7A→037A7C, D0=0.
- Otherwise test opponent byte+A9 nonzero and opponent word+4==0200.
- Then reload opponent via receiver+38, read its animation pointer+1C and longword animation+8.
- Nonzero animation word → D0=1 at037A7E→037A80; otherwise D0=0.
A4 must already identify the opponent at entry. A4/D0/CCR can change; no broader calling convention is established.

A second bounded run used the same scenario and traced only this predicate:
037A5C BCC→037A7A MOVEQ0→037A7C RTS. Debugger output confirms D0=0.
Tracing begins after the compare breakpoint, while the first run independently supplies the actual memory read/opcode/value.
The near-condition breakpoint did not fire. Reaching24 during the attack phase does not prove this particular predicate executes at that distance; it has other incoming gates.
Both files are small. No unrestricted trace or debugger disassembly export was used.

This demonstrates a **proximity gate in a Boolean opponent-state/animation predicate**.
The caller consuming D0, the exact named gameplay action, and hitbox bug causation remain unresolved.
Other observed read PCs:
0x2FB36, 0x2FB62, 0x35ECA, 0x35EF4, 0x36452, 0x374EA, 0x37502, 0x37A08, 0x37A56, 0x39508.
Each is searchable with null function ownership. Static pattern matches, including false positives, were not promoted.

## Independent exporter repair and fixture
[bounded_m68k_export_v01.py](../tools/bounded_m68k_export_v01.py) replaces debugger-expression-based exports for this recovery:
integer-only byte ranges, aligned bounds,256-byte maximum,128-instruction maximum,64KiB output limit, exclusive creation.
It never passes a value like A6 to the debugger.
A six-byte NOP/MOVEQ/RTS fixture and eight negative cases pass, including register/expression strings, oversized/out-of-range/odd lengths and truncated instructions.
The fixture initially caught Capstone accepting a short immediate buffer. Decode now uses lookahead then rejects instructions crossing the requested end.
Fixture passed **before** the44-byte real-region export.
The earlier V02 debugger exporter is retained as historical failure evidence; its numeric-literal correction is not relabeled as tested.

## Assembly parity
Source tools/collision_consumer_037a56_v03.s, GNU as2.38 -m68000 / objcopy.text.
CPU interval [037A56,037A82),44 bytes.
Source SHA-256: 0afcfba167206ae02cc185f63cbf61349e5c8b00aef2d5a35232f2e437b572fa.
Expected original and assembled SHA-256:
392e38ccac8f3ea8919bc0d68d6d32daeb3144bf0e4ceaefe8095352aa0cbdad.
Mismatch addresses[]; PASS.
The source is authored instructions/labels; no incbin or raw ROM directives.
All previous V01/V02 assembly sources match their prior hashes.

## Existing SQLite preservation
Migration [ingest_collision_consumer_v03.py](../tools/ingest_collision_consumer_v03.py).
Backup: evidence/functions_v01_before_collision_consumer_v03.sqlite.
Backup and DB integrity/FK checks pass before/inside/after commit.
Every old row remains exact; no prior function IDs, call relationships, issues, raw observations or reconstruction receipts changed.
Counts stay61 functions/80 calls because the new region's containing function is unresolved.
Added: one region,14 instructions,6 blocks, explicit CFG edges,10 consumer sites, five scenario summaries and187 operand rows.
Four prior assembly sources are hash-protected.

New tables: collision_consumer_regions, collision_consumer_instructions, collision_consumer_blocks, collision_consumer_edges, collision_consumer_sites, collision_scenario_summaries.
Existing assembly_region_reconstructions and runtime_collision_dependencies gain additive evidence.
Hitboxes issue remains investigative/open.

```sql
SELECT * FROM collision_consumer_regions;
SELECT cpu_pc,function_id,region_id FROM collision_consumer_sites;
SELECT source_pc,target_pc,kind,runtime_proven FROM collision_consumer_edges;
SELECT cpu_pc,frame,address,bus_data FROM runtime_collision_dependencies
WHERE evidence_id='collision-consumer-v03' AND kind='READ' ORDER BY id;
```

## Reproduction and execution limits
Run project commands from D:\AIOS_SFZ3MIX_V032 with canonical per-command preflight:
```powershell
C:\Python314\python.exe C:\AIOS\02_RUNTIMES\AIOS_KNOWLEDGE_CONTEXT_RUNTIME_01\host_context_runtime.py build --workspace sfz3mix-v032
C:\Python314\python.exe tools\bounded_m68k_export_v01.py --fixture
C:\Python314\python.exe tools\run_collision_scenarios_v03.py
C:\Python314\python.exe tools\run_collision_scenarios_cf_v03.py
C:\Python314\python.exe tools\bounded_m68k_export_v01.py --start 0x37a56 --length 44 --output evidence\collision_consumer_export_v03.json
C:\Python314\python.exe tools\verify_collision_consumer_v03.py
C:\Python314\python.exe tools\ingest_collision_consumer_v03.py
```
All capture/export/migration names refuse overwrite. Do not delete evidence or backups to rerun.
Verifier contains exact WSL assembler commands; runner receipts contain full emulator argv.
Local-only: scenario JSONL, launch JSON, far-path trace/console, opcode export, object/bin outputs, SQLite backup and DB receipt.
Network command/file-write timeouts occurred; missing writes were retried before accepted execution. No timed-out command is claimed as a passing test.
Exploratory local inspectors produced only candidates; those are not canonical ownership evidence.

D: start142,606,336 bytes free, final111,149,056 bytes (~106MiB).
The two new JSONL captures total about230KB; the larger free-space decrease is unaccounted for and is not attributed to these bounded logs. No deletion, relocation or further capture attempted.
ROM and all old sources unchanged. No expensive CI or gameplay modification.

## Next target
Trace the caller consuming this predicate's D0 and the gates before037A56; reach the near branch deliberately.
Use the proven +21C reader sites to distinguish a proximity decision from actual movement/contact resolution.
Preserve null function ownership until entry/call boundaries are verified. Do not mark community hitboxes fixed.
