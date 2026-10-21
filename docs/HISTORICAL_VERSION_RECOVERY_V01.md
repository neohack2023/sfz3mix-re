# Historical SFZ3 Mix version recovery map (2026-10-21)

## Research purpose
Locate *older Zero800 SFZ3 Mix builds* to distinguish original SFA3 logic from incremental hacks, especially the documented removal of crouch cancel and crouch counter in v0.01a. Historical references are not verified local ROM copies.

Primary changelog: https://sfz3mix.github.io/download/log.txt
Official distribution page: https://sfz3mix.github.io/download.html
Historic HBMAME roster: https://github.com/Robbbert/hbmame/blob/master/src/hbmame/hbmame.lst
Archive listings are discovery leads, not authorization to redistribute copyright-protected ROM components.

## Important change boundaries

| Version | Changelog significance | Recovery priority |
|---|---|---|
| Vanilla `sfa3us` | Original Capcom source behavior, not yet acquired | Essential before original-game IPS fix |
| `0.01a` | Earliest documented removal of crouch cancel and crouch counter, plus other simultaneous modifications | **Critical** if surviving binary exists; no confirmed public copy identified |
| `0.01b`–`0.01g` | Subsequent early updates, guard/throw/super changes | High; may preserve removal logic with less later alteration |
| `0.05f` | Experiments with juggle / air-recovery rules | High |
| `0.06b` | Custom Combo restricted during attacks | High |
| `0.07`, `0.07a`, `0.07b` | HBMAME historical entries `sfz3mix07`, `sfz3mix07a`, `sfz3mix07b` | Best **early emulator-indexed** leads |
| `0.08`–`0.13` | HBMAME has named entries, 0.13 is official early webpage's named release | High for cross-version semantic reconstruction |
| `0.20` | Major new CPS2Turbo driver, program/graphics/audio expansion and 416×234 screen | **Architectural discontinuity**: do not raw-diff code offsets across boundary |
| `0.21`–`0.32` | Later fixes; `0.22` specifically mentions continue sprite/number/audio corrections | Useful for community regression provenance |

## Discovery results
- **Official website:** lists release versions 0.13 and 0.23 through 0.32 by name, with only 0.32 plainly exposing a ZIP link on the fetched page; no validated downloadable 0.01-series archive.
- **HBMAME project source roster:** explicitly records `sfz3mix07`, `sfz3mix07a`, `sfz3mix07b`, `sfz3mix08`, `sfz3mix09`, `sfz3mix10`, `sfz3mix11`, `sfz3mix12`, `sfz3mix13`; historical `cps2t.cpp` tracks `sfz3mix20`–`sfz3mix31` and current `sfz3mix`. This proves that emulator *definitions* were documented, not the existence of downloadable ROM bytes in that repository.
- HBMAME 0.242 and 0.243 release histories corroborate versions 0.07/0.07b/0.08 and 0.07a/0.09/0.10 respectively. Other releases enumerate 0.11/0.12/0.13 and 0.20–0.23.
- Upstream forum discussion from Zero800 notes that offsets/pointers were relocated between versions; don't treat any address parity as given: https://www.1emulation.com/forums/topic/37618-support-for-new-rom-hack-projects/
- **No 0.01a executable was obtained or hash verified in this reconnaissance**.

## Next actions
1. Record each discovered release identity, version, download source, authorization/provenance, binary hash, original internal member names, CPU program architecture and emulator driver. Do not infer a downloaded file exists from HBMAME game entries.
2. Seek author-supplied **patch-only** archives and source notes first, including public release assets and historical website snapshots. Avoid unlabeled third-party binaries as authoritative originals.
3. Acquire historical builds only from legitimate sources. Do not add copyrighted ROM binaries to GitHub.
4. If lawfully held builds can be obtained: keep extracted ROM programs in a separate read-only versioned reference manifest. D: storage is constrained; don't clone large assets.
5. Use source-aware instruction signatures and runtime behavior tests across release boundaries, especially 0.13→0.20, rather than naive binary offset diff.
6. To isolate 0.01a removal specifically, the cleanest comparison is verified vanilla `sfa3us` vs 0.01a, with exhaustive checks for all other modifications listed in that release. Later versions won't identify the original change uniquely.

## Status
RELEASES_IDENTIFIED; OLDER_BINARIES_NOT_ACQUIRED; CHECKSUMS_NOT_VERIFIED. No ROM files moved, no gameplay changes.

## 2026-10-21 correction: actual official historical archive URLs found

**Supersedes the earlier claim that the page only exposed a 0.32 download.** Clicking the author's version labels directly resolves historical archive URLs, and the hosting server reports ZIP or 7z media types. Content integrity still needs downloaded-file inspection; these are **located, not locally verified copies**.

- v0.13: https://sfz3mix.github.io/download/0.13/sfz3mix13.zip
- v0.23: https://sfz3mix.github.io/download/0.23/sfz3mix.7z
- v0.24: https://sfz3mix.github.io/download/0.24/sfz3mix.7z
- v0.25: https://sfz3mix.github.io/download/0.25/sfz3mix.7z
- v0.26: https://sfz3mix.github.io/download/0.26/sfz3mix.7z
- v0.27: https://sfz3mix.github.io/download/0.27/sfz3mix.7z
- v0.28: https://sfz3mix.github.io/download/0.28/sfz3mix.7z
- v0.29: https://sfz3mix.github.io/download/0.29/sfz3mix.7z
- v0.30: https://sfz3mix.github.io/download/0.30/sfz3mix.7z
- v0.31: https://sfz3mix.github.io/download/0.31/sfz3mix.7z

Source: https://sfz3mix.github.io/download.html and author-controlled GitHub Pages repository https://github.com/sfz3mix/sfz3mix.github.io.

**Pre-v0.13 binaries, especially v0.01a and v0.07, remain unlocated in a directly verified author download.** Historical HBMAME set definitions are still strong identifiers but are not proof of files. Do not confuse the Game's original CPS2 data layout with >=0.20 CPS2Turbo data layout. Existing canonical v0.32 ROM remains unchanged.
