# Current state: next agent handoff
Updated: 2026-10-20. This is the living status document; see [knowledge index](KNOWLEDGE_INDEX.md) for deeper evidence.

## Mission
Produce reversible patches for **SFZ3 Mix v0.32 as an FBNeo-compatible CPS2 ROM**, preserving the user's community [TODO list](../TODO.md). Do not make a recompilation or clone the existing workspace.

## Working input policy
Use the existing extracted ROM files on Host 02 directly. Verify CPU program `sz3mx.03` SHA-256 `b5f7a1598e4f91a5113c506505b482b2cd1a19e366fe31471740e45dbd204691` before analysis; currently indexed local candidate path is `D:\AIOS_SFZ3MIX_V032\tools\sz3mx.03`, which was hash-verified on Host 02 (2026-10-20). Recheck before future changes. **No ZIP extraction/repack step is required for function discovery or source reassembly.** Distribution-archive mapping is historical and optional for emulator packaging.

## Confirmed accomplishments
- Historical ZIP provenance hash (not the central working artifact): `867b8356872a034ec7e06f776bf757ec2095fee7616931b71f720f30369806ab`. Original has eight entries, HBMAME mapping uses six.
- HBMAME 0.289.3 reproduces the score changing from 0 to 1 after continuing; root cause unresolved.
- Byte-level accounting covers 6 MiB CPU member, but is **not** whole-ROM disassembly.
- 32 sampled HBMAME program-data reads match original CPU member offsets, **not proven opcode-fetch mapping**.
- Capstone CFG: 839 *candidate* instructions, 414 edges, 59 *unverified* entrypoints.
- GNU M68000 assembler reassembled one genuine 26-byte code fragment exactly; clean archive reconstruction preserved all eight members. **No patch accepted.**
- Host 02 workspace: `D:\AIOS_SFZ3MIX_V032`. Previous D: free-space check approximately 96 MiB; latest check 2026-10-20 returned **38 MiB**. Avoid new large local traces, snapshots or duplicate ROM copies until storage is reconciled. Verify available space before further work.

## Next execution target
**Validate opcode-fetch mapping using bounded HBMAME instruction traces.** Compare decoded runtime instructions to original bytes and existing Capstone CFG; discover new runtime-backed entrypoints and indirect branches. Expand the function registry with evidence levels and link validated routines to the community TODO. Reassemble every newly verified assembly fragment byte-identically before proposing any change.

## Gates
1. Existing extracted ROM component hashes and free space confirmed.
2. Before/after measurements and trace recorded with CPU and file address space identified.
3. New functions annotated with caller/callee, instructions, confidence, and proof.
4. No original ROM overwritten; no bulk duplicate archive.
5. Dated receipt committed without copyrighted ROM bytes; update this page and [index](KNOWLEDGE_INDEX.md).

## Blockers and cautions
- Opcode-fetch/decryption parity and complete code/data separation remain unresolved.
- No whole-ROM build from assembly, no complete function map, no accepted community fixes.
- A prior vector-disassembly probe did not produce expected files; revalidate the launch mode.
- Dedicated SFZ3 registration is now verified; see the latest authority/trace checkpoint below.
- FBNeo rollback/netplay acceptance untested.

## Key links
- [Community issues](../TODO.md)
- [Latest instruction recovery](INSTRUCTION_RECOVERY_V01.md)
- [Candidate functions](FUNCTION_REGISTRY_V01.json)
- [Historical tools, attempts and evidence](RE_ENGINEERING_HANDOFF_2026-10-20.md)

Update this short document only after testing; preserve immutable historic reports.

## New function database capability
Function Database V01 passed the Host 02 SQLite build and address query tests: 59 candidate entries, 76 static direct-call sites with unresolved caller owners, and 4 issue associations. See [Function Database V01](FUNCTION_DATABASE_V01.md). These are searchable leads, not confirmed recovered functions.

