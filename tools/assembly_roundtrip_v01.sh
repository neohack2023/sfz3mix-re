#!/usr/bin/env bash
set -euo pipefail
root="/mnt/d/AIOS_SFZ3MIX_V032"
tool="$root/tools/.m68k_toolchain/usr/bin"
export LD_LIBRARY_PATH="$root/tools/.m68k_toolchain/usr/lib/x86_64-linux-gnu"
src="$root/tools/sfz_buffer_writer_v01.s"
out="$root/evidence/sfz_buffer_writer_v01"
"$tool/m68k-linux-gnu-as" -m68000 -o "$out.o" "$src"
"$tool/m68k-linux-gnu-objcopy" -O binary -j .text "$out.o" "$out.bin"
echo "ASSEMBLER_RC_0"
wc -c "$out.bin"
