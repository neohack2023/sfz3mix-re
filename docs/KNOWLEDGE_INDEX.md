# Knowledge and evidence index

Use this directory of links to find verified results, unresolved leads, and reusable tools without rereading all historical reports.

| Question | Authoritative starting point | Status |
|---|---|---|
| What should the next agent do? | [Current state](CURRENT_STATE.md) | Maintained handoff |
| What did the community request? | [TODO and requester attribution](../TODO.md) | Open bugs and proposals |
| Which experiments passed or failed? | [RE handoff](RE_ENGINEERING_HANDOFF_2026-10-20.md) | Evidence inventory and limits |
| How was the continue score reproduced? | [Continue-counter receipt](CONTINUE_COUNTER_2026-10-19.md) | Runtime symptom proven, no fix |
| What bytes and archives were verified? | [Whole-program V01](WHOLE_PROGRAM_V01.md) | Complete byte accounting, not code recognition |
| What is known about address mappings? | [32 sampled matches](PROGRAM_MAPPING_SAMPLES_V02.json) | Data-space samples only |
| How far is instruction recovery? | [Instruction recovery V01](INSTRUCTION_RECOVERY_V01.md) | Bounded CFG, assembly parity for 26 bytes |
| What functions are known? | [Function registry](FUNCTION_REGISTRY_V01.json) | 59 unverified entries |
| What older addresses may matter? | [Function leads](FUNCTION_LEADS_V01.json) | Hypotheses, not proven roles |

## Canonical artifact and workflow
- Primary: **verified extracted ROM components**, not the distribution ZIP. CPU program `sz3mx.03` SHA-256 `b5f7a1598e4f91a5113c506505b482b2cd1a19e366fe31471740e45dbd204691`. Confirm the existing Host 02 file's hash before using it.
- Analyze CPU bytes → classify instructions/functions/data → assemble into a disposable program-file derivative → compare byte hashes and test in the emulator.
- Packaging into an emulator ZIP is optional and only relevant at compatibility or release validation. Older archive-centered reports remain historical evidence, not instructions to re-extract anything.

## Tool directory
- **Legacy archive package test (not the primary ROM-analysis entrypoint):** [rom_rebuild_v01.py](../tools/rom_rebuild_v01.py).
- **RAM/program-space samples:** [program_space_probe_v02.lua](../tools/program_space_probe_v02.lua) and [compare_program_space_v02.py](../tools/compare_program_space_v02.py).
- **68000 static graph:** [m68k_cfg_v01.py](../tools/m68k_cfg_v01.py), [test_m68k_cfg_v01.py](../tools/test_m68k_cfg_v01.py).
- **Genuine editable assembly:** [sfz_buffer_writer_v01.s](../tools/sfz_buffer_writer_v01.s), [assembly_roundtrip_v01.sh](../tools/assembly_roundtrip_v01.sh), [verify_assembly_rom_v01.py](../tools/verify_assembly_rom_v01.py).
- **Function registry generator:** [build_function_registry_v01.py](../tools/build_function_registry_v01.py).
- **Runtime test harnesses:** currently local to Host 02, especially `tools/continue_press.lua`, `score_debug.lua`, `pc_trace.lua`.
- **Toolchain binaries:** local, not committed. Capstone 5.0.6 and WSL GNU M68000 assembler 2.38.

## Evidence vocabulary
`RUNTIME_PROVEN`: observed in a reproducible emulator test, not necessarily FBNeo or hardware. `STATIC_CANDIDATE`: disassembly or graph hypothesis requiring a runtime check. `ASSEMBLY_PARITY_PASS`: byte-exact source reassembly, not a gameplay fix. `REPRODUCED_NOT_FIXED`: bug observable, cause still unknown. `FAILED`: preserve prior attempt and reason. `ACCEPTED_PATCH`: verified ROM modification with regression evidence.

## Document maintenance
Keep [CURRENT_STATE](CURRENT_STATE.md) short and updated. Add dated receipts for significant discoveries, and link them here. Preserve existing file URLs rather than moving old reports into new folders. Never check a community TODO merely because assembly or packaging tests passed. See [AGENTS.md](../AGENTS.md).

## Searchable function database
- [Function Database V01](FUNCTION_DATABASE_V01.md) documents the indexed SQLite schema and commands. The derived DB stays local on Host 02; builder and sanitized source registry live in GitHub.

## Original unmodified comparison reference
[Original Capcom sfa3us revision manifest and acquisition status](ORIGINAL_SFA3US_REFERENCE.md): exact CRCs, required parent components, and lawful-source verification gates. **Identified but not acquired or verified locally.**

## External SFA3 and CPS2 research sources
- [External SFA3 source index V01](EXTERNAL_SFA3_SOURCE_INDEX_V01.json): seven machine-readable upstream references; explicit platform, revision and evidence limitations. Includes PS1 Alpha 3 recompilation, CPS2 Alpha 3 hitbox Lua/RAM maps, Alpha 3 arcade patch examples and CPS2 recompilation methodology. **No exact sfa3us complete decompilation verified.**

## Tested SFA3 RAM compatibility and function-knowledge ingestion
- [SFA3 RAM comparison and 8-byte hitbox record tests](SFA3_RAM_COMPATIBILITY_V01.md): read-only HBMAME input-driven RAM checkpoints, 2 observed player bases, 20/20 original-format records decoded; no instruction xref yet.
- [Machine-readable SFA3 RAM profile](SFA3_RAM_PROFILE_V01.json): per-field status, 0x400 player stride versus 0x100 projectile stride, DB import counts and limitations.
- [Tools: compare](../tools/compare_sfa3_ram_v02.py), [decode box records](../tools/decode_sfa3_hitbox_data_v01.py), [ingest RAM](../tools/ingest_sfa3_ram_v01.py), [ingest decoded records](../tools/ingest_sfa3_box_decode_v01.py), [query](../tools/query_sfa3_ram_v01.py).
