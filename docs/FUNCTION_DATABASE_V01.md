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
