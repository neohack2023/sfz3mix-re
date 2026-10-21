# Function knowledge database V01

## Purpose
Searchable SQLite index for recovered and candidate SFZ3 Mix v0.32 Motorola 68000 functions. It is a local **derived database**, rebuildable from GitHub's sanitized registry and the optional local CFG. It does **not** contain copyrighted ROM machine-code bytes.

## Implemented and validated on Host 02, October 20, 2026
- Script: [`tools/function_db_v01.py`](../tools/function_db_v01.py)
- Database location: `D:\AIOS_SFZ3MIX_V032\evidence\functions_v01.sqlite`
- Inputs: [sanitized function candidate registry](FUNCTION_REGISTRY_V01.json) and local `evidence/m68k_cfg_v02.json`.
- Result: **59 function candidates**, **76 static direct-call relationships**, **8 community issues**, **4 candidate-to-community-issue associations**. All 76 call sites have unknown caller function ownership, so caller links remain null rather than invented.
- A tested query for `0x00331C` returns `FUNC_CAND_0026`, with mapping level `SAMPLED_MAPPING_ONLY`, `LOW` confidence, unresolved function bounds, and issue `continue-score` as an **investigative association, not causal proof**.

## Schema
- `functions`: stable ID, CPU address and address-space identity, original program member, nullable byte offset, mapping status, name, role, confidence, runtime confirmation, bounds confirmation, source notes.
- `calls`: optional caller and callee function IDs, instruction site address, target address, direct/indirect type, confidence and evidence reference.
- `issues` and `function_issues`: normalized community request registry, source post, and relationship type.
- `evidence` and `function_evidence`: cited source URI, evidence type, evidence validation status, role of evidence.
- `metadata`: original archive SHA-256, CPU SHA-256 and registry provenance.
- Indexes support address, caller, callee and issue-backed lookups.

## Build and query
```powershell
python D:\AIOS_SFZ3MIX_V032\tools\function_db_v01.py build --registry D:\AIOS_SFZ3MIX_V032\evidence\function_registry_sanitized_v01.json --cfg D:\AIOS_SFZ3MIX_V032\evidence\m68k_cfg_v02.json --database D:\AIOS_SFZ3MIX_V032\evidence\functions_v01.sqlite
python D:\AIOS_SFZ3MIX_V032\tools\function_db_v01.py query --database D:\AIOS_SFZ3MIX_V032\evidence\functions_v01.sqlite --term 0x00331C
```
Build refuses to overwrite an existing database. Produce a new version or reconcile a deliberately retained copy before rebuilding. Search accepts hex CPU addresses and function/issue-text terms. JSON query output includes evidence, issues and relationships.

## Promotion rules
- `LOW` and `UNVERIFIED_STATIC_ENTRY_CANDIDATE` are the default for current import. Do not infer code/data or functions from a decoder result alone.
- Do not populate `file_offset` merely from a CPU address: exact mapping must be verified at that location; separate data-space matching from fetched opcodes.
- A known direct call target does not establish **which function owns the call site**; `caller_id` stays null until verified function boundaries.
- Confirm opcode mapping, live traces, register effects, call ownership and function extent before promoting a candidate to recovered.
- The database is a search cache, **not** the sole authority. Keep the canonical sanitized registry and dated execution receipts versioned in GitHub, and local raw evidence on Host 02.
- Store new discoveries with immutable evidence references and stable function IDs. Update [current state](CURRENT_STATE.md) and [knowledge index](KNOWLEDGE_INDEX.md) after test-backed advancement.

## Runtime SFA3 RAM profile extension (2026-10-20)
[Runtime report](SFA3_RAM_COMPATIBILITY_V01.md) and [machine-readable profile](SFA3_RAM_PROFILE_V01.json) record dynamic player structures and verified 8-byte box-table-shaped data. Host 02 database additively includes `ram_structures`, `ram_slots`, `ram_fields`, `ram_observations`, `ram_issue_links`, `ram_box_decodes`, and empty `function_ram_xrefs`. Integrity and FK checks passed. Existing function/call records preserved. Do **not** populate xrefs merely from a RAM address or from data table decoding: record the actual 68000 instruction and confirmed function ownership first.

## Collision reconstruction extension (2026-10-20)
[Validated reconstruction](COLLISION_RECOVERY_V01.md) adds FUNC_REC_02C19A at CPU/file offset 0x02C19A, end-exclusive 0x02C1E2. This is an entry-bounded callable region with a shared wrapper tail; ownership is not asserted exclusive. All original 59 candidate rows and 76 call rows remain unchanged.

Additive tables:
- `function_basic_blocks`: seven blocks with exclusive end addresses and evidence.
- `function_instructions`: 26 instruction memberships, sizes, mnemonic text, runtime visitation and mapping status; no machine-code bytes.
- `function_cfg_edges`: direct conditional/fallthrough relationships, separately marking runtime-observed transitions.
- `function_reconstructions`: assembly source, parity receipt, hashes, bounds and limitations.
- `function_operand_accesses`: 44 local CPU operand observations; 16-bit bus masks preserve byte/word distinctions.
- `function_data_xrefs`: four proven record-field readers for two data records.

Existing `functions`, `calls`, `evidence`, `function_evidence`, `function_issues`, `ram_fields`, `function_ram_xrefs` and prior runtime instruction records are extended/reconciled. Totals: 60 functions, 79 calls, eight function-RAM xrefs. The first two original collision instruction sites now point to the recovered region; seven remain null. The `hitboxes` link is investigative, not a fix. Four added RAM fields document +0 active marker, +0x38 opponent word, +0x2C9 orientation condition and +0x21C output; visual semantics remain bounded.

