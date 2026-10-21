# Historical roll recovery V03 — bounded runtime checkpoint

**Status: PARTIAL; success criterion not met.** Historical HBMAME execution is established, but no runtime-grounded roll/throw function or historical behavior difference has been verified. No gameplay patch, canonical ROM change, engine rebuild or project clone.

## Identity and admission
2026-10-21, Host02 DaltonsLaptop574, existing D:\AIOS_SFZ3MIX_V032, scope github:neohack2023/sfz3mix-re.
All six requested repository entry documents read. Local CURRENT_STATE predates GitHub historical reports; local AGENTS.md and historical V02 document returned ENOENT.
Fresh scope preflight and actual command admission returned READY_CONTINUE. Transient RESOURCE_CRITICAL and CONTEXT_PROJECTION_STALE blocks were respected; explicit context rebuild and subsequent admission succeeded. Resource blocking is not the final research blocker.

Canonical tools/sz3mx.03 SHA-256 verified before and after runner execution:
b5f7a1598e4f91a5113c506505b482b2cd1a19e366fe31471740e45dbd204691.
Disk audit: C: 110,916,485,120 free bytes; D: 39,845,888. Historical downloads/extraction/emulator staging used bounded C: temporary directories removed by TemporaryDirectory. Only small probes were added to existing D: tools. No historical ROM collection retained.

## Fresh historical verification and execution
Archive and CPU hashes match [V01 pins](HISTORICAL_023_027_COMPARISON_V01.md); 7z integrity PASS for each release.
HBMAME 0.289.3 lists dedicated drivers from hbmame/drivers/cps2t.cpp:
sfz3mix24, sfz3mix25, sfz3mix26.
Driver XML CRCs were matched to extracted program/assets, then member names adapted without changing bytes. CPU CRCs: 6b3cfa0c, 2ef2a33b, d97dcc03. Shared QSound dl-1425.bin was sourced locally and verified at CRC d6cf5ef5.

| Version | Frames | JSONL records | CPU state-write records | Distinct write PCs | Exit |
|---|---:|---:|---:|---:|---:|
| 0.24 | 3360 | 343 | 69 | 42 | 0 |
| 0.25 | 3360 | 343 | 69 | 42 | 0 |
| 0.26 | 3360 | 343 | 69 | 42 | 0 |

Log SHA-256:
- 0.24: a628dc5cc10a1fbc621b89ff9b5d4c54c12bc49271a57d243ae6dc8c0b5c8896
- 0.25: 3b630b1f3250625fc1e5b51602917d895cff965bf7d3c2d24ef0d67d471e77c6
- 0.26: 8b9fadb4c2484a21f488b41941b74386ed56df67021c5272da5fd2f4e7ee2273

These are execution observations, not accepted roll tests. Probe requests crouch/release, LP+LK pulses, a single punch and jump. It logs frame, requested input edges, candidate player coordinates/state/animation/selectors and CPU-originated writes. It does not verify input-port reads or identify characters by a release-specific field. State bytes inherited from v0.32 are hypotheses in historical versions.

Across the 16 selected state windows per version, coordinates, state/mode and selectors agree, while both animation pointers increase by 0x1A0 from 0.24 to 0.25 and 0xD4 from 0.25 to 0.26. This is a bounded relocation observation, not normalized executable-function equivalence. For example frame 3000 P1 animation 1161602 → 1162018 → 1162230; x=782,y=40,state=0x0202,mode=2 in each.

The tap snapshots report IR equal to program-space word at CURPC for only 20/69 samples in each version. **Do not interpret this diagnostic as opcode mapping parity or mapping failure:** IR timing during a bus callback has not been established, nor have these program-space words been compared independently to historical source bytes. Correct current-instruction attribution and debugger disassembly remain required before source reconstruction.

## Why behavior remains unverified
The inherited fixed-frame start sequence is not a demonstrated controlled match setup. A short v0.24 visual diagnostic completed at frame1002, with absolute-path screenshots at500 and1000: frame500 shows the world/intro transition; frame1000 shows character selection with INSERT COIN visible. Neither establishes delivered player control. The observed late state progression may include attract/demo behavior. Do not classify it as roll acceptance/rejection or infer a named move.

