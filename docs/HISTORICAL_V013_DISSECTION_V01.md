# SFZ3 Mix v0.13: verified archive and chip-layout dissection V01

**Status:** archive verified and CPU-chip allocation inventoried; semantic function recovery **not yet conducted**. This is executable archaeology, **not** a crouch-cancel fix or parity claim.

Source: user-uploaded `sfz3mix13 00.zip` from current project conversation. Uploaded archive SHA-256 `43d48d84a49f26c3ce7c8d46adceb7324b7224d6c51eb9cd466780ec5e2ea28e`, 22 MiB compressed. All ZIP member CRCs pass. **24 archived members:** eight CPU chips, eight graphics chips, two sound CPU members, two audio sample members, one additional dependency, two batch instructions, one key. The key is intentionally excluded from the repository manifest.

| CPU chip | Size | SHA256 prefix | Entropy bits/byte | Nonzero bytes |
|---|---:|---|---:|---:|
| sfz3mix.03 | 524288 | e803be2d0b800ec9 | 5.9432 | 395922 |
| sfz3mix.04 | 524288 | 9d7eefebf80c741a | 5.5747 | 366829 |
| sfz3mix.05 | 524288 | 99229cae2a7e257f | 4.6578 | 285719 |
| sfz3mix.06 | 524288 | 072ced484f4a07b9 | 4.8491 | 290484 |
| sfz3mix.07 | 524288 | 66769880e2b4473c | 4.9806 | 305899 |
| sfz3mix.08 | 524288 | dccc979f4c23f7a4 | 5.6720 | 377015 |
| sfz3mix.09 | 524288 | e830b9d853766d67 | 5.6094 | 354461 |
| sfz3mix.10 | 524288 | 2ad21daaa4749637 | 0.7190 | 31703 |

**Caution:** per-chip nonzero bytes and byte entropy are inventory statistics, not valid proof of executable code, free expansion space, or where logic was inserted. `sfz3mix.10` has many zero bytes, but its CPU mapping and reachability remain untested.

Historical bundle batch instructions rename `sfz3mix.03`/`.04` into `sz3e.03c`/`.04c` for the `sfa3` layout or `sz3ud.03c`/`.04c` for `sfa3ud`, and rename the remaining CPU members `.05`–`.10` into matching `sz3.` names. These instructions were read but **not executed**, and no ROM was renamed or repackaged. Their existence is evidence of an emulator packaging path, **not equivalence to original retail game code**.

v0.13 CPU layout: **eight 512KiB chips = 4MiB CPU program**. Canonical v0.32 working program is **single 6MiB CPU member**. Direct `0.13`→`0.32` physical offsets are not semantically comparable; reconstruct the CPU address layout and functions before matching signatures.

## Next bounded investigations
1. Recover the 68k CPU interleave/address mapping for v0.13 from the appropriate HBMAME driver, distinguishing encrypted opcode fetch from ROM-data reads.
2. Find routines participating in landing, crouching, juggle and cancel eligibility in v0.13, by reproducible state traces; do not assume V04 proximity gate has the same purpose.
3. Retrieve v0.23 and neighboring 0.24–0.27 versions **one at a time** into permitted temporary storage, derive semantic movement/animation diffs, preserve only hashes/scripts/structural findings. Don't put archives on full D:.
4. The changelog's v0.01a removal **cannot be isolated by v0.13 alone**. Need pre-removal reference or a controlled original-vanilla comparison before producing an IPS patch.

## Provenance / limits
The original uploaded archive remains outside GitHub. No ROM/game keys or sound/graphic/code bytes are committed. No gameplay changes, patches, disassembly-function claims, or dynamic emulator runs were performed.
