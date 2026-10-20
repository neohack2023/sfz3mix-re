#!/usr/bin/env python3
"""Validate genuine M68K GNU-as machine code against original bytes and all-member ROM package roundtrip."""
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile
import rom_rebuild_v01 as base

root=Path(r"D:\AIOS_SFZ3MIX_V032")
orig=root/"downloads/sfz3mix_v032_original.zip"
assembled=root/"evidence/sfz_buffer_writer_v01.bin"
output=root/"evidence/assembly_roundtrip_v01_disposable.zip"
receipt=root/"evidence/assembly_roundtrip_v01_receipt.json"
off=0x00331C
assert base.assert_original(orig)==base.ORIGINAL_SHA256
with ZipFile(orig) as zipf: rom=zipf.read("sz3mx.03")
machine=assembled.read_bytes()
assert len(machine)==26, "Unexpected assembled code size"
prior=rom[off:off+len(machine)]
if machine!=prior:
    mismatches=[{"offset_hex":f"0x{off+i:06X}","original":f"{x:02X}","assembled":f"{y:02X}"}
                for i,(x,y) in enumerate(zip(prior,machine)) if x!=y]
    raise AssertionError("Machine-code mismatch: "+json.dumps(mismatches[:20]))
if output.exists() or receipt.exists():
    raise FileExistsError("Refusing overwrite of prior test")
def replace(raw):
    if raw[off:off+len(machine)]!=machine:
        raise AssertionError("Original ROM bytes changed")
    b=bytearray(raw)
    b[off:off+len(machine)]=machine
    return bytes(b)
try:
    base.rebuild(orig,output,{"sz3mx.03":replace})
    count=base.verify_members(orig,output)
    rec={"status":"PASS_ASSEMBLED_26_BYTE_SLICE_AND_8_MEMBER_ROUNDTRIP",
         "assembler":"GNU binutils m68k-linux-gnu-as -m68000 2.38",
         "source_program_file_offset":"0x00331C",
         "assembled_source":"tools/sfz_buffer_writer_v01.s",
         "verified_compiled_bytes":len(machine),
         "assembled_sha256":base.sha(machine),
         "original_slice_sha256":base.sha(prior),
         "source_archive_sha256":base.file_sha(orig),
         "repacked_archive_sha256":base.file_sha(output),
         "all_members_unchanged":True,
         "verified_member_count":count,
         "gameplay_patch":False,
         "repacked_zip_removed_after_validation":True}
    base.write_json(receipt,rec)
    print(json.dumps(rec,indent=2))
finally:
    if output.exists(): output.unlink()
