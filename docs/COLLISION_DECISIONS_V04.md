# Collision decision recovery V04

## Decision
**PARTIAL MILESTONE — near-success purpose not runtime verified.**
Recovered the actual callable entry enclosing037A56, its caller/result use, both-sided distance samples, state gates, a new visual/input/animation observation, and five exact assembly regions.
No successful D0=1 return, selector-zero write or resulting action was observed. Do not name or claim the successful mechanic from this receipt.

Scope github:neohack2023/sfz3mix-re; Host02/DaltonsLaptop574; existing D:\AIOS_SFZ3MIX_V032.
Canonical preflight READY_CONTINUE for accepted commands. No registration change, clone, extraction or gameplay modification.
ROM hash before/after unchanged: b5f7a1598e4f91a5113c506505b482b2cd1a19e366fe31471740e45dbd204691.
[Machine-readable evidence](COLLISION_DECISIONS_V04.json).

## Callable entry and caller
FUNC_REC_037A46 is now a runtime-confirmed callable region [037A46,037A82),19 instructions.
It reuses the unchanged V03 REGION_037A56 (14 instructions/six blocks), adding a16-byte prefix.
It calls helper037A82; that helper also branches into the common false-return block at037A7A.
These are shared return blocks, not exclusive ownership claims.

Runtime control trace:
- Caller site0379B4 BSR→037A46.
- Entry037A46 BSR→helper037A82, helper RTS→037A4A.
- Prefix checks opponent+31, then reaches037A56 where eligible.
- False exit037A7A→037A7C RTS→0379B8.
The enclosing owner of caller0379B4 is still unresolved.

At0379AE the byte-verified caller clears D6, tests bit0 in D5, and conditionally calls037A46.
The return uses MOVEQ0/1, so BNE at0379B8 consumes the returned Z flag; it does not need a separate TST of D0.
Observed returns were D0=0, SR with Z set. The actual positive branch remains unobserved.

## What the success path would do — static evidence only
Byte-exact blocks establish:
1.0379B8 BNE→037A3E on a true result.
2.037A3E writes D6=0 to receiver+21E, then returns D0=1.
3.Outer JSR02C584 calls decision entry03797E. At02C58A, zero skips application; nonzero calls037AD2.
4.037AD2 writes6 to receiver+204, clears the longword at+200, then branches to dispatcher035A50.
5.The mode6 table entry statically resolves to035B2A.

Other static+21E readers include022204 and0377FE; the latter uses the byte as a table index. These are leads, not observed success-path behavior.
This supports a **behavior/command-selection dataflow**, but a named defensive action, guard, throw, counter or other mechanic is not established.
No examined success-prefix instruction writes player X/Y. This does not exclude later movement in the unresolved selected action.

## Targeted scenarios and gate separation
Three input-only experiments retained the original game bytes:
| Trial | Result | Logged events | JSONL bytes |
|---|---|---:|---:|
| collision_decisions_v04 | PARTIAL_LOG_CAP_REACHED_CONTROL_TRACES_VALID | 600 | 407265 |
| collision_decisions_controlled_v04 | COMPLETE_BOUNDED_NEGATIVE | 179 | 119374 |
| collision_decisions_crouch_v04 | COMPLETE_BOUNDED_NEGATIVE | 158 | 105832 |

First prototype: six approach/punch attempts with small visual checkpoints. Its600-event cap was reached, so the JSONL lacks COMPLETE. Its two closed control traces remain valid; partial operands are excluded from the accepted SQLite operand import.
The close trace rejects receiver state+6==06 inside helper037A82, before the distance read. Images show Sakura airborne during a counter-hit exchange.

Controlled standing trial: servo approach to approximately40–47 units; wait for grounded raw eligibility; issue a single Button1 pulse.
Actual near reads: 43, 40, 31, 45, 45.
Crouching trial: same arming conditions, Down held and delayed Button1 pulse; two attempts.
Actual near reads: 43, 40, 43, 43.
Far samples also occurred in both complete trials. This is not a state-matched47-versus48 boundary test.

At **every captured near read in the complete trials**, opponent+A9 was0.
The breakpoint at037A64 (beyond the A9 test) never fired.
When an active standing punch was recorded, receiver eligibility had changed; e.g. interval3056 has Ryu+A9=1 while Sakura word+4=0202, rejected by the helper.
The near-success conjunction therefore was not reached. Do not interpret close spacing alone as a true result.

Required conjunction:
- Receiver word+4==0200.
- Receiver byte+6 is not06,0A,0E or10.
- Opponent+31==0.
- Distance+21C<48, unsigned.
- Opponent+A9!=0.
- Opponent word+4==0200.
- Longword at opponent animation+8!=0.

These are raw tested/decoded conditions. The scope of each state code is not globally named.
The remaining exact blocker is a natural input sequence that combines these conditions **before** the receiver changes to an excluded state.
No forced RAM state, altered AI mask or ROM patch was used.

## Named visual/input observation
HUD images independently identify Ryu and Sakura.
At interval3349 in the standing trial:
- Input protocol: standing Button1 punch attempt.
- Image shows Ryu's upright extended-arm punch and Sakura in an airborne reaction pose.
- CPU snapshot in the same frame_done interval: Ryu animation cell 0x11D68E, word+4=0200, byte+6=0A, A9=1.
- Label: **Ryu standing Button1 punch**. Strength label remains unverified.
This is a current input/visual/same-interval RAM association, not a universal animation-ID dictionary or an atomic screenshot/CPU sample.
The crouching image establishes a crouching pose with Button1 input, not an independently identified active strike.
No exact Sakura move name is assigned.

