# Community Patch TODO — Street Fighter Zero 3 Mix v0.32

Track requested improvements to the **existing CPS2 FBNeo/HBMAME ROM**, not a recompilation. A checkbox is completed only after a reproducible before/after test, ROM-hash receipt, and reviewer acceptance. Requests below are carried forward from project discussion; original community message links and exact wording remain to be collected unless explicitly linked.

## Original community request and attribution
- **Requester:** [u/Motor_Economy_1741](https://www.reddit.com/user/Motor_Economy_1741/) (Reddit)
- **Post:** [“Street fighter zero 3 MIX IS DEAD !”](https://www.reddit.com/r/romhacking/comments/1xa4ydk/street_fighter_zero_3_mix_is_dead/) in **r/romhacking**, October 19, 2026.
- **Reported requests:** Karin's rolling begins late after excessive crouching glide; remove continue-counter digit from score; correct Alpha Counter flash position; restore original hitboxes; fix rare background evasion appearing in foreground. **Optional proposal:** add Street Fighter Alpha 3 MAX characters.
- **Constraint expressed by requester:** keep it as an FBNeo-playable ROM, rather than a recompilation, to preserve rollback/local netplay; ideally distribute a patch applicable to the original working ROM.
- **Separate engineering observations:** continue-screen blue sprite fragments were discussed in the comment investigation, rather than the initial list of five; FBNeo floor-edge issue has its own external GitHub reporter. Do not attribute those two items to the original post's bug list.

## P0 — Current investigations
- [ ] **Continue-screen blue sprite fragments** — Identify tile/attribute source and test writer at `0x026438` (candidate, not verified root cause). Avoid broad speculative sprite masks. **Status:** unresolved; prior masking/descriptor experiments failed acceptance.
- [ ] **Continue-counter score** — Reproduced visible score field `0 → 1` after continuing. Locate 68000 RAM field, writer and reader; distinguish expected count from HUD bug; isolate patch and replay both builds. **Status:** reproduced, not fixed. [Receipt](docs/CONTINUE_COUNTER_2026-10-19.md).

## P1 — Gameplay and visual correctness
- [ ] **Karin rolling / crouch glide** — Requester reports excessive crouching glide before rolling animation begins (possibly other characters); reproduce, inspect movement and animation timing.
- [ ] **Alpha Counter flash** — Record expected vs actual timing/effects across characters and emulators; isolate rendering or ROM source.
- [ ] **Hitboxes** — Gather specific moves, characters, frames and capture evidence; compare collisions against intended rules before changing boxes.

## P2 — Mechanic and renderer compatibility
- [ ] **Background evasion foreground pop** — Requester reports rare appearance in foreground, possibly when the opponent attacks; reproduce and investigate layer/depth state.
- [ ] **FBNeo floor-edge rendering glitch** — Compare same ROM/input against HBMAME/MAME; determine renderer-only vs ROM patch. [External report: FBNeo #1833](https://github.com/finalburnneo/FBNeo/issues/1833). **Status:** externally reported, not locally reproduced.

## P3 — Feature feasibility (separate from bug fixes)
- [ ] **Alpha 3 MAX character integration** — Identify target characters and permissible data sources; assess ROM space, graphics, animations, palettes, moves and compatibility. No implementation committed.

## Per-item acceptance gates
- [ ] Link original community request and reporter/attribution if available.
- [ ] Record exact v0.32 input ROM variant and SHA-256.
- [ ] Obtain deterministic reproduction and evidence (or mark proposal, not bug).
- [ ] Identify responsible routine/data and scope a reversible, isolated delta.
- [ ] Test unmodified vs patched with matched inputs on the appropriate emulator(s).
- [ ] Record changed offsets/bytes, clean and patched hashes, expected/actual results, regressions and rollback procedure.
- [ ] Mark fixed only after passing tests; never include copyrighted ROM binaries in this repo.

## Working location
Local Host 02 execution artifacts: `D:\AIOS_SFZ3MIX_V032`. Do not move or delete this working tree. Source scripts and small sanitized receipts can be promoted into this repository separately after review.
