# V01 — Whole-program byte coverage and reversible package build
**Date:** 2026-10-20  
**Authority:** Tested execution receipt from Host 02. GitHub stores scripts and sanitized reports; source ROM stays local.  
**Scope:** SFZ3 Mix v0.32 only. Registered AIOS CPS2-specific scope remains unresolved.

## Verified results (Host 02)
- Script: [`tools/rom_rebuild_v01.py`](../tools/rom_rebuild_v01.py), mirrored locally at `D:\AIOS_SFZ3MIX_V032\tools\rom_rebuild_v01.py`.
- Input: `D:\AIOS_SFZ3MIX_V032\downloads\sfz3mix_v032_original.zip`
- Original ZIP SHA-256: `867b8356872a034ec7e06f776bf757ec2095fee7616931b71f720f30369806ab`
- Actual original ZIP has **8 entries**. The earlier HBMAME emulator-specific remapping contains 6; it omits `phoenix.key` and `site.txt`. Do not conflate these containers or silently discard original entries.
- Whole CPU program member: `sz3mx.03`, **6,291,456 bytes**, SHA-256 `b5f7a1598e4f91a5113c506505b482b2cd1a19e366fe31471740e45dbd204691`.
- **1,536 × 4 KiB pages** accounted for all CPU member bytes. Preliminary labels: 934 `mixed_unresolved`, 579 `repeated_byte`, 23 `low_diversity_data_candidate`.
- Exact local report: `D:\AIOS_SFZ3MIX_V032\evidence\program_classification_v01.json`; includes per-page offset, SHA-256, entropy, byte diversity, classification and `code_verified=false`.
- Rebuild member parity: **PASS**, all 8 entries match name/order, size, CRC and uncompressed SHA-256 between original and newly generated ZIP.
- Repacked ZIP SHA-256: `6c70227b345ffc80cf5a7daf373d9bad5ae157f544a9b8f231414b1c3867d0b1`. Differs from original ZIP `867b835...` because container encoding can differ; **ZIP-byte identity NOT achieved or claimed**.
- Local receipt: `D:\AIOS_SFZ3MIX_V032\evidence\roundtrip_v01_receipt.json`.
- Fixture self-test: **PASS** for unchanged member round-trip, guarded isolated file-offset edit, reverse edit, and confirmation-gate denial. **Fixture only: no real ROM patch made.**

## Interpretation boundaries
This is **complete byte coverage**, NOT full 68000 instruction disassembly, code/data separation, recovered symbols, decompilation or assembly reconstitution. Entropy and repeated bytes are structural hints; code/data remains unresolved. Emulator CPU addresses such as `0x026438` do not automatically correspond to physical offsets in `sz3mx.03`. CPS2 encryption/decryption, region mapping, and bank/layout handling require independent verification before assembly edits.

## Safe workflow
```powershell
python tools/rom_rebuild_v01.py selftest
python tools/rom_rebuild_v01.py classify --source ORIGINAL.zip --report analysis.json
python tools/rom_rebuild_v01.py roundtrip --source ORIGINAL.zip --output disposable_roundtrip.zip --receipt roundtrip_receipt.json
```
`apply` requires a patch manifest with exact source archive SHA-256, target member, byte offsets, expected-old/new hex with equal lengths, and the `--file-offset-mapping-confirmed` flag. It rejects in-place writes and an existing output. `revert` consumes the patch receipt, validates patched-archive SHA-256, restores bytes, and checks every member. **Do not enable this on actual ROM gameplay edits until correct byte mapping is proven**.

## Follow-up technical gates
1. Establish actual instruction entrypoints and CPS2 program-region mapping in emulator/driver; correlate *file* offsets with *CPU* addresses and decrypted opcode view.
2. Install or find a suitable m68k-aware disassembler safely, or reuse the working HBMAME debugger in bounded segments. Ghidra headless and Capstone were **not available through the current Host 02 probes**; do not claim a complete Ghidra project.
3. Mark each decoded instruction with source address, code-confidence, function entry, CFG edges, xrefs, and stable provenance; distinguish executable vs data tables and unused spans.
4. Use [`docs/FUNCTION_LEADS_V01.json`](FUNCTION_LEADS_V01.json) to promote only validated functions. Link each to a community TODO, reproducer, and before/after hash receipt.
5. Validate an actual assembly edit via verified ROM offset mapping, independently built archive, HBMAME and FBNeo gameplay tests, and rollback/netplay preservation before release.

## Privacy and licensing
Never commit ROM members, CPS2 keys, emulator binaries, source archive dumps or full in-game assets. The byte-classification report and test ZIP remain local, while this sanitized receipt and original authored scripts reside in GitHub.
