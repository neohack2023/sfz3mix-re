# Historical v0.23–v0.27 executable comparison V01

**Execution:** 2026-10-21, Host 02 `DaltonsLaptop574`, temporary C: scratch via [bounded comparator](../tools/compare_historical_23_27_v01.py). **Five official ZIP/7z archives downloaded, 7z integrity-tested and extracted, 8 members per release SHA-256/CRC32 scanned; temporary extraction and archive files removed automatically.** Canonical D:\AIOS_SFZ3MIX_V032 working ROM untouched. This is **structural research only**, no gameplay behavior or code-level culprit proven.

## Version corpus (CPU program verified)

| Version | Archive SHA-256 | CPU member | CPU SHA-256 |
|---|---|---|---|
| 0.23 | `6245369b96362cda568bcac32c1c7ea81bda28a92e811958c8b97b9360f41ac6` | `sfz3mix.p1` | `bfae9cd8a6925cdc3cf4fdd7ac3e3d699c48fb484c4b1d82ec56b02ebe758996` |
| 0.24 | `9082929fd7075502a35e5f977f3ccb6cc3dbafc35fd9e693e7508fe61ae7b9d7` | `sfz3mix.p1` | `2fba55f17fa2801cb05ce07a9ba66ed515cb1163dde69592728214a6a77b2f8f` |
| 0.25 | `cdde7583917bfb13d0c985184c2ee2fa1b99a266610e544fc1b8f545cbb6a4c6` | `sfz3mix.p1` | `5ff23470ddec1dadc9935c370adfef4408beb92f0cccac94181d1dfe81e948c4` |
| 0.26 | `7bc49cc6c88460efe67a38f8c405081af4eee53ac71230bc2f9732128da4290c` | `sz3mx.03` | `7724bf1ea71d9a85f88054307c1a195637736d372e1a92c4831dc43d25b9452e` |
| 0.27 | `924ff8a21b2e2d4e402bffcd8deb9bbadcaa21729aaa1f284062ff9c18792ae3` | `sz3mx.03` | `b556e7ff15ba9b3b618a8421926251ffec6116766985ed96cb7a001d6b737f32` |

Each CPU member is exactly **6,291,456 bytes**. The source archives were about 17.8MB. v0.26 renames the CPU, GFX, sound and samples to `sz3mx.*`, consistent with author's changelog. The sound CPU and sample SHA-256 values remained identical across all five versions. The second 32MiB graphics member also remained identical. First graphics member changed between 0.23→0.24 and 0.25→0.26, but matched between 0.24/0.25 and 0.26/0.27. This isolates which *assets* need later scrutiny, not which behavior changed.

## Byte/page deltas

Page size 4096; 1536 total CPU pages per version. These are **physical byte comparisons**, not executable-function differences.

| Adjacent versions | Byte mismatches | Changed pages | Number of contiguous changed-page spans | Representative span |
|---|---:|---:|---:|---|
| 0.23→0.24 | 2,975,013 | 936 | 6 | [0x20000,0x3B1000) |
| 0.24→0.25 | 2,789,003 | 933 | 7 | [0x26000,0x3B1000) |
| 0.25→0.26 | 2,839,453 | 933 | 8 | [0x32000,0x3B2000) |
| 0.26→0.27 | 3,046,593 | 946 | 1 | [0x000000,0x3B2000) |

Most physical byte mismatches concentrate in the first ~3.9MiB. The remaining pages are identical for each adjacent comparison. Do not infer whether this is asset recompaction, encryption, or code movement without mapping. In particular, identifying a gameplay bug from these raw spans alone would be unsound.

## Targeted investigation priorities tied to author's history

[Author changelog](https://sfz3mix.github.io/download/log.txt):
- **0.23 baseline:** Roll Recovery enabled by `lp+lk` or falling command, labeled invulnerable in changelog.
- **0.24:** roll/escape command priority, code corrections, increased recovery time, run termination on damage/throw.
- **0.25:** roll recovery command fixed.
- **0.26:** roll/escape immunity to grabs fixed, Charlie and Dan hitbox adjustments, legacy filename rename.
- **0.27:** running diagonal charge, quick-tap and Super Cancel command recognition; several active move/recovery changes.

**What is not yet demonstrated:** no specific Karin roll routine, crouch cancellation, hitbox defect, state-machine writer, compiled source equivalence, or actual live roll trace identified. No game patch accepted. The major byte mismatch regions mean naïve IPS/chunk diff would change unrelated behavior.

## Next executable step
Focus on **0.24 vs 0.25** (narrowest author's roll-recovery change) and **0.25 vs 0.26** (roll grab immunity). Read the relevant HBMAME driver’s CPU data/opcode mapping; locate reachable 68000 command parser, landing recovery, move eligibility and state writers by bounded signature/CFG analysis and controlled emulator inputs. Compare normalized function semantics or exact code windows, not broad binary offsets. v0.27 can serve as later regression baseline.

The **Karin crouching glide → delayed roll animation** report remains a separate repro requirement: do not attribute it to changelog's generic roll-recovery command fixes without input/frame evidence.

**Retention:** Only tool, file sizes, hashes, counts and analysis are committed. Program ROMs, key material, graphics/sounds and large artifacts were never committed.
