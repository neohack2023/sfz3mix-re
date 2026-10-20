# Authority recovery and collision trace handoff — 2026-10-20

Status: BLOCKED / NO RUNTIME TRACE. This receipt records read-only diagnosis, not recovered execution authority.
Host: WINDOWS_EXECUTION_HOST_02 / DaltonsLaptop574, device b2b68f35-3656-4385-9dce-b60e3d9e3e78.
Repository baseline observed: 51ca3dcc22b87ef39fd0b8e513a7fb8ddd8eb4f8.
Existing target: D:\AIOS_SFZ3MIX_V032, v0.32. No clone or subproject created.

## Findings and evidence boundaries

- The current [Drive Project Scope Registry](https://docs.google.com/spreadsheets/d/1qOLbOwA3greC_PmauIq4HrGeuauCjBIE8EbXKpIX2Do/edit) was fetched (52,467 characters, 155 lines). No SFZ3, sfz3mix-re, Street Fighter, or AIOS_SFZ match exists in its returned content. Drive searches for sfz3mix and sfz3 returned no results. Current [migration ledger](https://docs.google.com/spreadsheets/d/183iLRCmf3l5nuftdsCeqHAEV5SZYHEbv49NHYbbsRL0/edit) returned 16,174 characters and no matching project reference. These observations establish no_match in the inspected registry, not absence from every possible archive.
- GitHub AGENTS.md independently says a dedicated SFZ3 scope has not yet been confirmed. Missing canonical registration is supported; a stale registered binding is not established.
- Direct filesystem listing confirmed the existing workspace, tools/sz3mx.03, evidence/functions_v01.sqlite, prior RAM receipts and HBMAME runtime. Root AGENTS.md read returned ENOENT. The D: runtime workspace is not shown to be a Git checkout; do not initialize or clone one to address this.
- Host entry contract was read at C:\AIOS\HOST02_AGENT_ENTRY_CONTRACT.md and its registry pointer. Host execution truth does not grant canonical project authority.
- Partial workspace-registry.json read showed safe_roots=[C:\AIOS]. Remaining projects/workspaces and actual root admission were not obtained. D: path admission is a separate required check, not a confirmed cause of the authority failure.
- Existing Repair-PCGameRE-ScopeBinding.ps1 was inspected as historical workflow evidence only; it was not executed or adapted. It must not be used to map SFZ3 to the unrelated PC scope.
- Prior invocation in the preceding attempt returned BLOCK_AUTHORITY | CANONICAL_SCOPE_UNRESOLVED. No authorized preflight result exists for SFZ3 in this recovery attempt.
- Host went offline during configuration reads at approximately 2026-10-20T21:33Z. Pending workspace-registry continuation call 520c1a52-80c2-427f-9864-055b13afad69 failed with MCP -32000 Connection closed. Contract read 8e9ce620-b34f-421e-9c04-b7db18c6f8ee remained executing at last status check; resolve it before retrying that read.
- All six requested repository entrypoints were read in order on GitHub. Existing findings remain unchanged: 59 candidate functions, 76 calls, 20 decoded samples / 16 distinct records, zero verified function-RAM xrefs. These counts are prior tested repository facts, not a new live SQLite audit.

## Execution receipt

No shell command, emulator launch, trace script, hash audit, SQLite query/migration or gameplay mutation was executed in this recovery attempt. Host interaction used list_devices, read_file, list_directory and get_tool_result only. Drive/GitHub reads and sanitized repository documentation publication are the only other operations.

Reads: D:\AIOS_SFZ3MIX_V032\AGENTS.md (ENOENT); D:\ and existing workspace directory listings; C:\AIOS\00_REGISTRY\HOST02_AGENT_ENTRY_CONTRACT.json; host entry contract; DESKTOP_COMMANDER_HARDENED_01 workspace registry (first 220 lines only) and Repair-PCGameRE-ScopeBinding.ps1; directory listings for the hardened runner and AIOS_SYNC. Read of current-runtime.txt failed because no device was online.

Runtime observations captured: 0. Verified new function relationships: 0. Hypotheses about stale mapping, missing projection or actual router implementation remain inconclusive. No community fix accepted.

ROM integrity: NOT RECHECKED. Expected CPU SHA-256 remains b5f7a1598e4f91a5113c506505b482b2cd1a19e366fe31471740e45dbd204691.
Disk space: NOT RECHECKED. Prior documented D: free bytes 39,845,888 is stale and insufficient as a current execution gate.
Database integrity/FKs: NOT RECHECKED; no migration or DB write performed.
Documentation validation: proposed record is explicitly non-authoritative, no ROM bytes/dumps included, prior findings preserved, repository paths/link targets checked against fetched entrypoints. No code test PASS claimed.

## Smallest proposed registration — NOT APPLIED

```json
{
  "proposal_status": "REVIEW_ONLY_NOT_REGISTERED",
  "proposed_scope_key": "github:neohack2023/sfz3mix-re",
  "chatgpt_project_name": "Street Fighter Zero 3 Mix",
  "aliases": ["SFZ3 Mix", "SFZ3 Mix v0.32"],
  "project_type": "Repository-backed ROM reverse engineering",
  "parent_scope_proposal": "global-working-memory",
  "repository": "neohack2023/sfz3mix-re",
  "host_id": "WINDOWS_EXECUTION_HOST_02",
  "workspace": "D:\\AIOS_SFZ3MIX_V032",
  "version": "v0.32",
  "authority_state": "proposed_unregistered",
  "verification_status": "pending_governance",
  "project_folder_id": null,
  "project_handoff_file_id": null,
  "retrieval_index_file_id": null,
  "authority_transfer": false,
  "execution_authorized": false
}
```

The proposed key is a candidate for authority review, not a manufactured canonical identity. Do not activate a local entry declaring drive_authoritative before its Drive registration/object authority is verified.

Smallest missing authorization requirement: the designated AIOS governance workflow must approve/register an exact project identity and binding to this existing repository/workspace, with current handoff/index pointers and an explicit bounded read-only execution lane. The task authorizes preparing this proposal, not inventing canonical approval when no valid record exists. No existing registry or runtime policy was altered.

## Ready-to-resume sequence

1. Reconnect Host 02 and resolve pending read status. Re-read full workspace registry, workspace-aware contract, current runtime pointer and active preflight projection/config. Determine all consumers before any change.
2. Through the established governed registration workflow, resolve/approve this proposal or a verified successor. Preserve backups and record exact changed fields and authority receipt. Mirror only that verified binding into the existing local router. Admit only the exact D:\AIOS_SFZ3MIX_V032 path where required, not all of D:. Do not disable preflight or inherit another scope.
3. Require actual preflight authorization for this exact project/workspace. No trace until PASS/authorized result is captured.
4. Hash existing tools/sz3mx.03 and verify free disk space before execution. Use no ZIP extraction, no large capture and no cleanup by inference. Inspect tools/ram_trace.lua, pc_trace.lua, debugger_api_probe.lua and memory_api_probe.lua before choosing the supported bounded watchpoint/trace API and existing deterministic input sequence. Exact launch command remains to be derived from those local tools; no untested command is presented as executed.
5. Observe CPU reads/writes overlapping P1 0xFF8490..93 / 0xFF849C..9F, P2 0xFF8890..93 / 0xFF889C..9F; selectors 0xFF84C8..CB / 0xFF88C8..CB. Watch byte/word overlaps as well as long accesses. Separate debugger observer reads from CPU-originated accesses. Capture pre/post instruction PC semantics, opcode evidence, effective address, width, value/mask, frame and gameplay state. Correlate pointer plus selector*8 with ROM record reads only when the trace establishes it.
6. Verify opcode-fetch mapping independently of program-data mapping. Attribute ownership only after function entry/extent and control flow are proven. Unowned runtime instructions remain observations with null function owner.
7. Inspect existing DB schema; back up under a bounded storage budget, then add observations and verified links transactionally to the existing functions_v01.sqlite. Never rebuild over it. Preserve 59/76 and existing RAM records; run integrity_check and foreign_key_check after each accepted migration.
8. Commit only tested sanitized tooling/schema/docs and receipt, with raw traces, ROM bytes and emulator artifacts kept local. Update CURRENT_STATE and KNOWLEDGE_INDEX; leave hitboxes issue open.

## Final read-status reconciliation
The pending workspace contract call 8e9ce620-b34f-421e-9c04-b7db18c6f8ee subsequently completed (2026-10-20T21:34:15Z). Its documented contract permits absolute cwd only inside approved roots and describes automatic discovery limited to direct children of C:\AIOS\04_WORKSPACES. This document describes implementation pending activation and is not proof of current activation. A fresh workspace-registry continuation read f43cbb11-d60a-4e2c-a6b5-77411543194d failed with Connection closed at 21:35:18Z. No registry read remains pending from this attempt. A subsequent current-runtime.txt read succeeded and returned versions\\0.2.51; active runtime source and full configuration still require inspection. Host connectivity was intermittent, not a proven persistent outage. The published CURRENT_STATE and KNOWLEDGE_INDEX edits both passed exact content readback. No execution authority or trace was obtained.


## Governed registration completed — 2026-10-20, 18:16 EDT

This successful continuation supersedes the BLOCKED current-state label above; earlier failure evidence remains historical.

- User explicitly approved scope github:neohack2023/sfz3mix-re, existing workspace D:\AIOS_SFZ3MIX_V032, Host 02, authority split and bounded tracing/SQLite permission.
- Parent global-working-memory verified in Drive REGISTRY row 2: Active, drive_authoritative, passed; its root and current handoff resolved.
- Exact identity dedup: no existing scope/alias or Memory Object Registry match; no new execution workspace, clone or second project identity.
- Authoritative registration saved and all 22 cells read back exactly in REGISTRY!A24:V24:
  https://docs.google.com/spreadsheets/d/1qOLbOwA3greC_PmauIq4HrGeuauCjBIE8EbXKpIX2Do/edit#gid=14783079&range=A24:V24
- Existing-scope Drive branch: https://drive.google.com/drive/folders/1V_7jBQBiN_wZgkJ43F_sHFZ70m1PmCme
- Verified handoff: https://drive.google.com/file/d/18hnN1BPu_7ZLzR6ZtYUbcFa0nY8qRRhK/view?usp=drivesdk
- Verified retrieval index: https://drive.google.com/file/d/1UBYu4F4wRvND-1kuTV3OedujlJ8IwhGM/view?usp=drivesdk
- Host workspace token sfz3mix-v032 points to the existing D: workspace and canonical scope. Added only that exact safe root, workspace/project entry and context binding. All unrelated JSON fields preserved; backups verified byte-identically before mutation.
- Backups: C:\AIOS\09_REMOTE_RUNNER\DESKTOP_COMMANDER_HARDENED_01\workspace-registry.json.pre_sfz3mix_20261020T221554Z.bak and C:\AIOS\02_RUNTIMES\AIOS_KNOWLEDGE_CONTEXT_RUNTIME_01\registry\scope-bindings.json.pre_sfz3mix_20261020T221554Z.bak.
- The local registry is approximately 60 MB despite 29 workspace entries; it parsed successfully. Its unrelated large content was preserved, not cleaned or diagnosed in this task.

### Canonical preflight PASS

Ran:
C:\Python314\python.exe C:\AIOS\02_RUNTIMES\AIOS_KNOWLEDGE_CONTEXT_RUNTIME_01\host_context_runtime.py build --workspace sfz3mix-v032

Then:
C:\Python314\python.exe C:\AIOS\02_RUNTIMES\AIOS_HOST_INTELLIGENCE_01\unified_preflight.py --workspace sfz3mix-v032 --objective "bounded read-only Motorola 68000 collision-memory trace" --target sfz3mix-v032 --stage pre-exec --task-class LIGHT --require-fresh --command "HBMAME read-only collision-memory probe"

Result READY_CONTINUE / ALL_REQUIRED_PREFLIGHT_COMPONENTS_PASS, exit 0, scope VERIFIED, context FRESH.
Receipt C:\AIOS\02_RUNTIMES\AIOS_HOST_INTELLIGENCE_01\state\preflight\20261020T221640Z-39dfd3da7743.json.
The actual Desktop Commander trace launch and DB migration independently returned the same authorized verdict. No preflight rule was disabled.

### Collision trace PASS, function ownership unresolved

HBMAME 0.289.3 executed existing sfz3mix runtime with:
hbmame.exe sfz3mix -rompath D:\AIOS_SFZ3MIX_V032\runtime_hbmame\roms -skip_gameinfo -nothrottle -video none -sound none -debug -debugger none -autoboot_delay 0 -autoboot_script D:\AIOS_SFZ3MIX_V032\tools\collision_access_v01.lua -seconds_to_run 65

Launched by C:\AIOS\09_REMOTE_RUNNER\RUN_SFZ3MIX_COLLISION_V01.py, cwd runtime_hbmame; 90-second subprocess limit. Exit 0, elapsed 14.2 seconds; finished 3100 frames with 50 distinct samples at nine sites (31 READ, 19 WRITE). Samples are deduplicated by kind/address/CURPC/data, not total access counts. Filtered window 2940..3060, established boot/select inputs plus P1 button pulses at 2960 and 3000. ATTACK_WINDOW labels input schedule, not proof of contact/hit.

Taps return nil, preserving bus data. Observer snapshot reads are guarded against recursive attribution; taps removed before debugger disassembly. CURPC identifies current instruction start separately from in-progress PC register. No game RAM or CPU state writes by the observer; WRITE samples are game-originated writes.

| PC | Observed instruction |
| --- | --- |
| 0x027EDA | move.l ($c8,A1), (-$5cd6,A5) |
| 0x027EF0 | movea.l ($90,A1), A2 |
| 0x029A10 | move.b ($cb,A6), D0 |
| 0x029A1A | move.b ($cb,A4), D1 |
| 0x029A42 | movea.l ($9c,A6), A0 |
| 0x029A46 | movea.l ($9c,A4), A1 |
| 0x02C1A6 | move.b ($cb,A4), D0 |
| 0x02C1AC | movea.l ($9c,A4), A0 |
| 0x02F666 | move.l (A0), ($c8,A6) |

Example: frame 2940, PC 0x02C1AC reads P2 pointer words at 0xFF889C (0x000F) and 0xFF889E (0x2ACA), consistent with pointer 0x000F2ACA. The same instruction reads P1 0xFF849C/9E. Selector byte +CB is reported on aligned bus address +CA with mask 0x00FF; ingestion normalizes to the accessed low byte. All nine debugger-disassembled instruction byte sequences match exact offsets in hash-verified sz3mx.03; IR agrees with the first opcode word. This proves those observed instruction mappings only, not whole-program opcode parity.

Raw evidence stays local:
- evidence/collision_access_v01.tsv (6,994 bytes), SHA-256 4c099e68554cc200d265b6ea4d108e23136a38f6df6b61577384655917b5762f.
- evidence/collision_pc_*.txt: nine bounded disassembly snippets.
- evidence/collision_access_validation_v01.json.
- evidence/collision_access_db_receipt_v01.json.

Existing SQLite additively extended by tools/ingest_collision_access_v01.py: runtime_collision_instructions (9), runtime_collision_accesses (50), runtime_collision_access_fields (74), runtime_collision_issue_links (9). Links reference existing player slots/fields, evidence and hitboxes issue. All function owners remain null; existing function_ram_xrefs stays 0. The 59 candidates, 76 calls, existing fields and 20 box decodes remain byte-value identical at row level. Backup evidence/functions_v01_before_collision_access_v01.sqlite created using SQLite backup API.

Pre/post migration integrity_check=ok, foreign_key_check empty. Three mask-normalization assertions passed. Ingest validates trace hash, completion marker, instruction mapping and source ROM hash before transaction. No rerun accepted over an existing backup.

CPU SHA-256 reconfirmed after execution: b5f7a1598e4f91a5113c506505b482b2cd1a19e366fe31471740e45dbd204691. No original ROM change or gameplay patch. Hitbox issue remains open.

Remaining: verified function extent/call ownership, direct accesses to selected ROM box records, collision semantics/contact tests and reproducibility across another run. Do not infer ownership from nearby candidates. Preserve this run's output before any repeat because the probe opens its fixed output paths for writing. D: decreased from 39,845,888 to 29,360,128 free bytes across this session; trace TSV is only 6,994 bytes, and the cause of the larger decrease was not established. Recheck space before further execution; no cleanup authorized/performed.
