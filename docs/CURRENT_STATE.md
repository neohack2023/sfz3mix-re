# Current state: Street Fighter Zero 3 Mix v0.32
Updated: 2026-10-20.

## Mission and authority
Preserve the original FBNeo/HBMAME-compatible CPS2 ROM. No standalone recompilation or clone.
Canonical scope `github:neohack2023/sfz3mix-re`; Host 02 workspace token `sfz3mix-v032` → `D:\AIOS_SFZ3MIX_V032`.
Drive owns governance/routing, GitHub live repository implementation, Host 02 local execution evidence. [Registration and preflight recovery](AUTHORITY_RECOVERY_2026-10-20.md) passed. Per-command preflight remains mandatory and returned READY_CONTINUE in the latest work.

## Primary artifact and integrity
Use existing `tools/sz3mx.03`, SHA-256 `b5f7a1598e4f91a5113c506505b482b2cd1a19e366fe31471740e45dbd204691`, verified unchanged before/after this run. Do not unzip or re-extract the distribution archive.
D: began this run with 434,110,464 free bytes (~414 MiB), recovering from the earlier storage warning. Recheck before execution; no further cleanup performed.

## Latest verified collision recovery
[Recovery and test receipt](COLLISION_RECOVERY_V01.md), [machine-readable reconstruction](COLLISION_RECONSTRUCTION_V01.json), [assembly parity](COLLISION_ASSEMBLY_PARITY_V01.json).
- `FUNC_REC_02C19A`: callable entry `0x02C19A`, exit RTS `0x02C1E0`, end-exclusive `0x02C1E2`; 26 instructions, seven blocks.
- Direct BSR targets plus runtime entry/RTS/return prove this entry-bounded region. It shares a tail with the wrapper at `0x02C17E`; exclusive ownership/all incoming callers remain unproved.
- `0x02C1AC` reads the opponent +0x9C pointer; +CB selector scales by eight. Live record reads at `0x0F2AE2` and `0x0D65D0` prove X-offset/radius-X use. Four observed output calculations match game-originated writes to receiver+0x21C.
- Source-authored GNU M68000 assembly reassembles all 72 bytes exactly; no mismatches, no ROM patch.
- SQLite now contains 60 functions (59 old candidates preserved), 79 calls (76 old preserved), eight verified function-RAM xrefs and four function-data xrefs. Two old trace instruction sites now have an entry-bounded owner; other seven remain unresolved. Integrity/FK checks pass.

## Preserved findings and limits
The original 50-sample trace (31 reads, nine sites), 20 decoded box samples / 16 distinct old addresses, player bases 0xFF8400 and 0xFF8800 / stride0x400 remain preserved. Projectile pool 0xFF9400 / stride0x100 remains spawn-untested.
The continue score symptom is reproduced, not fixed. Earlier 26-byte assembly parity remains valid. Static CFG counts (839 candidate instructions / 414 edges / 59 initial entries) are historical discovery metrics, not whole-ROM coverage.
No community issue is fixed. Full code/data separation, complete opcode mapping, visual hitbox semantics, FBNeo rollback/netplay and physical hardware acceptance remain untested.

## Next execution target
Verify wrapper entry/call ownership and the seven remaining reader sites; trace downstream consumers of +0x21C and exercise inactive/zero-selector branches in a bounded scenario. Preserve existing evidence names and database backups. Do not infer function ownership from nearest addresses or begin unrelated gameplay patches.
Use [knowledge index](KNOWLEDGE_INDEX.md), [function database](FUNCTION_DATABASE_V01.md), [community TODO](../TODO.md) and repository AGENTS.md. The D: workspace is the existing runtime/artifact location; do not clone into it.