## Unmodified Capcom base ROM reference
[sfa3us source and CRC manifest](ORIGINAL_SFA3US_REFERENCE.md) identified; no verified local original has been found or acquired. This remains a separate comparison reference, not a replacement for hacked v0.32.

## Latest runtime RAM/collision-table evidence (2026-10-20)
- [New read-only runtime comparison](SFA3_RAM_COMPATIBILITY_V01.md) shows dynamic original-SFA3-profile player structures at 0xFF8400 and 0xFF8800 (**0x400 player slot stride**); two additional historical player slots inactive. Projectile base 0xFF9400 / 0x100 stride remains untested with a fired projectile. An initial probe wrongly used 0x100 as player spacing; that interpretation is superseded.
- Historical pointer+box-ID indexing resolved **20/20 active samples** to readable, plausible 8-byte dimension records within the hash-verified extracted v0.32 CPU program (**16 distinct addresses**). This corroborates stored data structure, not engine collision use.
- SQLite function database contains 2 RAM structure pools, 28 slots, 14 fields, 88 observations, 2 hitbox-issue investigation links and 20 decoded box entries. Previous 59 function candidates and 76 call sites retained; **0 verified instruction-to-RAM/function xrefs**.
- Next gate: bounded read-only instruction/memory access trace at 0xFF8490, 0xFF849C, 0xFF8890, 0xFF889C and corresponding ROM record addresses during real attacks; only after verified PC and function ownership should xrefs be promoted.

## Latest validation and storage warning
Last runtime audit (2026-10-20) reconfirmed extracted CPU member SHA-256 `b5f7a1598e4f91a5113c506505b482b2cd1a19e366fe31471740e45dbd204691`, five new Python scripts pass syntax checks, and the upgraded SQLite database passes `PRAGMA integrity_check` with 59 functions, 76 calls, 28 RAM slots, 88 observations, 20 box decodes, and 0 function-RAM xrefs. **D: free space was only 39,845,888 bytes (~38 MiB).** Cause of the additional reduction was not established; investigate before any further bulk capture.

## Registered authority and collision instruction trace — 2026-10-20
**Governance recovered; execution resumed.** Scope `github:neohack2023/sfz3mix-re` is saved in Drive Project Scope Registry `REGISTRY!A24:V24`, parent `global-working-memory`; all cells and required pointers passed readback. Host 02 router/context binding `sfz3mix-v032` maps to the existing D: workspace. Canonical and actual launch preflights returned `READY_CONTINUE / ALL_REQUIRED_PREFLIGHT_COMPONENTS_PASS`.

[Existing recovery receipt, now including successful continuation](AUTHORITY_RECOVERY_2026-10-20.md) records exact commands, receipts and limits. HBMAME completed a bounded 3100-frame run: 50 distinct samples, 31 reads, 9 instruction sites. Confirmed readers include `0x027EF0` (+0x90 pointer), `0x029A42/46` and `0x02C1AC` (+0x9C pointers), and `0x02C1A6` (+0xCB selector). All nine observed instruction byte sequences match exact CPU file offsets and runtime IR. No whole-program opcode parity claim.

Existing SQLite now includes 9 runtime instructions, 50 access samples, 74 links to existing RAM fields and 9 investigative hitboxes links. All function owners remain null: function extent/call ownership has not been verified. Original 59 candidates, 76 calls, 20 box decodes and zero function-RAM xrefs preserved. Pre/post integrity and FK checks pass; CPU hash reconfirmed unchanged. No gameplay modifications.

Next: establish function boundaries/call paths for these exact reader PCs and trace selected collision-record accesses; keep unverified relationships separate. Preserve fixed-name raw outputs before rerunning the probe. D: final free space was 29,360,128 bytes (~28 MiB), down from ~38 MiB; cause unverified. Recheck storage before another run. Root AGENTS.md remains absent from the D: runtime workspace; use the existing GitHub entrypoint without cloning.
