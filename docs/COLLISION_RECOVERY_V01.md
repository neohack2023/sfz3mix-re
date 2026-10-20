# Collision callable-region recovery and assembly parity — 2026-10-20

**PASS for the bounded callable region 0x02C19A–0x02C1E1.** Function ID: FUNC_REC_02C19A. Existing workspace and database retained; no gameplay or source-ROM modification.

## Preconditions and evidence
Canonical preflight repeatedly returned READY_CONTINUE / ALL_REQUIRED_PREFLIGHT_COMPONENTS_PASS for sfz3mix-v032 under github:neohack2023/sfz3mix-re. CPU sz3mx.03 SHA-256 was independently checked before and after:
b5f7a1598e4f91a5113c506505b482b2cd1a19e366fe31471740e45dbd204691.
D: began with 434,110,464 free bytes (~414 MiB). Existing SQLite integrity_check=ok and foreign_key_check empty. Preserved 50-sample trace hash independently matched 4c099e68554cc200d265b6ea4d108e23136a38f6df6b61577384655917b5762f.

Existing Capstone 5.0.6, HBMAME 0.289.3 and WSL GNU M68000 assembler 2.38 were exercised. No installation, ZIP extraction, repository clone or new workspace.

## Recovered region
The old trace establishes 0x02C1A6 (+CB) and 0x02C1AC (+9C) as real readers. Decoding from an arbitrary earlier address 0x02C140 failed to form a continuous stream; that is not a function-boundary claim. Anchoring at verified instruction starts instead exposes a closed direct CFG to RTS.

- Callable entry: 0x02C19A, a direct BSR target observed at runtime.
- Exit instruction: RTS at 0x02C1E0; end-exclusive 0x02C1E2.
- 26 byte-verified instructions, seven basic blocks.
- Incoming BSR sites: 0x02C182, 0x02C18A, 0x02C192. First call corroborated by live entry/RTS and return to 0x02C186; other two are static opcode-verified relationships.
- Wrapper at 0x02C17E sets A6=A5+0x400,+0x800,+0xC00,+0x1000; final path falls through into the same leaf. A5=0xFF8000 observed, giving first player objects 0xFF8400 / 0xFF8800. Four active players are not established.
- No call or indirect branch exists inside the recovered leaf. Caller function IDs stay null because wrapper ownership and all external/indirect incoming edges are not exhaustively proven.
- This is an entry-bounded shared region, not exclusive function ownership over every byte.

A6 supplies the receiver object. The word at receiver+0x38 is sign-extended into A4, addressing the opponent on the 24-bit bus. D0 is cleared, reads opponent+CB, then shifts left three; A0 receives opponent+9C plus that index. The body reads record+4 and record+0, applies an orientation-dependent sign calculation, combines opponent X and receiver X, and stores a 16-bit absolute delta at receiver+0x21C.

Clobbers: D0, D1, D2 low byte, A0, A4 and CCR. A5/A6 are not changed by the body. No broader ABI guarantee is claimed. SP/d@SP debugger snapshots were inconclusive and excluded from entry/return proof.

## Smallest additional runtime experiment
The initial 50 samples lacked entry/exit and record reads. A new experiment watches just the frame_done interval 2939→2940 after the existing boot/select inputs, while tracing one active invocation from entry to RTS.

V01 instruction trace worked, but operand callbacks incremented their count before failing on absent Lua A7 state; its reported 44 attempts are not accepted observations. V01 artifacts remain local as failure evidence.
V02 uses the exposed SP state for logging; entry/return proof relies on PCs, not the inconclusive stack-memory expression. It completed exit 0 in 12.53 s, produced 44 actual operand rows, and preserved all old output files.

Observed chains:
| Receiver | Opponent | Pointer | Selector | Record | Read fields |
| --- | --- | --- | --- | --- | --- |
| 0xFF8400 | 0xFF8800 | 0x0F2ACA | 3 | 0x0F2AE2 | +0 signed X=-3; +4 unsigned radius=19 |
| 0xFF8800 | 0xFF8400 | 0x0D6580 | 10 | 0x0D65D0 | +0 signed X=0; +4 unsigned radius=24 |

