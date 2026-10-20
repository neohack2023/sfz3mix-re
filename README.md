# Street Fighter Zero 3 Mix: reverse-engineering and patch work

This repository tracks **incremental patches to the existing SFZ3 Mix v0.32 CPS2 ROM**, preserving the FBNeo/HBMAME ROM workflow. It is **not** a recompilation or replacement game project.

## Current confirmed baseline (2026-10-19)
- Host 02 working tree: `D:\AIOS_SFZ3MIX_V032` (local, not committed).
- Runtime-confirmed continue symptom: score field changes from 0 before defeat to 1 after continuing.
- HBMAME 0.289.3 CPS2Turbo / Motorola 68000 was used to reproduce the issue.
- Original downloaded archive SHA-256: `867B8356872A034EC7E06F776BF757EC2095FEE7616931B71F720F30369806AB`.
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
