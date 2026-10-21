# Current state: Street Fighter Zero3 Mix v0.32

## Authority and integrity
Scope github:neohack2023/sfz3mix-re; Host02 DaltonsLaptop574; existing D:\AIOS_SFZ3MIX_V032 / sfz3mix-v032.
Drive governs registration, GitHub implementation, Host02 local evidence.
Accepted V04 preflights READY_CONTINUE. ROM tools/sz3mx.03 hash b5f7a1598e4f91a5113c506505b482b2cd1a19e366fe31471740e45dbd204691, unchanged before/after.
No clone, extraction, gameplay patch or new database.

## Latest V04 checkpoint — partial milestone
[Caller/state engineering receipt](COLLISION_DECISIONS_V04.md), [machine-readable evidence/parity](COLLISION_DECISIONS_V04.json).
-Verified callable entry FUNC_REC_037A46, [037A46,037A82), enclosing V03 reader037A56.
-Actual caller0379B4, helper037A82 and return0379B8 verified by bounded trace. Existing consumer/shared-return blocks reused, not exclusively owned.
-BNE consumes returned Z flag. Static true path writes selector0 to+21E, returns success and reaches037AD2 mode6 application. **True return/application not observed. Named mechanic unresolved.**
-Controlled near reads31/40/43/45 all had opponent+A9=0. Other close attempts rejected receiver state6==06 or word+4==0202. Precise eligibility conjunction is in the receipt.
-Current visual/input association: Ryu standing Button1 punch, animation cell0x11D68E in interval3349; strength and global animation mapping unverified.
-Five parity regions PASS:112bytes including reused44bytes,68new unique bytes.
-SQLite62functions/83calls;200 new operands from two complete trials. All prior rows and five prior successful assembly sources preserved; integrity/FKs PASS.
-First prototype hit600-event cap; partial operands excluded from accepted import. Its closed call traces remain evidence.

## Preserved V01–V03
V01 callable02C19A writes absolute distance to computed opponent edge at+21C.
V02 wrapper02C17E shares the leaf. V03 consumer037A56 gates a Boolean state/animation predicate at unsigned48.
Historical original59candidates/76calls,50sample/nine-site trace,20box samples/16old records remain.
Player basesFF8400/FF8800 spacing400; projectileFF9400 stride100 remains spawn-untested.
No community hitbox cause/fix, full code/data separation or FBNeo/hardware acceptance claim.

## Storage and next gate
Last D: check44,040,192 bytes (~42MiB). New logs~632KB plus small images do not explain larger space loss. Stop captures until storage is rechecked.
Need natural overlap of opponent active flag+A9 and eligible receiver before hit reaction; then observe D0=1,+21E0,037AD2/035B2A and action behavior.
Do not force RAM or label a successful mechanic from static dataflow alone.
Use existing evidence/functions_v01.sqlite and retained migration backups.
[Knowledge index](KNOWLEDGE_INDEX.md), [DB guide](FUNCTION_DATABASE_V01.md), [community TODO](../TODO.md).

## Historical reference pin (remote-only, 2026-10-21)
Official v0.13 and v0.23–v0.31 archived releases are pinned as author-site URLs in [HISTORICAL_RELEASE_PINS_V01.md](HISTORICAL_RELEASE_PINS_V01.md) and [JSON](HISTORICAL_RELEASE_PINS_V01.json). Use them directly for documentation research, and fetch one archive temporarily only if byte-level comparisons require it. No new Host02 archive collection is necessary. Original v0.32 remains canonical. The earlier 0.01a build was not located; crouch-cancel removal implementation and community bug fixes remain unverified.