The first record already appears among the earlier 16 distinct decoded addresses; the second is newly observed here. Both actual CPU reads match the original source-file words and pointer+(selector<<3). This agrees with the published SFA3 push-record layout:
https://github.com/Jesuszilla/mame-rr-scripts/blob/master/cps2-hitboxes.lua
Only X/radius-X reads are proven here; this leaf does not read the Y fields.

Four complete receiver calculations reproduce the game-originated output writes: 173,171,179,177. “push_edge_distance_candidate” is a descriptive investigation name, not proof of hit/contact resolution or restored visual hitboxes.

## Source-authored assembly parity
- Source: tools/collision_leaf_02c19a_v01.s; no incbin, byte arrays or raw-byte directives.
- CPU interval: [0x02C19A,0x02C1E2), 72 bytes.
- GNU as -m68000 and objcopy .text output matched exactly.
- Expected original and assembled SHA-256:
  b1950ddb837bf0036268744f336ad6dff445dde6c7de5cfb2920d2c933b6178e.
- Mismatch addresses: [].
- [Machine-readable parity receipt](COLLISION_ASSEMBLY_PARITY_V01.json).
- [Machine-readable reconstruction](COLLISION_RECONSTRUCTION_V01.json).

The HBMAME full-region disassembly matches original bytes instruction-by-instruction. Runtime path covers the selector-present case, orientation==1 branch and negative-delta path. Other branch encodings are statically byte-verified; all branch paths have not been runtime-exercised.

## Reproduction commands
Existing host context projection is refreshed after adding tools; preflight remains enabled.

    C:\Python314\python.exe C:\AIOS\02_RUNTIMES\AIOS_KNOWLEDGE_CONTEXT_RUNTIME_01\host_context_runtime.py build --workspace sfz3mix-v032
    C:\Python314\python.exe C:\AIOS\09_REMOTE_RUNNER\RUN_SFZ3MIX_RECOVERY_V02.py
    wsl.exe bash /mnt/d/AIOS_SFZ3MIX_V032/tools/collision_assembly_v01.sh
    C:\Python314\python.exe D:\AIOS_SFZ3MIX_V032\tools\verify_collision_reconstruction_v01.py
    C:\Python314\python.exe D:\AIOS_SFZ3MIX_V032\tools\ingest_collision_reconstruction_v01.py

The published runner has the same tested contents; its source lives at tools/run_collision_recovery_v02.py. The probe refuses to overwrite its outputs. The ingestion refuses to repeat over the existing backup. For a new trial, deliberately assign new evidence names and preserve lineage; do not delete old receipts to force reruns.

Local-only artifacts: evidence/collision_recovery_{console,trace,disasm}_v02.txt, collision_recovery_v02.tsv, collision_recovery_launch_v02.json, collision_leaf_02c19a_v01.{o,bin}, disassembly and prior failed V01 outputs. No ROM bytes/dumps/binaries published.

## Existing SQLite migration and checks
The transaction backs up with SQLite's backup API to evidence/functions_v01_before_collision_reconstruction_v01.sqlite.
Additions: function_basic_blocks, function_instructions, function_cfg_edges, function_reconstructions, function_operand_accesses and function_data_xrefs. Four newly observed RAM fields are added; existing RAM fields retained.

Final: 60 functions (59 original candidates unchanged plus one recovered region), 79 calls (76 original unchanged plus three incoming BSR sites), 26 instructions, seven blocks, 44 new operand accesses, eight function-RAM xrefs and four function-data xrefs. Two prior runtime instruction sites now link to the verified entry-bounded region. Other seven prior sites remain unresolved. The 20 earlier box decodes are unchanged.

Integrity and foreign-key checks passed before and after commit. Exact-row preservation checks passed for original functions/calls/box decodes. Mismatch detector negative controls passed (changed byte and length mismatch). Four observed arithmetic cases passed. No expensive CI used.

## Limits and next target
Hitboxes community issue remains OPEN / INVESTIGATION_NOT_FIXED. The region computes an opponent-edge distance; neither hitbox restoration nor its entire gameplay use is established. Remaining work: wrapper entry/call ownership, the other seven observed instruction sites, runtime zero-selector/inactive branches and downstream consumers of +0x21C. Repeat on a second scenario before widening semantics. Karin rolling and Alpha Counter effects remain separate future tasks.
