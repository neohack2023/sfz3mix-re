# Current state: Street Fighter Zero 3 Mix v0.32
Updated: 2026-10-20 — Collision Engine Recovery V02.

## Authority and primary artifact
Scope github:neohack2023/sfz3mix-re; Host02 DaltonsLaptop574; existing workspace D:\AIOS_SFZ3MIX_V032 / token sfz3mix-v032.
Drive governs routing/registration; GitHub owns repository implementation; Host02 retains execution evidence.
Per-command preflight returned READY_CONTINUE throughout accepted execution. No registration change.
Existing tools/sz3mx.03 SHA-256 b5f7a1598e4f91a5113c506505b482b2cd1a19e366fe31471740e45dbd204691 verified unchanged before/after.
No extraction, clone, gameplay modification or original-ROM write.

## Latest verified recovery
[Engineering receipt](COLLISION_ENGINE_RECOVERY_V02.md), [machine-readable evidence and parity](COLLISION_ENGINE_RECOVERY_V02.json).
- FUNC_REC_02C17E is callable from02C07E, returns02C082; three calls to FUNC_REC_02C19A and one final fallthrough share the existing seven leaf blocks.
- Wrapper prefix28bytes, dual-record block36bytes, selector-update block38bytes all source-authored GNU assembly byte-exact. Existing72-byte V01 leaf source unchanged.
-67 traced instructions establish wrapper/leaf paths, inactive object slots and both sign paths. Stack debugger snapshots remain inconclusive.
-180 bounded operand rows across frame_done intervals2939..2946. Twenty +21C writes, zero reads: bounded negative consumer result.
-029A10 chain reobserved: +CB selectors and +9C pointers lead to record offsets+2/+6. Vertical interval math established; broader push/contact/correction behavior unresolved.
-All seven prior unowned sites now have block/confidence assessments; function IDs stay null.
-SQLite61 functions/80 calls; seven shared-block memberships, four wrapper blocks,180 new operand observations. Transactional backup and integrity/FK checks PASS. Old knowledge preserved; three call owners updated with runtime proof.

## Storage and limits
Final D: free161,480,704 bytes (~154MiB). A debugger disassembly-length expression interpreted A6 as a register and produced an oversized local export. Failure preserved; validator streams explicit ranges; probe corrected to0x expressions but not rerun. Stop extra captures until storage is rechecked.
No +21C consumer, zero-selector case, exhaustive indirect-call inventory, or owning function for029A10 is established.
Community hitboxes issue remains OPEN; no fix for hitboxes, Karin rolling or Alpha Counter effects.

## Preserved findings
Original59 candidates/76 static calls remain historical discovery metrics. Original50-sample/nine-site trace and20 decoded samples/16distinct old records retained.
Player basesFF8400/FF8800, spacing400; projectileFF9400/stride100 remains spawn-untested.
V01 FUNC_REC_02C19A and72-byte parity remain valid. No whole-ROM code/data separation or FBNeo/hardware acceptance claimed.

## Next target
Find static +21C read candidates and choose a bounded reaching scenario. Establish the029A10 chain's callable entry, then observe overlap-positive behavior.
Use existing evidence/functions_v01.sqlite; never replay migrations over backups or seed-rebuild the database. Shared body memberships must be queried explicitly.
[Knowledge index](KNOWLEDGE_INDEX.md), [DB/query guide](FUNCTION_DATABASE_V01.md), [community TODO](../TODO.md).
