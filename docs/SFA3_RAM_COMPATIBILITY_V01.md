# SFZ3 Mix v0.32 versus original Street Fighter Alpha 3 RAM layout

**Experiment date:** 2026-10-20. **Host:** DaltonsLaptop574, existing `D:\AIOS_SFZ3MIX_V032`. All gameplay experiments read ROM and RAM; scripted coin/start/attack inputs only. **No RAM writes, no ROM modifications, no project clone, no ZIP extraction.**

## External source and a corrected reading of it

The historical [CPS2 hitbox script](https://github.com/Jesuszilla/mame-rr-scripts/blob/master/cps2-hitboxes.lua) has an `sfa3` profile. It defines **player base `0xFF8400`, 4 players, `player_space=0x400` from the post-processing default**, projectile base `0xFF9400`, 24 projectiles, `object_space=0x100`, and screen-left `0xFF8290`. An initial probe incorrectly treated the projectile/object spacing as player spacing. **That first interpretation is superseded:** player 2 begins at **`0xFF8800`**, not `0xFF8500`.

This historical Lua script includes conditional write operations in throw/tripwire processing. **Do not launch that upstream script unmodified as a read-only probe.** Our script only reads RAM and ROM.

## Runtime procedure

Run `tools/ram_trace.lua` against the existing `sfz3mix` HBMAME runtime with the established deterministic input sequence. It saves 64 KiB RAM snapshots on frames **3000, 9300, 10000, 10300, 10550, 10640, 10730, 11000, 13000, 15000, 16900**. It completed with exit code 0. Analysis of these local dumps is done by [`compare_sfa3_ram_v02.py`](../tools/compare_sfa3_ram_v02.py); its local receipt is `evidence/sfa3_ram_comparison_v02.json`. The earlier 2000-frame test did not enter an active match and is not authoritative for game-specific RAM.

### Layout assessment

| Historical SFA3 structure | Observed in v0.32 | Confidence |
| --- | --- | --- |
| Player #1 base `0xFF8400` | 11/11 snapshots have active marker, changing position/status and ROM pointer candidates | Strong runtime corroboration of structure layout |
| Player #2 base `0xFF8800` | 11/11 active marker, changing position/status and ROM pointer candidates | Strong runtime corroboration of structure layout |
| Player #3 `0xFF8C00`, player #4 `0xFF9000` | Zero-filled during this test | Inactive; existence/functionality not disproven |
| Projectile base `0xFF9400`, stride `0x100` | Initial four slots have no active object | Unverified; no projectile-spawn scenario tested |
| Screen-left `0xFF8290` | Values change between checkpoints | Consistent, not yet visually calibrated |

The two observed player regions show dynamic status at `+0x04`, position at `+0x10/+0x14`, animation pointer at `+0x1C`, and changing table/selector fields at `+0x90/+0x94/+0x98/+0x9C`, `+0xC8..CB`. **A changing field doesn't alone prove its intended semantic role.**

## Pointer dereference test, not just nonzero pointers

Tool [`decode_sfa3_hitbox_data_v01.py`](../tools/decode_sfa3_hitbox_data_v01.py) uses the hash-verified **extracted** `tools/sz3mx.03` CPU program (SHA-256 `b5f7a1598e4f91a5113c506505b482b2cd1a19e366fe31471740e45dbd204691`) and source-described indexing:

- Vulnerability pointers: RAM offsets `+0x90/94/98`, IDs `+0xC8/C9/CA`.
- Push pointer: `+0x9C`, ID `+0xCB`.
- Record file address `pointer + (ID << 3)`, 8-byte record, signed big-endian X/Y offsets, unsigned big-endian X/Y radii.

**88 attempted field/frame/player combinations; 20 active ID/pointer pairs; 20/20 resolve inside this v0.32 CPU program and decode to dimension records within the original script's plausible size/sign conventions.** They represent **16 distinct record addresses**. Example, frame 3000 player 1 pushbox record at `0x0D6588`: X offset 0, Y offset 38, X radius 20, Y radius 38. Original execution sample receipts remain local at `evidence/sfa3_hitbox_pointer_decode_v01.json`.

**Meaning:** More than pointer plausibility, this corroborates that v0.32 stores compatible box record-shaped data. It does **not** yet demonstrate the running collision engine actually used these records on those frames. No code-to-RAM read/write xref has been verified, no hitbox fix made, and no emulator overlay synchronisation tested.

## SQLite knowledge ingestion: PASS

In the existing `evidence/functions_v01.sqlite`, we added rather than replaced tables:

- `ram_structures`: 2 original profile pools, with source, confidence, provenance
- `ram_slots`: 4 historical player and 24 projectile slots, indicating sampled/unsampled and active/inactive states
- `ram_fields`: 14 annotated player-field candidates
- `ram_observations`: 88 sampled slot/frame occupancy observations
- `ram_issue_links`: 2 investigative links to the existing `hitboxes` community issue
- `ram_box_decodes`: 20 validated record-shaped byte interpretations at 16 distinct CPU program addresses
- `function_ram_xrefs`: deliberately **0 verified**. No function ownership can be promoted without debugger traces.
- Existing **59** candidate functions and **76** static call sites preserved. Database foreign-key and integrity checks passed.
- A pre-migration SQLite backup is stored locally in `evidence/functions_v01_before_ram_profile_v01.sqlite`.

Reproducible scripts: [`ingest_sfa3_ram_v01.py`](../tools/ingest_sfa3_ram_v01.py), [`ingest_sfa3_box_decode_v01.py`](../tools/ingest_sfa3_box_decode_v01.py), and [`query_sfa3_ram_v01.py`](../tools/query_sfa3_ram_v01.py).

### Query example

```powershell
python D:\AIOS_SFZ3MIX_V032\tools\query_sfa3_ram_v01.py --database D:\AIOS_SFZ3MIX_V032\evidence\functions_v01.sqlite --address 0xFF8800
```

This returned the second player slot and the historical field definitions correctly.

## Next acceptance gate: actual function relationships

1. Use a bounded **read-only debugger trace** or memory read watchpoint to capture which program counters read RAM `0xFF8490` / `0xFF849C`, player #2 equivalent `0xFF8890` / `0xFF889C`, and the accessed ROM record addresses during an attacking frame.
2. Correlate with player movement/attack animation and, if feasible, synchronized overlay or screenshot. Test a genuine projectile spawn separately.
3. Confirm observed PC opcode fetch and mapped file offsets; attribute the read to a recovered function with known boundaries, not just the nearest candidate.
4. Insert verified relationships into `function_ram_xrefs`, link to `hitboxes`, and retain provenance. Avoid changing hitbox data before this passes.

Historical external Lua is a reference, **not** an accepted patch or read-only runtime script.
