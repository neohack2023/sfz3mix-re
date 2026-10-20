# Original Capcom arcade baseline: sfa3us

Status (2026-10-20): **IDENTIFIED; LOCAL COPY NOT FOUND; NOT ACQUIRED**.

- Game: Street Fighter Alpha 3 (USA 980616, SAMPLE Version), set `sfa3us`, parent `sfa3`.
- Verification authority: FinalBurn Neo machine manifest: https://wiki.neo-source.com/database/view/arcade/sfa3us
- Original hack creator Zero800 described `sfa3us` as the base revision; this is a source-lineage statement, not byte parity for SFZ3 Mix v0.32.
- Host 02 targeted searches (AIOS workspaces, runtimes, caches, downloads and expected ROM locations) did not locate a matching `sfa3us` set. This is **not** an exhaustive disk inventory.
- The original Capcom program is separate from hacked `sz3mx.03`. Keep originals in a **read-only comparison reference** only if lawfully obtained.
- Capcom's official modern game release: https://store.steampowered.com/app/1842988/Capcom_Arcade_2nd_Stadium_Street_Fighter_Alpha_3/ . Purchasing that game does **not** establish possession of these exact arcade dump files.

## Program components, unmodified (all 524288 bytes)

| Filename | CRC32 |
| --- | --- |
| `sz3-usam_03.6a` | `14319e29` |
| `sz3-usam_04.7a` | `65fbc272` |
| `sz3-usam_05.8a` | `e93c47d1` |
| `sz3-usam_06.9a` | `1bf09de3` |
| `sz3-usam_07.6d` | `f6296d96` |
| `sz3-usam_08.7d` | `1f4008ff` |
| `sz3-usam_09.8d` | `822fc451` |
| `sz3-usam_10.9d` | `92713468` |

## Other game components
- Graphics (4 MiB each): `sz3.13m` `0f7a60d9`; `sz3.15m` `8e933741`; `sz3.17m` `d6e98147`; `sz3.19m` `f31a728a`; `sz3.14m` `5ff98297`; `sz3.16m` `52b5bdee`; `sz3.18m` `40631ed5`; `sz3.20m` `763409b4`. These may be supplied by parent set `sfa3`.
- Sound CPU: `sz3-usam_01.1a` `c180947d`, `sz3-usam_02.2a` `9ebc280f` (131072 bytes each).
- QSound (4 MiB each): `sz3.11m` `1c89eed1`; `sz3.12m` `f392b13a`.
- ROM key `sfa3u.key` 20 bytes CRC32 `4a8f98c1`.
- All CRCs derive from the cited FinalBurn Neo manifest, not yet verified from local data.

## Acquisition and provenance gates
1. Locate a copy from user-owned lawful backup / original arcade board dump, or a rightsholder-authorized redistribution where available.
2. Verify filename, length, CRC32 and additionally calculate SHA-256 of each available component, keeping source/acquisition notes.
3. Record parent-set dependencies explicitly; don't mistake an 11-file clone archive for a standalone complete set.
4. Place the unmodified reference under a dedicated **read-only reference** path without overwriting the existing SFZ3 Mix workspace or creating redundant full copies. Prefer references to existing owned files.
5. Compare against the hacked ROM with layout-aware and pointer-aware mapping. Do not compare `sfa3us` as a single linear image to hacked `sz3mx.03`.
6. No ROM files, keys, or game dumps are committed to GitHub.

## Current result
No verified local unmodified set, no CRC verification performed on source files, and no claim that an authorized original ROM archive was acquired.
