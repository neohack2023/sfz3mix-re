# Current state: Street Fighter Zero 3 Mix v0.32

## Authority and integrity
Scope github:neohack2023/sfz3mix-re; Host02 DaltonsLaptop574; existing D:\AIOS_SFZ3MIX_V032 / token sfz3mix-v032.
Drive governs scope; GitHub owns tested implementation; Host02 holds local raw evidence.
Canonical preflight READY_CONTINUE throughout accepted V03 tests.
ROM tools/sz3mx.03 SHA-256 b5f7a1598e4f91a5113c506505b482b2cd1a19e366fe31471740e45dbd204691, unchanged before/after.
No clone, extraction, ROM patch or gameplay modification.

## Latest milestone: first downstream consumer
[Collision consumer V03 receipt](COLLISION_CONSUMER_V03.md) and [machine-readable reconstruction/parity](COLLISION_CONSUMER_V03.json).
- Actual read037A56 at receiver+21C, value273; traced unsigned>=48 branch returnsD0=0.
- Region[037A56,037A82),14 instructions/6blocks,44 source-authored bytes reassemble exactly.
- The region gates a Boolean opponent-state/animation predicate. Containing function/caller purpose and near-success path remain unresolved; it is not promoted as a new function.
- Triggered baseline/approach/attack-input/retreat/release phases:147 CPU reads across10sites,40 sampled output writes. All40 match the V01 arithmetic.
- +21C is an absolute horizontal word-distance from receiver X to a computed opponent edge; no physical push correction or hitbox fix established.
- Original180 observations preserved:20 rising writes with fixed selectors/records. Exact old named gameplay states were not captured. New baseline reproduces first8writes with raw state/animation/coordinate snapshots.
- Independent bounded exporter fixture passed before44-byte export; integer ranges,256-byte cap, overwrite refusal. No debugger disassembly commands in V03.
- Existing SQLite61functions/80calls; new region/sites/CFG and187operands added transactionally. All old rows and4old assembly sources preserved; integrity/FKs PASS.

## Prior verified checkpoint
V01 FUNC_REC_02C19A reads+9C/+CB, indexes8-byte records and writes+21C.
V02 FUNC_REC_02C17E is a callable wrapper sharing the existing leaf blocks;28/36/38-byte reconstructions retain exact parity.
Seven original unowned collision sites remain unowned with explicit assessments. Original59candidates/76calls and20box samples/16old addresses remain historical metrics.
PlayersFF8400/FF8800 spacing400; projectileFF9400 stride100 remains spawn-untested.

## Constraints and next target
D: final111,149,056 bytes (~106MiB). V03 logs total~230KB; larger free-space drift is unexplained. No large capture.
Trace callers of the037A56 predicate and its D0 result; deliberately exercise its near branch before naming the decision.
The recovered region's entry is not a confirmed function boundary. Named attacks, full code/data mapping, FBNeo/hardware acceptance and hitbox bug causes remain unproved.
No community issue is fixed.
Use existing evidence/functions_v01.sqlite. Migration backups refuse replay; do not seed-rebuild or overwrite the database.
[Knowledge index](KNOWLEDGE_INDEX.md), [DB guide](FUNCTION_DATABASE_V01.md), [TODO](../TODO.md).
