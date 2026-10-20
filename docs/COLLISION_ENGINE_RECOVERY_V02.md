# Collision Engine Recovery V02 — 2026-10-20

## Decision
PASS for wrapper/shared-tail classification, bounded consumer-negative evidence, seven site assessments, three exact assembly reconstructions and additive SQLite integration. No gameplay patch or hitbox fix.

Scope: github:neohack2023/sfz3mix-re. Host 02: DaltonsLaptop574. Existing workspace D:\AIOS_SFZ3MIX_V032; no clone, extraction, installation or new database.
Per-command canonical preflight returned READY_CONTINUE / ALL_REQUIRED_PREFLIGHT_COMPONENTS_PASS for inspection, launch, verification, migration and final hash check. A stale context projection after adding a tool was rebuilt through host_context_runtime.py; no authority override.

ROM SHA-256 before/after:
b5f7a1598e4f91a5113c506505b482b2cd1a19e366fe31471740e45dbd204691.
Original V01 leaf source SHA-256 unchanged:
c9e9bd5c0526032a8eec09d5e93bca0a533a07be2e64815229bbd02f0c0b0c90.

## Wrapper and shared region
FUNC_REC_02C17E is a runtime-observed callable wrapper, rather than a duplicate exclusive owner of the leaf bytes.
- Direct BSR at 0x02C07E enters 0x02C17E; caller's containing function remains unresolved.
- Prefix [0x02C17E,0x02C19A) sets A6=A5+0x400, +0x800, +0xC00, +0x1000.
- BSR sites 0x02C182, 0x02C18A and 0x02C192 call existing FUNC_REC_02C19A.
- Returns observed at 0x02C186, 0x02C18E and 0x02C196.
- Last LEA falls through into the same leaf entry. Its RTS at 0x02C1E0 returns to 0x02C082.
- The 67-instruction trace contains four leaf entries and four RTS executions.
- Seven existing leaf blocks are referenced by function_shared_blocks, not duplicated. Four prefix blocks and seven prefix instructions belong to the wrapper.
- Runtime object slots: FF8400, FF8800, FF8C00, FF9000. Last two take the inactive gate. This does not establish four active players.
- A5 is preserved by this body; wrapper changes A6 and leaf clobbers A0/A4/D0/D1/D2-low/CCR. Wider ABI and indirect entry inventory remain unresolved.
- Architectural BSR/RTS stack effects are -4/+4. Debugger SP snapshots stayed FF7FF6, so they are excluded from live stack/ABI proof; control flow is established by actual PCs and source-byte matching.

The overlapping interval [02C19A,02C1E2) is one shared body. Both entrypoints are real; exclusive whole-range ownership is not asserted.

## Bounded gameplay experiment and downstream result
Existing boot/select inputs were reused; no memory values or game instructions were modified.
Frame_done intervals 2939..2946: 180 operand rows, cap512, 20 writes and zero reads at FF861C/FF8A1C.
These are both players' +0x21C fields. This is a bounded negative consumer result, not evidence that the value is never consumed.
Multiple game updates can occur inside an interval. Observations retain interval numbers and register snapshots; bus longwords are two 16-bit transfers and byte masks identify their lane.

The newly observed 029A10 chain reads both +CB selectors and +9C pointers, shifts indices by three and accesses:
| Instruction | Record | Offset | Word |
|---|---|---|---|
| 029A56 | 0D65D0 | +2 | 6 |
| 029A5E | 0F2AE2 | +2 | 59 |
| 029A70 | 0D65D0 | +6 | 6 |
| 029A74 | 0F2AE2 | +6 | 26 |

Each actual table word matches the source ROM. The code combines +2 with object +14, computes an absolute vertical delta, subtracts summed +6 radii, and conditionally exits at 029B3E. These observations support vertical interval comparison using the original SFA3 eight-byte format. They do not establish a +21C consumer or positional correction. Later horizontal tests / +298 writes are statically visible but not promoted as runtime-proven contact resolution.

V02 trace SHA-256: e02c8ab5a5ceb3edcc9fdff2f159ff0ae81c806359907323d7cbf4846bc8f0bf
Instruction trace SHA-256: 2f3378249b1ecc9c0386e822f93e39b7a377e51a5e73381ed611ba6220d467cf
HBMAME exit0, stderr empty, elapsed58.49s.

## Seven previously unowned sites
| PC | Bounded context | Ownership/confidence |
|---|---|---|
| 029A10 | A6+CB; zero branch to029B3E | Reobserved; function unresolved |
| 029A1A | A4+CB; zero branch to029B3E | Reobserved; function unresolved |
| 029A42 | A6+9C, indexed record+2 | Reobserved; function unresolved |
| 029A46 | A4+9C, indexed record+2 | Reobserved; function unresolved |
| 027EDA | A1+C8 longword -> A5-5CD6; zero branch027FDA | Old runtime proof + newly byte-verified block |
| 027EF0 | A1+90 indexed by selector*8; BSR027EF8→0296A6 | Old runtime proof + static call; caller unresolved |
| 02F666 | source(A0) longword -> A6+C8..CB | Old runtime proof + exact block assembly |

