# Instruction-aware M68000 recovery V01 — tested handoff (2026-10-20)

**Game:** SFZ3 Mix v0.32, original ROM patch path, not recompilation. **Host:** DaltonsLaptop574 / `D:\AIOS_SFZ3MIX_V032`. **No community gameplay fix is claimed.**

## Verified inputs and toolchain
- Source ZIP SHA-256 `867b8356872a034ec7e06f776bf757ec2095fee7616931b71f720f30369806ab`.
- CPU member `sz3mx.03`, 6,291,456 bytes, SHA-256 `b5f7a1598e4f91a5113c506505b482b2cd1a19e366fe31471740e45dbd204691`.
- Isolated Capstone 5.0.6 at `tools/.vendor` and GNU binutils 2.38 cross-assembler/objcopy in `tools/.m68k_toolchain`, invoked with existing WSL Ubuntu. Toolchain binaries stay local.
- Samples from the earlier probe matched 32/32 HBMAME program-data addresses to same CPU member offsets. HBMAME's CPS2 Turbo driver also declares a **separate opcode fetch map**, so direct instruction-fetch parity still needs explicit validation.

## Bounded instruction-aware discovery (PASS as *candidates*)
- [`m68k_cfg_v01.py`](../tools/m68k_cfg_v01.py) decodes Motorola 68000 instructions, follows direct branches/calls and conditional fallthrough, and records unknown indirect transfers. Entry seeds: reset/vector candidates (conservative first 32 longwords) plus earlier debugger-known regions.
- Latest local artifact `evidence/m68k_cfg_v02.json`: **839 static instruction candidates; 2,978 candidate-code bytes; 414 edges; 76 direct call edges; 59 candidate function entries**. 6,288,478 bytes not validated as code. Neither full disassembly nor complete code/data classification is proven.
- Synthetic [`test_m68k_cfg_v01.py`](../tools/test_m68k_cfg_v01.py): **PASS** for BSR, BEQ, both fallthroughs, RTS and call target.
- Sanitized [`FUNCTION_REGISTRY_V01.json`](FUNCTION_REGISTRY_V01.json) records all 59 entry candidates, addresses and evidence status, without publishing program bytes. Each remains `UNVERIFIED_STATIC_ENTRY_CANDIDATE`.
- Local `evidence/m68k_snippets_v02.s` carries annotated byte-exact diagnostic slices; the comments are not yet independently reassembled mnemonics outside the test slice.

## Genuine GNU-as assembly-to-ROM round-trip (PASS for one 26-byte fragment)
- [`sfz_buffer_writer_v01.s`](../tools/sfz_buffer_writer_v01.s) is *seven actual assembly instructions* at program offset `0x00331C`; it includes indexed `move.l`, `addi.w`, `andi.w`, `move.w` and `rts`. Its gameplay function is not confirmed.
- [`assembly_roundtrip_v01.sh`](../tools/assembly_roundtrip_v01.sh) uses `m68k-linux-gnu-as -m68000` plus objcopy and emitted 26 bytes.
- [`verify_assembly_rom_v01.py`](../tools/verify_assembly_rom_v01.py) compared assembled bytes against original bytes. **Identical** SHA-256 `1e10baeac9c614e6ddca06aff970b38ee96bf33ddfcbd91d904570ce1d1406e7`.
- The verifier replaced that exact span in a disposable archive reconstructed from the *original eight members*. **PASS 8/8 identical uncompressed members** (name/order/CRC/hash). The resulting ZIP had a different container hash, as expected. Test receipt: `evidence/assembly_roundtrip_v01_receipt.json`. Disposable ZIP deleted after receipt. Original unchanged.
- This is *not* proof that the entire CPU program has been assembled from source, nor that any new gameplay patch works.

## Next acceptance gates
1. Cross-check opcode fetch/decryption versus original member and HBMAME's actual disassembly; avoid confusing data-space mapping with instruction fetch.
2. Extend CFG entry evidence with bounded runtime PC traces, indirect call and jump table resolution and verify function boundaries.
3. Promote resolved and observed routines individually into the registry; connect source-backed functions to the [community TODO](../TODO.md), including countdown artifacts, continue counter, Karin rolling, Alpha Counter flash, hitboxes, background evasion.
4. Broaden the editable assembly source incrementally while proving each original-code reassembly equals source bytes; keep unknown spans explicitly data/unknown.
5. Only then attempt a nontrivial reversible patch in a disposable ROM, then test both HBMAME and FBNeo and required netplay/rollback behavior.

## Local execution
```powershell
python D:\AIOS_SFZ3MIX_V032\tools\test_m68k_cfg_v01.py
wsl -d AIOS-Ubuntu-22.04 -- bash /mnt/d/AIOS_SFZ3MIX_V032/tools/assembly_roundtrip_v01.sh
# Original assembly verification already generated an immutable receipt; don't rerun it over that path.
```

Do not commit the ROM archive, individual ROM members, firmware/keys, emulators, decrypted dumps, or raw machine-code inventories. Do not create another game clone. No CI run was needed.

## Storage safety checkpoint
A final Host 02 check found **96,468,992 bytes free on D:**, so additional bulk disassembly or video capture must be deferred or directed to an approved location with verified room. The isolated cross-assembler files total approximately 5.0 MB and the Python vendor directory approximately 9.0 MB; the larger decrease in free space observed during this session is **not attributed to these tools without evidence**. No unrelated files were deleted. The original archive hash was rechecked and still matches its pinned value, and the disposable rebuild ZIP is absent.
