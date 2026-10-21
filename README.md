# Street Fighter Zero 3 Mix: reverse-engineering and patch work

This repository tracks **incremental patches to the existing SFZ3 Mix v0.32 CPS2 ROM**, preserving the FBNeo/HBMAME ROM workflow. It is **not** a recompilation or replacement game project.

## Community progress

**[Read the community progress report](docs/COMMUNITY_PROGRESS.md)** for a plain-language account of verified reverse-engineering results, historical version comparisons, outstanding gameplay issues, and how to contribute useful bug reports. This page is maintained separately from technical evidence and will not label an issue fixed until in-game acceptance tests pass.

## Pinned historical builds (cloud references)

Older author-hosted SFZ3 Mix releases **0.13 and 0.23–0.31** are pinned in [the historical version catalog](docs/HISTORICAL_RELEASE_PINS_V01.md) and [machine-readable JSON registry](docs/HISTORICAL_RELEASE_PINS_V01.json). **Do not require all reference archives on Host 02**; retrieve only the version needed for a bounded comparison, verify bytes, and preserve sanitized findings. The v0.32 working ROM is unchanged.

## Start here: navigation for people and agents

**New agent?** Read [AGENTS.md](AGENTS.md), then [current status and next action](docs/CURRENT_STATE.md), [community issue backlog](TODO.md), and [knowledge / evidence index](docs/KNOWLEDGE_INDEX.md). The detailed receipts below are retained as historical evidence, not separate competing handoffs.

## Primary working artifact

**The extracted v0.32 ROM program and its related ROM components are the working targets.** Work directly from the existing verified ROM files on Host 02. **Do not instruct agents to unzip or re-extract the distribution ZIP as a standard prerequisite.** The ZIP is only historical input provenance or an optional emulator packaging detail. For the currently indexed CPU program, use `D:\AIOS_SFZ3MIX_V032\tools\sz3mx.03` which was hash-verified on Host 02 (2026-10-20) against the authoritative CPU member SHA-256 `b5f7a1598e4f91a5113c506505b482b2cd1a19e366fe31471740e45dbd204691`; reverify before future changes.

## Current confirmed baseline (2026-10-19)
- Host 02 working tree: `D:\AIOS_SFZ3MIX_V032` (local, not committed).
- Runtime-confirmed continue symptom: score field changes from 0 before defeat to 1 after continuing.
- HBMAME 0.289.3 CPS2Turbo / Motorola 68000 was used to reproduce the issue.
- Historical distribution archive SHA-256 (provenance only): `867B8356872A034EC7E06F776BF757EC2095FEE7616931B71F720F30369806AB`.
- Symptom **reproduced**, causative RAM/68000 writer **not yet isolated**; there is no accepted patch.

## Immediate next work
1. Locate the continue-counter RAM field and its 68000 writers/readers through a bounded trace.
2. Differentiate deliberate counter increment from HUD rendering corruption.
3. Apply an isolated patch to a disposable derivative, retaining the original.
4. Re-run equivalent clean and patched emulator inputs and compare screenshots/memory traces.
5. Record offset, expected bytes, changed bytes, hashes, test commands, failures and acceptance decision.

Other requested targets include continue-screen graphics, Karin slide, Alpha Counter flash, hitboxes, foreground evasion, and Alpha 3 MAX character feasibility. Investigate independently and do not conflate tested ideas with verified behavior.

## Repository policy
Only commit **tools, source, patch deltas, scripts, docs, manifests and suitably reviewed evidence**. Do not commit game ROMs, firmware, redistributed game assets, emulator binaries or large capture dumps. Keep the local working tree as the execution source until a tested, hash-verified transfer is complete.

## Current recovery milestones
- [V01 whole-program byte coverage and reversible ZIP-member roundtrip](docs/WHOLE_PROGRAM_V01.md) (validated, not a full disassembly).
- [32 sampled ROM-data-to-emulator address matches](docs/PROGRAM_MAPPING_SAMPLES_V02.json) (opcode fetch mapping still unverified).
- [Function/address leads registry](docs/FUNCTION_LEADS_V01.json) (hypotheses kept separate from verified recovered functions).
- [Community patch backlog](TODO.md) (all gameplay fixes remain open).

## Instruction-aware recovery milestone
- [Verified M68000 CFG candidate recovery and 26-byte GNU assembler ROM round-trip](docs/INSTRUCTION_RECOVERY_V01.md).
- [59 candidate function entrypoints (not yet promoted)](docs/FUNCTION_REGISTRY_V01.json).
- [Community fix checklist](TODO.md) remains open until gameplay parity tests pass.
