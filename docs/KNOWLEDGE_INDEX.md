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
| What functions are known? | [Function registry](FUNCTION_REGISTRY_V01.json) | 59 original candidates plus verified shared callable regions |
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

## Approved registration and runtime collision instruction accesses
- [Authority recovery receipt with successful continuation](AUTHORITY_RECOVERY_2026-10-20.md): Drive row 24 and Host 02 binding verified; canonical preflight PASS. Fifty access samples / nine exact instruction sites; function ownership unresolved.
- [Bounded read-only HBMAME probe](../tools/collision_access_v01.lua) and [additive SQLite ingestion](../tools/ingest_collision_access_v01.py): 74 RAM-field links, existing records preserved, integrity/FKs PASS. Raw output remains local. Preserve fixed output files before a repeat.

## Verified collision callable-region reconstruction
- [Recovery and local validation receipt](COLLISION_RECOVERY_V01.md): FUNC_REC_02C19A, 26 instructions / seven blocks, runtime pointer-selector-record reads and bounded ownership limits.
- [Machine-readable reconstruction](COLLISION_RECONSTRUCTION_V01.json) and [72-byte assembly parity receipt](COLLISION_ASSEMBLY_PARITY_V01.json).
- [Editable GNU assembly](../tools/collision_leaf_02c19a_v01.s), [assembler command](../tools/collision_assembly_v01.sh), [bounded probe](../tools/collision_recovery_v02.lua), [runner](../tools/run_collision_recovery_v02.py), [verifier](../tools/verify_collision_reconstruction_v01.py), [transactional DB migration](../tools/ingest_collision_reconstruction_v01.py).
- Current registry: 59 original static candidates plus one verified entry-bounded callable region. Earlier zero-owner/zero-xref checkpoints remain historical evidence.

## Collision Engine Recovery V02
- [Engineering receipt, failures and next target](COLLISION_ENGINE_RECOVERY_V02.md).
- [Machine-readable wrapper, seven site assessments, runtime dependencies and three parity receipts](COLLISION_ENGINE_RECOVERY_V02.json).
- [Wrapper prefix](../tools/collision_wrapper_02c17e_v02.s), [dual-record block](../tools/collision_dual_records_029a42_v02.s), [selector-update block](../tools/collision_selectors_02f666_v02.s).
- [Bounded probe](../tools/collision_engine_v02.lua), [runner](../tools/run_collision_engine_v02.py), [verifier/assembler](../tools/verify_collision_engine_v02.py), [transactional migration](../tools/ingest_collision_engine_v02.py).
- SQLite:61 functions/80 calls; explicit shared blocks; unresolved function owners retained. +21C consumer search was bounded-negative. Recheck154MiB free storage before captures.

## First downstream collision-result consumer V03
- [State review, triggered scenarios, first consumer and limits](COLLISION_CONSUMER_V03.md), [machine-readable evidence/parity](COLLISION_CONSUMER_V03.json).
- [44-byte consumer assembly](../tools/collision_consumer_037a56_v03.s); [bounded exporter with fixture](../tools/bounded_m68k_export_v01.py).
- [Scenario probe](../tools/collision_scenarios_v03.lua), [runner](../tools/run_collision_scenarios_v03.py), [control-flow probe](../tools/collision_scenarios_cf_v03.lua), [control-flow runner](../tools/run_collision_scenarios_cf_v03.py).
- [Verifier/assembler](../tools/verify_collision_consumer_v03.py), [preserving SQLite migration](../tools/ingest_collision_consumer_v03.py).
- 037A56 reads+21C and gates a Boolean predicate at unsigned48; far branch proven, near branch and caller purpose unresolved. No new function owner invented.

## V04 caller/result/state recovery — success path unresolved
- [Engineering receipt and precise gate blocker](COLLISION_DECISIONS_V04.md), [machine-readable trials/callable/parity](COLLISION_DECISIONS_V04.json).
- [Callable037A46](../tools/collision_predicate_037a46_v04.s), [caller bit0 block](../tools/collision_caller_0379ae_v04.s), [success store](../tools/collision_success_037a3e_v04.s), [mode application](../tools/collision_apply_037ad2_v04.s), [outer caller](../tools/collision_outer_02c584_v04.s).
- [Controlled standing harness](../tools/collision_decisions_controlled_v04.lua), [standing runner](../tools/run_collision_decisions_controlled_v04.py), [crouching harness](../tools/collision_decisions_crouch_v04.lua), [crouching runner](../tools/run_collision_decisions_crouch_v04.py).
- [Verifier](../tools/verify_collision_decisions_v04.py), [preserving migration](../tools/ingest_collision_decisions_v04.py).
- Current62functions/83calls. Earlier null-owner V03 rows are historical; collision_region_ownership_claims supplies current nonexclusive membership.
