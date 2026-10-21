# Historical 68000 roll/eligibility comparison V02: bounded code-anchor scan

**Status: PARTIAL.** Verified binary retrieval and instruction-candidate scanning completed; **actual roll-recovery function, eligibility predicate, grab-immunity code and Karin-specific animation defect are NOT yet isolated or dynamically verified**. Do not elevate decoded windows into named gameplay functions.

## Run and provenance
- Host 02, existing `D:\AIOS_SFZ3MIX_V032`, registered scope `sfz3mix-v032`, unified preflight `READY_CONTINUE`.
- Tool: [historical_m68k_candidates_024_026_v01.py](../tools/historical_m68k_candidates_024_026_v01.py). Source/pinned release URLs from author's download page; Capstone 5.0.6 loaded from existing `tools\.vendor` for read-only M68K candidate decoding.
- Historical v0.24, v0.25, v0.26 archives: independently downloaded into bounded C: scratch; each archive SHA-256 matched the previously observed value; 7z integrity test passed; extracted CPU member SHA-256 matched; temp directory removed automatically. No ROM or key bytes committed. No gameplay patch or emulator runtime trace executed in this pass.
- Archived and CPU SHA identities: [comparison V01](HISTORICAL_023_027_COMPARISON_V01.md). This V02 scan was not a source-to-ROM roundtrip; parity acceptance not claimed.

## Quantitative verified results
All three CPU programs are 6,291,456 bytes.
- v0.24→v0.25: 3,502,453 identical bytes at corresponding offsets, 2,789,003 differing bytes. 163,418 of 393,216 aligned 16-byte blocks identical; 40,349 of 98,304 aligned 64-byte blocks identical.
- v0.25→v0.26: 3,452,003 identical bytes at corresponding offsets, 2,839,453 differing bytes.
- v0.24→v0.25 probe around canonical v0.32 0x02C584 (256 bytes): 220/256 aligned bytes identical. This is **a structural candidate**, not proof that the v0.32 function or its semantics map to the exact same historical address.
- v0.24→v0.25 probe around canonical v0.32 0x037A46 (256 bytes): only 4/256 bytes identical; strong warning against assuming stable function offsets.

## Concrete pointer-relocation observations
Capstone decodes one candidate sequence at CPU offset 0xE70:
- v0.24: `movea.l #$31642c, a0`.
- v0.25: `movea.l #$3165cc, a0`. Immediate increased by 0x1A0.
- v0.26: `movea.l #$3166a0, a0`. Immediate increased by 0xD4 from v0.25.

Other nearby sequences show similar per-release immediate-address shifts while surrounding instruction mnemonics and operands remain unchanged. At 0xE84 and 0xE98 the same phenomenon occurs. This demonstrates that some high-level byte deltas are relocation-like pointer changes, **not independently confirmed gameplay rule edits**.

Capstone may produce plausible-looking instruction text on data or encrypted/unused regions. Confirm opcode mapping/reachability in emulator before classifying any candidate sequence as executed game logic.

## Why the requested functions remain unassigned
1. We still need controlled input states for roll recovery, Karin rolling/crouch glide, landing, and opponent throw attempts on historical 0.24/0.25/0.26 versions.
2. No debugger control trace from any of those historical versions connects candidate instruction addresses to observed memory-state changes.
3. No verified cross-version CFG/callgraph alignment distinguishes address relocation from a changed condition, input test, or state writer.
4. The historical changelog's generic roll-recovery fix is not necessarily the commenter's specific Karin roll-delay defect; don't merge them by name alone.

## Next bounded plan
1. Identify and validate HBMAME driver set names and CPU/opcode mapping for each historical version. Test each release's emulator boot and input script *independently* using exact source hash.
2. Capture short matched scenarios: neutral crouch→stand→roll, roll input during landing recovery, attempt roll when attacking, opponent throw during roll, and Karin-specific delayed roll animation. Log player state and animation identifiers, X/Y deltas, command input, rollback-independent frames, and writer PC. Cap event counts.
3. Trace writer/reader PCs that *actually differ* in post-input behavior between v0.24 and v0.25, then v0.25 and v0.26.
4. Find corresponding changed functions via normalized instruction+CFG signatures accounting for pointer relocations; recover minimal editable 68000 assembly; reassemble byte-exact and test matching scenarios. Add SQLite entries **only** after ownership/range and effect evidence are validated.
5. Preserve original v0.32 gameplay and ROM hash; any future community patch is disposable, reversible and subject to FBNeo acceptance.

**Community status:** 0 accepted changes. Crouch-cancel removal introduced in 0.01a and is a separate earlier-history question. No evidence yet links V04 `+0x21C` proximity gate to roll/grab immunity.
