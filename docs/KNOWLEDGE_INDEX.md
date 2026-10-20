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
