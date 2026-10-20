# Continue counter: investigation receipt (2026-10-19)

**Status:** reproduced in emulator; root cause and patch pending.

- Execution host: WINDOWS_EXECUTION_HOST_02 (DaltonsLaptop574)
- Local source receipt: `D:\AIOS_SFZ3MIX_V032\EXECUTION_RECEIPT.md`
- Runtime: HBMAME 0.289.3 (Windows x64, CPS2Turbo, Motorola 68000)
- Evidence class: emulator runtime only; physical hardware not tested
- Source zip SHA-256: `867B8356872A034EC7E06F776BF757EC2095FEE7616931B71F720F30369806AB`
- CPU entry recorded: `sz3mx.03`, 6,291,456 bytes, CRC32 `7A968DA6`
- Emulator audit: 1 ROM set OK

## Reproduction
A clean v0.32 boot and Lua-driven input sequence began a CPU match as Ryu/E.Honda/Blanka vs Sakura. Before continuing, the top-left score field displayed `0`. After the defeat, CONTINUE countdown, second coin and start/select flow, it displayed `1`.

Local evidence: `evidence/continue_press_log.txt`, `evidence/snapshots_extended`, `evidence/snapshots_window`, `evidence/snapshots_continue_pressed`. Local input reproducer: `tools/continue_press.lua`.

**Interpretation limit:** this establishes the visible symptom only, not which 68000 routine caused it or whether the score increment is intended.

## Required acceptance
Identify counter storage and writes; construct a minimal reversible patch; demonstrate deterministic clean-vs-patched behavior; log ROM hashes and byte-level changes. Do not mark patched or fixed before these checks.

Environment note: the source receipt says the FBNeo license was not accepted for that session; testing used HBMAME instead. Original ROM content stays local.