Migration: [ingest_collision_reconstruction_v01.py](../tools/ingest_collision_reconstruction_v01.py). It requires the locally verified reconstruction and preserved traces, backs up via SQLite API, uses one transaction, checks original-row preservation and runs integrity/FK checks before/after commit. It refuses repeat ingestion. The original V01 builder is the historical seed importer and does not rebuild all runtime extension tables; do not overwrite the existing database.

Search the recovered function with the existing query command, using `--term 0x02C19A`. Join `function_instructions` on `cpu_pc=0x02C1AC` to resolve its entry-bounded owner. Join `function_data_xrefs` to `ram_box_decodes` by `record_address=entry_address` when comparing earlier sampled records; absence in an old snapshot is not absence of a live read.

## Collision Engine Recovery V02 extension
[Receipt](COLLISION_ENGINE_RECOVERY_V02.md), [registry/parity](COLLISION_ENGINE_RECOVERY_V02.json), [migration](../tools/ingest_collision_engine_v02.py).
Existing DB now61 functions/80 calls. FUNC_REC_02C17E owns four prefix blocks/seven instructions and references the seven existing FUNC_REC_02C19A blocks through function_shared_blocks. Shared instructions are not duplicated.
Three existing calls gain their proven wrapper caller; a new call at02C07E has unknown containing caller. All other previous rows are preserved.

Additional tables:
- function_shared_blocks: function→existing block membership with evidence.
- function_control_relationships: direct calls and shared fallthrough, independently marking runtime proof.
- function_contracts: register/stack evidence and limits.
- collision_reader_assessments: seven proven sites with bounded block descriptions and null function owners.
- runtime_collision_dependencies:180 CPU bus observations; masks retain byte/word/longword-transfer distinction.
- collision_data_dependencies: four actual vertical record readers (+2/+6), owners unresolved.
- assembly_region_reconstructions: three exact source-authored regions, hashes and evidence.

Backup evidence/functions_v01_before_collision_engine_v02.sqlite passes integrity/FKs; transaction checks preserved rows and integrity/FKs before/after commit. Migration refuses replay.
Twenty +21C writes and zero reads across intervals2939..2946 are a bounded negative consumer result. Never infer nonuse outside this scenario.

```sql
SELECT f.id,b.id,b.start_address,b.end_exclusive
FROM function_shared_blocks s JOIN functions f ON f.id=s.function_id
JOIN function_basic_blocks b ON b.id=s.block_id;
SELECT cpu_pc,function_id,confidence FROM collision_reader_assessments;
SELECT cpu_pc,kind,address,bus_data,bus_mask,frame
FROM runtime_collision_dependencies WHERE address IN (0xFF861C,0xFF8A1C);
SELECT * FROM collision_data_dependencies;
```
Historical builder/earlier row counts above describe earlier checkpoints. Do not rebuild over the extended DB.

## Downstream consumer V03 extension
[Receipt](COLLISION_CONSUMER_V03.md), [machine registry](COLLISION_CONSUMER_V03.json).
61functions/80calls remain unchanged: REGION_037A56 is reader-anchored and has null function ownership.
New tables collision_consumer_regions/instructions/blocks/edges/sites and collision_scenario_summaries retain14instructions,6blocks,10sites and five input-phase summaries.
assembly_region_reconstructions gains44-byte exact parity; runtime_collision_dependencies gains187observations (147reads/40writes).
All original rows remain exact; four successful prior assembly sources are hash-protected.
Backup evidence/functions_v01_before_collision_consumer_v03.sqlite and DB pass integrity/FK checks.

```sql
SELECT * FROM collision_consumer_regions;
SELECT cpu_pc,function_id,region_id FROM collision_consumer_sites;
SELECT source_pc,target_pc,runtime_proven FROM collision_consumer_edges;
SELECT cpu_pc,frame,address,bus_data FROM runtime_collision_dependencies
WHERE evidence_id='collision-consumer-v03' AND kind='READ' ORDER BY id;
```
Input labels identify issued controls, not validated move names. Snapshot edge values precede a game write; bus_data is the new value. Prefetched IR at other callbacks is not their opcode proof.
The near branch and the caller consuming D0 are unresolved. No hitbox issue is fixed.

## V04 callable ownership and negative success-path tests
[Receipt](COLLISION_DECISIONS_V04.md), [registry](COLLISION_DECISIONS_V04.json).
FUNC_REC_037A46 is a runtime-confirmed callable enclosing existing REGION_037A56.
New function_consumer_region_memberships and collision_region_ownership_claims reference V03's existing region/instructions. No old rows are rewritten.
Three prefix blocks/five instructions join the fourteen shared consumer instructions. Shared false returns remain nonexclusive.
Totals62functions/83calls; three new calls, five parity regions,200 operands from two complete trials.
The first prototype's600-event partial log is not imported as a complete trial.

New collision_decision_trials, collision_state_move_observations and collision_decision_dataflow retain confidence, negative outcomes and static/runtime distinctions.
All old rows and five earlier assembly sources passed preservation checks. SQLite backup evidence/functions_v01_before_collision_decisions_v04.sqlite and integrity/FKs PASS.

```sql
SELECT r.id,COALESCE(o.function_id,r.function_id) AS current_entry_bounded_owner
FROM collision_consumer_regions r
LEFT JOIN collision_region_ownership_claims o ON o.region_id=r.id;
SELECT * FROM collision_decision_trials;
SELECT * FROM collision_state_move_observations;
SELECT * FROM collision_decision_dataflow;
```
Selector0/+21E and mode6 success dataflow is byte-verified static evidence; successful application was not observed. Do not label a gameplay mechanic or fix.