Screenshots remain local; paths and SHA-256 values are in the JSON. They were visually inspected.
Screen snapshots use MAME's documented screen:snapshot API:
https://docs.mamedev.org/luascript/ref-devices.html#screen-device

## Assembly parity
Existing GNU as2.38 -m68000 / objcopy.text; no ROM patch or raw-byte source directives.
| Source | CPU interval | Bytes | Expected = assembled SHA-256 |
|---|---|---:|---|
| [collision_predicate_037a46_v04.s](../tools/collision_predicate_037a46_v04.s) | [0x37A46,0x37A82) | 60 | 719c9ac1cd49d5b7803b42723686caabd56190d60401723b078bb2b3bb642564 |
| [collision_caller_0379ae_v04.s](../tools/collision_caller_0379ae_v04.s) | [0x379AE,0x379BC) | 14 | 4e60a8250afac76570cdb173b060899e382f590c05793897235ba47f0b9a9b42 |
| [collision_success_037a3e_v04.s](../tools/collision_success_037a3e_v04.s) | [0x37A3E,0x37A46) | 8 | 075597ed24ac57a42908f4bbc1e6c55bedb627c99d62b7e7348cf469cb5dbaca |
| [collision_apply_037ad2_v04.s](../tools/collision_apply_037ad2_v04.s) | [0x37AD2,0x37AE0) | 14 | 2d34021e66672b7c638ea19696a564ba33dd2a23be5aae4f2f408dc0cb443e90 |
| [collision_outer_02c584_v04.s](../tools/collision_outer_02c584_v04.s) | [0x2C584,0x2C594) | 16 | 7f38de5a41c65e87cd1528037c99af9ef2a315cb9a01883507811f0eaadf1b3f |

All five PASS, mismatch addresses[].
112 assembled bytes include the reused44-byte V03 body: **68 newly reconstructed unique bytes**.
The callable source includes the unchanged V03 assembly rather than copying its instructions.
Source hashes and exact ranges are in the JSON. The success/application regions are statically proven reconstructions, not runtime-success claims.

## SQLite and preserved evidence
Existing evidence/functions_v01.sqlite extended transactionally:
-62 functions/83 calls.
-New FUNC_REC_037A46 plus three call relationships; caller function IDs remain null where unproved.
-Three prefix blocks/five instructions; membership points to existing REGION_037A56 blocks without duplication.
-New ownership claim identifies the entry-bounded owner; historical V03 null-owner rows remain intact.
-200 CPU observations imported from the **two complete** trials.
-Three trial receipts, one visual/state/move association, static result dataflow and five parity regions.

New tables:
function_consumer_region_memberships, collision_region_ownership_claims,
collision_decision_trials, collision_state_move_observations, collision_decision_dataflow.
Backup: evidence/functions_v01_before_collision_decisions_v04.sqlite.
All previous rows and five previous successful assembly sources remain exact. Integrity/FK checks pass before/inside/after commit.
The community hitboxes association remains investigative; no causal link or fix.

```sql
SELECT * FROM collision_region_ownership_claims;
SELECT f.id,m.region_id FROM functions f
JOIN function_consumer_region_memberships m ON m.function_id=f.id;
SELECT caller_id,site_address,target_address,confidence FROM calls
WHERE site_address IN (0x379B4,0x37A46,0x2C584);
SELECT id,status FROM collision_decision_trials;
SELECT * FROM collision_state_move_observations;
SELECT * FROM collision_decision_dataflow;
```

## Reproduction and resource limits
Project commands ran from D:\AIOS_SFZ3MIX_V032 under canonical preflight:
```powershell
C:\Python314\python.exe C:\AIOS\02_RUNTIMES\AIOS_KNOWLEDGE_CONTEXT_RUNTIME_01\host_context_runtime.py build --workspace sfz3mix-v032
C:\Python314\python.exe tools\inspect_collision_v04.py
C:\Python314\python.exe tools\inspect_collision_v04b.py
C:\Python314\python.exe tools\query_m68k_v04.py calls 0x3797e
C:\Python314\python.exe tools\query_m68k_v04.py field 0x21e
C:\Python314\python.exe tools\run_collision_decisions_v04.py
C:\Python314\python.exe tools\run_collision_decisions_controlled_v04.py
C:\Python314\python.exe tools\run_collision_decisions_crouch_v04.py
C:\Python314\python.exe tools\verify_collision_decisions_v04.py
C:\Python314\python.exe tools\ingest_collision_decisions_v04.py
```
Local inspectors also queried bounded ranges around03797E/037A46/035A50/037AD2. An end falling inside an instruction was rejected by the fixture-tested exporter; no partial bytes were promoted.
Verifier contains exact WSL assembly commands. Launch JSONs preserve complete HBMAME argv and exit0/empty-stderr results.
Output names and rollback backups must be preserved; do not remove them to replay a migration.
The first prototype's capped logger/trace source is preserved for reproduction; prefer the complete controlled harnesses for new work.
No original distribution extraction, tool reinstall, expensive CI, frame recording or large dump.
Raw JSONL, PNGs, console/instruction traces, object/binary derivatives, SQLite backups and exploratory inspectors stay local.

D: started106,954,752 bytes free; last post-migration check44,040,192 bytes (~42MiB).
The new gameplay logs are631,534 bytes total plus small PNGs; they do not explain the larger storage drift. Its cause remains unresolved.
Recheck storage before any further capture. No files were deleted or moved.

## Next precise target
Find a whiff/active-attack interval with opponent+A9!=0 while receiver remains eligible, then trace the actual D0=1 return, +21E selector0 write,037AD2/035B2A dispatch and resulting action.
Use a slow or short-range input scenario justified by the observed gates; do not simply extend logging time or force RAM.
Only after that observation should the reaction receive a named mechanic or be associated causally with the community hitbox complaint.