All seven receive searchable collision_reader_assessments; none receives guessed function ownership. Their direct exits, instructions and confidence are in COLLISION_ENGINE_RECOVERY_V02.json. Alternate entry and predecessor discovery remains incomplete.

## New editable assembly parity
GNU m68k-linux-gnu-as2.38 -m68000 and objcopy .text, using existing tools/.m68k_toolchain:
| Source | CPU interval | Bytes | Expected = assembled SHA-256 |
|---|---|---|---|
| [collision_wrapper_02c17e_v02.s](../tools/collision_wrapper_02c17e_v02.s) | [2C17E,2C19A) | 28 | 5d0ce2f11294b0710fc2b22612b51acf35d04645b29f4c7dbd68536b435eb1b0 |
| [collision_dual_records_029a42_v02.s](../tools/collision_dual_records_029a42_v02.s) | [29A42,29A66) | 36 | ffb75a6805359b6bad410a6e25280af40d012aaf66f5ff412b38bd01c67aac1b |
| [collision_selectors_02f666_v02.s](../tools/collision_selectors_02f666_v02.s) | [2F666,2F68C) | 38 | e5f92cf4185897b3a4bda2889a308948b4c01492d2836fd7ebf475f444197415 |

All three PASS; mismatch addresses []. Source hashes are in the machine-readable receipt.
The wrapper source is a prefix: its local end label represents the existing leaf entry, not an added instruction or standalone replacement routine.
No original ROM file was patched.

## SQLite transaction and preservation
Existing evidence/functions_v01.sqlite extended in one transaction. SQLite API backup:
evidence/functions_v01_before_collision_engine_v02.sqlite.
Backup integrity/FK checks and database checks before/inside/after commit passed.
Final61 functions /80 calls. Original function IDs, prior evidence,20 decoded samples and old raw observations remain.
Only three prior call records were intentionally reconciled: wrapper caller ID, runtime kind/confidence and evidence. The new upstream call has unknown caller ID.
New tables:
function_shared_blocks, function_control_relationships, function_contracts,
collision_reader_assessments, runtime_collision_dependencies,
collision_data_dependencies, assembly_region_reconstructions.
Local receipt: evidence/collision_engine_db_receipt_v02.json.
Migration refuses replay when its rollback backup exists; do not delete the backup to force a rerun.

Useful queries:
```sql
SELECT f.id,s.block_id FROM functions f
JOIN function_shared_blocks s ON s.function_id=f.id
WHERE f.cpu_address=0x02C17E;
SELECT cpu_pc,region_start,region_end_exclusive,function_id,confidence
FROM collision_reader_assessments ORDER BY cpu_pc;
SELECT cpu_pc,kind,address,bus_data,bus_mask,frame
FROM runtime_collision_dependencies WHERE address IN (0xFF861C,0xFF8A1C);
SELECT * FROM assembly_region_reconstructions;
```

## Commands and failed approaches
Executed on Host02, with Set-Location D:\AIOS_SFZ3MIX_V032 for project commands:
```powershell
Get-FileHash tools\sz3mx.03 -Algorithm SHA256
Get-PSDrive D
C:\Python314\python.exe C:\AIOS\02_RUNTIMES\AIOS_KNOWLEDGE_CONTEXT_RUNTIME_01\host_context_runtime.py build --workspace sfz3mix-v032
C:\Python314\python.exe tools\inspect_collision_v02.py
C:\Python314\python.exe tools\run_collision_engine_v02.py
C:\Python314\python.exe tools\verify_collision_engine_v02.py
C:\Python314\python.exe tools\ingest_collision_engine_v02.py
```
The verifier invokes WSL bash and the existing absolute GNU assembler/objcopy paths; its exact commands are source-controlled. Runner records exact HBMAME argv and timeout in the local launch JSON.

Failures preserved:
1. Default Python lacked Capstone; existing tools/.vendor resolved it. No installation.
2. Arbitrary earlier disassembly starts were misaligned and rejected; they are not boundary evidence.
3. Debugger disassembly export length bare A6 resolved as a register, causing an oversized local text export. Runtime trace and operand taps remained bounded. Validator now streams only the intended ranges; all accepted opcode evidence matches original bytes. The committed probe corrects export expressions to explicit0x numbers. This correction was not rerun; accepted runtime observations are from the executed version. No repeat capture was justified.
4. Initial WSL command variable expansion lost the tool path; explicit absolute paths passed.
5. SP snapshots remain inconclusive; not used to assert stack ABI.
6. No +21C consumer observed in this eight-frame scenario; no zero-selector case observed.

Storage: start408,944,640 bytes free; final161,480,704 bytes (~154MiB). Oversized export retained locally as failure evidence. No extra captures, file deletion or relocation.
Raw TSV, instruction/disassembly outputs, console, binaries and database remain on Host02; only sanitized tools/sources/registries/receipts are published. No expensive CI requested.

## Next execution target
Before another capture, check storage and bound every debugger expression explicitly.
Find static +21C read candidates, then select one gameplay scenario that reaches them. Establish the containing entry for the029A10 chain and observe vertical overlap before claiming horizontal separation/correction. Preserve shared-block identities and null owners. Hitbox restoration, Karin rolling and Alpha Counter effects remain unfixed.
