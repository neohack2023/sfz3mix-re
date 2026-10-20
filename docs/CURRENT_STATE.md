# Current state: next agent handoff
Updated: 2026-10-20. This is the living status document; see [knowledge index](KNOWLEDGE_INDEX.md) for deeper evidence.

## Mission
Produce reversible patches for **SFZ3 Mix v0.32 as an FBNeo-compatible CPS2 ROM**, preserving the user's community [TODO list](../TODO.md). Do not make a recompilation or clone the existing workspace.

## Confirmed accomplishments
- Original ZIP hash: `867b8356872a034ec7e06f776bf757ec2095fee7616931b71f720f30369806ab`. Original has eight entries, HBMAME mapping uses six.
- HBMAME 0.289.3 reproduces the score changing from 0 to 1 after continuing; root cause unresolved.
- Byte-level accounting covers 6 MiB CPU member, but is **not** whole-ROM disassembly.
- 32 sampled HBMAME program-data reads match original CPU member offsets, **not proven opcode-fetch mapping**.
- Capstone CFG: 839 *candidate* instructions, 414 edges, 59 *unverified* entrypoints.
- GNU M68000 assembler reassembled one genuine 26-byte code fragment exactly; clean archive reconstruction preserved all eight members. **No patch accepted.**
- Host 02 workspace: `D:\AIOS_SFZ3MIX_V032`. Last D: free-space check approximately 96 MiB. Verify available space before further work.

## Next execution target
**Validate opcode-fetch mapping using bounded HBMAME instruction traces.** Compare decoded runtime instructions to original bytes and existing Capstone CFG; discover new runtime-backed entrypoints and indirect branches. Expand the function registry with evidence levels and link validated routines to the community TODO. Reassemble every newly verified assembly fragment byte-identically before proposing any change.

## Gates
1. Original hash and free space confirmed.
2. Before/after measurements and trace recorded with CPU and file address space identified.
3. New functions annotated with caller/callee, instructions, confidence, and proof.
4. No original ROM overwritten; no bulk duplicate archive.
5. Dated receipt committed without copyrighted ROM bytes; update this page and [index](KNOWLEDGE_INDEX.md).

## Blockers and cautions
- Opcode-fetch/decryption parity and complete code/data separation remain unresolved.
- No whole-ROM build from assembly, no complete function map, no accepted community fixes.
- A prior vector-disassembly probe did not produce expected files; revalidate the launch mode.
- Dedicated SFZ3 row not confirmed in Drive project-scope registry.
- FBNeo rollback/netplay acceptance untested.

## Key links
- [Community issues](../TODO.md)
- [Latest instruction recovery](INSTRUCTION_RECOVERY_V01.md)
- [Candidate functions](FUNCTION_REGISTRY_V01.json)
- [Historical tools, attempts and evidence](RE_ENGINEERING_HANDOFF_2026-10-20.md)

Update this short document only after testing; preserve immutable historic reports.