A 3360-frame v0.24 visual repeat produced the same JSONL hash as the first run, but its relative-path screenshots were not retained. The corrected 1002-frame diagnostic retained images locally; log SHA-256 6f750040f3577471325e1b8270a54920dcaee46fe11cc934970f6a50bb91439d.

No controlled landing/recovery/rejected-command coverage, paired throw attempt, defender immunity predicate, named Karin comparison, call/return chain or historical assembly parity was achieved. +0x21C remains unconnected to roll/throw immunity.

## Preserved failures and repairs
1. First staging attempt passed archive/CPU validation but failed because the mapper revisited an already moved member. Fixed with an existence check; no emulator run from that attempt.
2. Next attempt failed all three ROM audits on missing QSound device ROM. Added only the verified existing local member; successful runs followed.
3. Relative screenshot paths failed to retain images. Replaced with absolute paths for the short diagnostic.
4. First SQLite import launch was resource-blocked; after emulator completion the same import passed admission and completed. No blocked command was treated as executed.
Runner process exit0 alone is not acceptance: inspect each version's error, emulator exit, completion marker and log. Historical tools deliberately retain failed per-version receipts.

## SQLite
Existing evidence/functions_v01.sqlite updated transactionally with three rows in historical_execution_trials_v03. Evidence class BOUNDED_EXECUTION_ATTEMPT_NOT_GAMEPLAY_VALIDATED; roll_verified=0; function_owner=NULL. No previous function IDs, ownership, instructions or observations changed.
All42 pre-existing tables matched row digests before/after; integrity_check=ok; foreign_key_check empty. Backup via SQLite backup API at C:\AIOS\_TEMP\SFZ3MIX_V03_EVIDENCE_RETRY02\functions_v01_before_historical_v03.sqlite. No new function relationship or reconstructed region promoted.

## Decision gates
| Gate | Status | Boundary |
|---|---|---|
| 1. v0.24/v0.25 executable comparison | PARTIAL | Verified sources, executable runs and relocated state-write sites; no normalized function comparison |
| 2. Roll behavior reproduced in both | BLOCKED | Controlled match/input delivery not established |
| 3. Roll-eligibility function identified | BLOCKED | No delivered command → branch → outcome trace |
| 4. v0.25/v0.26 throw-immunity comparison | PARTIAL | Both execute; no equivalent controlled throw trials |
| 5. Throw-eligibility function identified | BLOCKED | No throw-decision trace |
| 6. Recovered historical assembly parity | BLOCKED | No function promoted or source parity claimed |
| 7. Karin delay reproduced/measured | BLOCKED | No matched Karin/control test |
| 8. SQLite and GitHub publication | PASS | Trial-only transactional import and sanitized tools/docs; no ROM data |

## Reproduction and exact next target
[Probe](../tools/historical_boot_inputs_v03.lua), [runner](../tools/run_historical_boot_inputs_v03.py), [transactional trial importer](../tools/ingest_historical_trials_v03.py), [boot visual probe](../tools/historical_visual24_v03.lua), [visual runner](../tools/run_historical_visual24_v03.py).
Read-only probes alter input fields only, never game RAM. Each emulator subprocess capped at90 seconds, network requests60 seconds, log1000 records, minimum C: free space2GiB. Existing output directories are protected by receipt-existence assertions. Raw evidence/backup paths are local and provisional; small sanitized summaries are in GitHub.

**No verified next gameplay modification candidate exists.** Smallest next harness change: replace fixed boot input frames with readiness-triggered coin/start/selection, log effective input-port values, and require a visible controlled neutral crouch→stand response. Establish deterministic characters and suppress no game state by RAM forcing. Then test LP+LK in neutral and after a measured landing on v0.24/v0.25. Trace the first executed eligibility branch and resulting state/animation divergence, with historical data/opcode mapping independently verified. Recover only that bounded region into assembly afterward. Preserve original FBNeo-compatible ROM format.
