# Community progress report: Street Fighter Zero 3 Mix

**Updated:** 2026-10-21  
**Target:** Original Street Fighter Zero 3 Mix v0.32 (CPS2 ROM for FBNeo/HBMAME)  
**Status:** Reverse engineering underway. **No community gameplay fix has been released or accepted.**

This is the readable public-facing progress page for players, testers, and people who reported gameplay problems. For the detailed technical evidence and current engineering state, see [CURRENT_STATE.md](CURRENT_STATE.md). This page deliberately separates **verified**, **under investigation**, and **not fixed**.

## What we've accomplished

### 1. We're working with the original game
We are examining the game's existing Motorola 68000 program and preserving the v0.32 ROM, rather than building a remake or changing the engine. Work takes place in a separate local testing environment. No modified game ROM is distributed here.

### 2. We can observe actual combat-related code running
Using HBMAME and repeatable experiments, we recorded CPU accesses to player-state memory and matched the observed instructions to bytes in the ROM program. An early controlled run captured **50 distinct CPU-access samples across nine instruction sites**. This established a useful debugging foundation, **not** a confirmed hitbox correction.

### 3. We've traced a specific gameplay decision further
Subsequent controlled traces followed code that computes fighter distance and a separate decision path that checks gameplay state and proximity. We identified a caller, a returned condition, and a possible downstream character-state change. Some tests exercised the rejection path. **We have not yet observed the successful state-change path in live gameplay**, so the specific move or mechanic is not confirmed.

### 4. We have a growing map of game functions
At the current V04 checkpoint, our local evidence database contains **62 function records and 83 call relationships**. We have verified **112 assembly bytes** across five parity regions against the original program, counting reused and newly recovered regions. These are research milestones, not a complete decompilation.

### 5. Historical releases are now indexed
Older releases **v0.13 and v0.23–v0.31** have been cataloged through historical release references. We have begun direct code comparisons of **v0.24, v0.25, and v0.26** to investigate rolling recovery, move eligibility, and grab immunity. Preliminary changes in memory access and program layout have been observed, but **the exact responsible roll/grab routines have not yet been recovered and proven**. Karin's reported rolling animation issue must not be assumed to be the same mechanic.

## What is still open

- **Hitbox/collision complaints:** specific cause and accepted fix not established.
- **Karin rolling/animation behavior:** comparison and gameplay verification pending.
- **Roll recovery and grab immunity changes:** exact historical routines and gameplay effects still being traced.
- **Other community-reported problems:** tracked in the [issue checklist](../TODO.md), not marked fixed without game tests.

## What we're doing next

1. Compare matching gameplay situations across the historical versions in an emulator.
2. Confirm the precise assembly instructions responsible for the behavior changes.
3. Reconstruct any confirmed routines as editable assembly and verify that they reproduce the original bytes.
4. If a relevant improvement can be adapted to v0.32, test a **reversible patch on a disposable copy** against the original, including regression tests.
5. Document successful and unsuccessful results before declaring a fix.

## How the community can help

A reproducible example is extremely useful. For a reported issue, please include **game version, characters, game mode, what you pressed, what you expected, what happened instead**, and ideally a short clip or replay. Historical builds or changelog references can help us isolate when a behavior changed.

You can follow our technical work in [the current state](CURRENT_STATE.md), inspect [historical version references](HISTORICAL_RELEASE_PINS_V01.md), or review the [community checklist](../TODO.md).

**Important:** A recorded instruction, theoretical branch, or promising comparison is not the same as an in-game fix. We'll update this page as evidence passes testing.

*This is an independent research effort, not an official SFZ3 Mix release.*
