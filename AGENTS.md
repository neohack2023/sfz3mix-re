# Agent onboarding: Street Fighter Zero 3 Mix

Start with [current state](docs/CURRENT_STATE.md), then the [community TODO](TODO.md) and [knowledge index](docs/KNOWLEDGE_INDEX.md). Read detailed historical receipts only as needed.

**Goal:** Patch the original SFZ3 Mix v0.32 CPS2 ROM for FBNeo/HBMAME. Do not create a recompilation or another project clone.

**Sources of truth:** GitHub main stores tested tools and sanitized research; Host 02 at `D:\AIOS_SFZ3MIX_V032` stores original ROM and runtime evidence; Google Drive's AIOS scope registry governs formally registered scopes. A dedicated SFZ3 scope has not yet been confirmed.

**Rules:** Verify original hashes and available disk space before work. Separate runtime proof, static candidates, failed approaches, and accepted fixes. Never commit copyrighted ROM data, keys, emulator binaries, or large captures. Changes to gameplay require reversible offsets, before/after hashes, and emulator regression tests. Program data-space and opcode-fetch mappings must be validated separately.

After verified progress, update `docs/CURRENT_STATE.md`, preserve a dated test receipt, update the knowledge index if new tools or findings are added, and only mark `TODO.md` completed when a fix passes acceptance.
