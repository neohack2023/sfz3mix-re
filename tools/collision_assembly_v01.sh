#!/usr/bin/env bash
set -euo pipefail
root="/mnt/d/AIOS_SFZ3MIX_V032"
tool="$root/tools/.m68k_toolchain/usr/bin"
export LD_LIBRARY_PATH="$root/tools/.m68k_toolchain/usr/lib/x86_64-linux-gnu"
"$tool/m68k-linux-gnu-as" -m68000 -o "$root/evidence/collision_leaf_02c19a_v01.o" "$root/tools/collision_leaf_02c19a_v01.s"
"$tool/m68k-linux-gnu-objcopy" -O binary -j .text "$root/evidence/collision_leaf_02c19a_v01.o" "$root/evidence/collision_leaf_02c19a_v01.bin"
"$tool/m68k-linux-gnu-objdump" -dr "$root/evidence/collision_leaf_02c19a_v01.o" > "$root/evidence/collision_leaf_02c19a_v01_objdump.txt"
