# SFZ3 Mix v0.32 — Consolidated RE Handoff (2026-10-20)

## Scope and source of truth
- Game remains an FBNeo-compatible CPS2 ROM patch project, not recompilation.
- Community source: [u/Motor_Economy_1741 Reddit post](https://www.reddit.com/r/romhacking/comments/1xa4ydk/street_fighter_zero_3_mix_is_dead/). See [TODO](../TODO.md) for complete backlog.
- Execution workspace: `D:\AIOS_SFZ3MIX_V032` on WINDOWS_EXECUTION_HOST_02 / DaltonsLaptop574.
- Host local evidence is authoritative for tested runtime observations; this report is a navigational handoff, not a replacement for logs or binaries.
- AIOS project-specific registered scope was **not verified** in the October 19 execution receipt. Do not invent it.

## Verified baseline and package mapping
- Original input archive: `downloads/sfz3mix_v032_original.zip`.
- SHA-256: `867b8356872a034ec7e06f776bf757ec2095fee7616931b71f720f30369806ab`.
- HBMAME-mapped archive: `runtime_hbmame/roms/sfz3mix.zip`; archive SHA-256 `9aa45504265889d66e01554d9e6950d0befb501b84e3fbf25e11702e5dd3d135`.
- Mapping receipt: `evidence/hbmame_rom_mapping.json`. Six entries, **rename-only, byte preserving**, no patch. Python builder `tools/map_for_hbmame.py` verifies expected entry CRC32 and resulting ZIP integrity.
- CPU `sz3mx.03` → `sfz3mix.p1`, 6,291,456 bytes, CRC32 `7A968DA6`.
- Graphics `sz3mx.13m` → `sfz3mix.c1`, 33,554,432 bytes, CRC32 `5389B651`.
- Graphics `sz3mx.21m` → `sfz3mix.c2`, 33,554,432 bytes, CRC32 `914C7031`.
- Audio CPU `sz3mx.01` → `sfz3mix.m1`, 524,288 bytes, CRC32 `52F98A5C`.
- Sound samples `sz3mx.11m` → `sfz3mix.q1`, 16,777,216 bytes, CRC32 `395EDCE2`.
- `dl-1425.bin` retained, 24,576 bytes, CRC32 `D6CF5EF5`.
- HBMAME 0.289.3 CPS2Turbo / Motorola 68000 audited the mapped set: **1 ROM set found, 1 OK**. Physical arcade hardware untested.
- FBNeo nightly ZIP was downloaded, but the October 19 receipt records that FBNeo's license was not accepted for the runtime session. The proof runs below used HBMAME. Do not claim FBNeo runtime equivalence.

## Experiments and outcomes
| ID | Experiment | Outcome | Evidence / next gate |
|---|---|---|---|
| EXP-01 | ZIP inventory and CRC integrity | Script exists; mapping successfully established | `tools/audit_bundle.py`; compare current hashes before reuse |
| EXP-02 | HBMAME archive remapping | PASS, rename-only; no ROM-byte modifications | `tools/map_for_hbmame.py`, `evidence/hbmame_rom_mapping.json` |
| EXP-03 | Clean-boot frame-controlled match/continue | PASS: visible score `0` before continue, `1` after | `tools/continue_press.lua`, `evidence/continue_press_log.txt`, screenshots |
| EXP-04 | HBMAME debugger disassembly | PASS: target-region dumps produced | `tools/targeted_disasm.lua`, `evidence/disasm_025cc0.txt`, `evidence/disasm_00331c.txt` |
| EXP-05 | RAM cheat narrowing | PARTIAL: candidate list generated, no responsible writer proven | `tools/score_debug.lua`, `evidence/score_candidates.xml` |
| EXP-06 | Near-continue save-state restoration | NOT VERIFIED: restore did not validate | `evidence/near_continue.sta`; prefer clean-boot harness |
| EXP-07 | Continue countdown stale/blue fragments mask experiments | FAILED ACCEPTANCE per prior project notes: 88 masks and V02 descriptors 90–102 | Need original iteration receipts/byte diffs to audit; don't repeat blind masking |
| EXP-08 | Gameplay ROM patch accepted | NOT DONE | No verified patched build or clean-vs-patched parity receipt |

## Confirmed observations, extracted leads and uncertainty
- `tools/continue_press.lua` schedules coin/start/select actions by frame, including continue coin at 10600 and start at 10670, captures frame snapshots, and exits after frame 17300. It logs to `evidence/continue_press_log.txt`. Tested story: Ryu/E.Honda/Blanka vs Sakura; team defeat; countdown; continuation.
- Score-debug commands in `evidence/score_debug_log.txt`: `cheatinit ub,ff0000,10000` at frame 9300, `cheatnextf increase,1` at 11000, and `cheatlist` at 17200. Output `score_candidates.xml` contains candidates, **not identified score ownership**.
- Disassembly dump `disasm_00331c.txt` contains `00331C move.l D1,(A4,D0.w)`, `003320 move.l D2,($4,A4,D0.w)`, `003324 move.l D3,($8,A4,D0.w)`, apparently a ring/buffer writer. Do not infer it writes the continue counter without a dynamic trace.
- `disasm_025cc0.txt` contains branches/calls across `025C40..025CC0`, including `025CC0 sub.w D7,($11a,A5)`; meaning relative to score is **not established**.
- Previous investigative lead: sprite writer at `0x026438`; candidate only, not the identified source of blue fragments.
- Earlier mask passes (88 masks; descriptors 90–102) failed acceptance according to project continuity, but exact scripts and diff receipts were **not found in the inspected local tools/patches listing**. Keep failure history separate from byte-verified local evidence.
- Note two different visual topics: intermittent stale countdown sprites (observed in Reddit conversation) vs score digit in HUD (locally reproduced). Fixing one does not prove the other fixed.
- External report [FBNeo floor edge glitch #1833](https://github.com/finalburnneo/FBNeo/issues/1833) is separate and may be emulator-specific; compare same ROM and input between HBMAME and FBNeo before ROM changes.
- ROM derivative format, bank offsets and HBMAME CPU-region mapping need validation before editing bytes: emulator CPU addresses are **not automatically archive offsets**.

## Tools available on Host 02
### Python/package analysis
`tools/audit_bundle.py`; `tools/map_for_hbmame.py`; `evidence/hbmame_rom_mapping.json`.

### HBMAME Lua and debugger
`tools/continue_press.lua`, `repro_after_continue.lua`, `repro_continue.lua`, `repro_extended.lua`, `repro_state_cli.lua`, `repro_window.lua`, `debugger_api_probe.lua`, `inmemory_probe.lua`, `ioport_probe.lua`, `memory_api_probe.lua`, `pc_trace.lua`, `ram_trace.lua`, `score_debug.lua`, `targeted_disasm.lua`.

### Runtime and evidence
`runtime_hbmame/hbmame.exe`, `runtime/fbneo64.exe`, `RUN_SFZ3MIX.cmd`, `RUN_SFZ3MIX.ps1`. Evidence directories: `snapshots`, `snapshots_after_continue`, `snapshots_continue_pressed`, `snapshots_extended`, `snapshots_inmemory_probe`, `snapshots_state_cli`, `snapshots_window`; logs include `pc_trace_log.txt`, `inmemory_probe_log.txt`, `repro_*_log.txt`, `score_debug_log.txt`, `targeted_disasm_log.txt`.

### Installed but not yet validated for this target
`Dalton-ghidra` local folder is present; exact version/project state not inspected. A `tools/sz3mx.03` binary is present and must **never** be promoted to GitHub.

## Next reproducible execution
1. Verify current source checksum, emulator audit, and baseline run without mutating originals.
2. Identify score HUD byte/word via correlated RAM observations; eliminate cheat-search false positives.
3. Use a bounded write/read breakpoint or trace on candidate addresses during the 10600–11300 frame transition. Log PC, address, width, value before/after and branch context.
4. Map confirmed code back to original input ROM storage through HBMAME driver/decryption/region understanding; inspect with Ghidra if useful.
5. Test a reversible, isolated change in a disposable derivative; preserve hashes and offsets.
6. Match clean vs patched inputs/screenshots, verify no side effects, and test FBNeo/netplay compatibility before community-facing claim.
7. Separately trace countdown sprite attributes/clear behavior and reject mask guesses without source-backed causality.

## Promotion and safety
GitHub stores human-readable docs, self-authored reusable scripts, small receipts and patch deltas. Keep full game ROMs, large captures and emulator redistributables on authorized local storage. This document records knowledge and pending leads; **no gameplay fix is being claimed**.
