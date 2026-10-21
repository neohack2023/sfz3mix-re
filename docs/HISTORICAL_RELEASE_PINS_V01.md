# PINNED | SFZ3 Mix older releases (remote-first)

**Persistent version index:** [machine-readable JSON](HISTORICAL_RELEASE_PINS_V01.json). This file is the human-facing pin for future conversations and agents. The existing v0.32 ROM remains the only canonical gameplay modification target. Older builds are **remote references**, not mandatory Host 02 installs or new clones.

**Author-controlled download page:** https://sfz3mix.github.io/download.html  
**Author's changelog:** https://sfz3mix.github.io/download/log.txt  
**Technical chronology:** [historical recovery research](HISTORICAL_VERSION_RECOVERY_V01.md)

| Version | Original layout | Official archive link | Comparison use |
|---|---|---|---|
| **0.13** | CPS2 | [ZIP](https://sfz3mix.github.io/download/0.13/sfz3mix13.zip) | Earliest located early-CPS2 comparator |
| **0.23** | CPS2Turbo | [7Z](https://sfz3mix.github.io/download/0.23/sfz3mix.7z) | Roll/collision-era historical regression |
| **0.24** | CPS2Turbo | [7Z](https://sfz3mix.github.io/download/0.24/sfz3mix.7z) | Roll/collision-era historical regression |
| **0.25** | CPS2Turbo | [7Z](https://sfz3mix.github.io/download/0.25/sfz3mix.7z) | Roll/collision-era historical regression |
| **0.26** | CPS2Turbo | [7Z](https://sfz3mix.github.io/download/0.26/sfz3mix.7z) | Roll/collision-era historical regression |
| **0.27** | CPS2Turbo | [7Z](https://sfz3mix.github.io/download/0.27/sfz3mix.7z) | Roll/collision-era historical regression |
| **0.28** | CPS2Turbo | [7Z](https://sfz3mix.github.io/download/0.28/sfz3mix.7z) | Later regression chronology |
| **0.29** | CPS2Turbo | [7Z](https://sfz3mix.github.io/download/0.29/sfz3mix.7z) | Later regression chronology |
| **0.30** | CPS2Turbo | [7Z](https://sfz3mix.github.io/download/0.30/sfz3mix.7z) | Later regression chronology |
| **0.31** | CPS2Turbo | [7Z](https://sfz3mix.github.io/download/0.31/sfz3mix.7z) | Later regression chronology |

## Operational retrieval policy

1. **Start here** and consult [CURRENT_STATE.md](CURRENT_STATE.md). Do not ask for reuploads simply because the archive is not already installed on Host 02.
2. Work on one selected release at a time. For documentation/changelog research, use the remote version links without downloading.
3. If byte-wise disassembly or differential analysis is required, actual archive bytes must be accessible to the analysis runtime. Fetch just that archive to **temporary** working storage with adequate headroom (local ephemeral storage, not persistent Host 02 collection), verify extracted members and hashes, and emit a sanitized comparison receipt. The URL by itself is not byte evidence.
4. Avoid using D: (nearly full in recent checks), don't overwrite or repack canonical v0.32, and never commit copyrighted program/graphics/audio bytes. Keep hashes, structural metadata, offsets, tool scripts, behavior traces, and independently developed patch deltas in GitHub.
5. v0.13 was uploaded and CRC-inspected previously in ChatGPT, but the persistent recoverable reference is the author's link above. v0.01a is still **not located**. Finding earlier releases is a separate task.
6. Note **architecture break at 0.20**: pre-v0.20 CPS2 chips and later CPS2Turbo expanded image are not address-comparable without mapping.

## Investigation priorities

- Crouch-cancel/Crouch Counter removal: version 0.01a changelog lead. v0.13 can establish whether the removal survived into a later early build; it cannot alone reveal the original delta.
- Karin roll, hitbox/collision regressions: follow changelog boundaries across 0.23–0.31, then map functions to canonical 0.32.
- Continue counter/display and Alpha Counter visuals: compare relevant release-era records, but do not mark any fix accepted without matched-gameplay tests.

**Status:** URLs pinned and machine index committed. Remote links verified as present on the current author's download page; archive-byte hashes for the pinned remote releases have not been independently verified in this operation. No new Host 02 storage used.
