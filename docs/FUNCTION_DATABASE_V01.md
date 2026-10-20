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
