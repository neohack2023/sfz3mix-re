#!/usr/bin/env python3
"""SFZ3 Mix v0.32: lossless-member ROM package analysis and reversible patch fixture.
No CPU address-to-file offset mapping is assumed or derived here.
"""
import argparse
import collections
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import tempfile
import zipfile

ORIGINAL_SHA256 = "867b8356872a034ec7e06f776bf757ec2095fee7616931b71f720f30369806ab"
PROGRAM_NAME = "sz3mx.03"
PAGE_SIZE = 4096

def sha(data):
    return hashlib.sha256(data).hexdigest()

def file_sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()

def assert_original(path):
    digest = file_sha(path)
    if digest != ORIGINAL_SHA256:
        raise ValueError("Original ZIP SHA256 mismatch: " + digest)
    return digest

def entries(path):
    with zipfile.ZipFile(path) as z:
        if z.testzip() is not None:
            raise ValueError("ZIP member CRC failure")
        if len(set(z.namelist())) != len(z.namelist()):
            raise ValueError("Duplicate member name")
        return [{"name": i.filename, "size": i.file_size,
                 "crc32": f"{i.CRC:08X}", "sha256": sha(z.read(i)),
                 "compress_type": i.compress_type} for i in z.infolist()]

def write_json(path, record):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(str(path))
    path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")

def classify(path, output):
    digest = assert_original(path)
    manifest = entries(path)
    with zipfile.ZipFile(path) as z:
        data = z.read(PROGRAM_NAME)
    if len(data) != 6291456:
        raise ValueError("Unexpected program length")
    pages = []
    for base in range(0, len(data), PAGE_SIZE):
        block = data[base:base + PAGE_SIZE]
        counts = collections.Counter(block)
        entropy = -sum((n / len(block)) * math.log2(n / len(block))
                       for n in counts.values())
        if len(counts) == 1:
            label = "repeated_byte"
        elif len(counts) <= 8 or entropy < 3:
            label = "low_diversity_data_candidate"
        elif entropy >= 7.75:
            label = "high_entropy_unresolved"
        else:
            label = "mixed_unresolved"
        pages.append({"file_offset": base, "length": len(block),
                      "sha256": sha(block), "entropy": round(entropy, 4),
                      "unique_bytes": len(counts), "most_common": counts.most_common(1)[0][0],
                      "label": label, "code_verified": False})
    hist = dict(collections.Counter(p["label"] for p in pages))
    record = {"schema": "sfz3mix.program_classification.v1",
              "classification": "byte-coverage heuristics ONLY; not disassembly, no code/data proof",
              "source_zip_sha256": digest, "cpu_member": PROGRAM_NAME,
              "cpu_sha256": sha(data), "cpu_bytes": len(data),
              "page_size": PAGE_SIZE, "pages_classified": len(pages),
              "bytes_accounted": sum(p["length"] for p in pages),
              "labels": hist, "archive_members": manifest,
              "known_emulator_addresses_not_file_offsets": ["0x025C40", "0x00331C", "0x026438"],
              "pages": pages}
    assert record["bytes_accounted"] == len(data)
    write_json(output, record)
    print(json.dumps({k: record[k] for k in
        ("cpu_bytes", "pages_classified", "bytes_accounted", "labels", "cpu_sha256")}, indent=2))
    return record

def rebuild(source, target, transforms=None):
    source, target = Path(source), Path(target)
    if source.resolve() == target.resolve():
        raise ValueError("Refusing in-place archive modification")
    if target.exists():
        raise FileExistsError(str(target))
    target.parent.mkdir(parents=True, exist_ok=True)
    transforms = transforms or {}
    temp = target.with_name(target.name + ".partial")
    if temp.exists():
        raise FileExistsError(str(temp))
    try:
        with zipfile.ZipFile(source) as inp, zipfile.ZipFile(temp, "w") as out:
            if inp.testzip() is not None:
                raise ValueError("Input archive CRC failed")
            out.comment = inp.comment
            for info in inp.infolist():
                payload = inp.read(info)
                if info.filename in transforms:
                    payload = transforms[info.filename](payload)
                out.writestr(copy.copy(info), payload)
        os.replace(temp, target)
    finally:
        if temp.exists():
            temp.unlink()

def verify_members(a, b):
    aa, bb = entries(a), entries(b)
    if len(aa) != len(bb):
        raise ValueError("Member count differs")
    for i, (x, y) in enumerate(zip(aa, bb)):
        if (x["name"], x["size"], x["crc32"], x["sha256"]) != (
            y["name"], y["size"], y["crc32"], y["sha256"]):
            raise ValueError("Member mismatch at index " + str(i))
    return len(aa)

def roundtrip(source, output, receipt):
    original = assert_original(source)
    rebuild(source, output)
    count = verify_members(source, output)
    row = {"status": "PASS", "type": "member_byte_identical_roundtrip",
           "input_archive_sha256": original, "output_archive_sha256": file_sha(output),
           "member_count": count, "all_member_order_crc_sha256_equal": True,
           "archive_bytes_identical": original == file_sha(output),
           "warning": "A changed ZIP hash is normal after recompression. This is NOT an assembly rebuild."}
    write_json(receipt, row)
    print(json.dumps(row, indent=2))

def change_bytes(raw, edits, reverse=False):
    dst = bytearray(raw)
    used = set()
    for e in edits:
        pos = int(e["offset"])
        old = bytes.fromhex(e["new_hex"] if reverse else e["old_hex"])
        new = bytes.fromhex(e["old_hex"] if reverse else e["new_hex"])
        if not old or len(old) != len(new):
            raise ValueError("Edits must have equal nonzero lengths")
        if pos < 0 or pos + len(old) > len(raw):
            raise ValueError("Edit out of bounds")
        span = set(range(pos, pos + len(old)))
        if used & span:
            raise ValueError("Overlapping edits")
        used |= span
        if dst[pos:pos + len(old)] != old:
            raise ValueError("Expected old bytes mismatch at file offset " + str(pos))
        dst[pos:pos + len(old)] = new
    return bytes(dst)

def apply(source, output, patch_json, receipt, mapping_confirmed=False):
    if not mapping_confirmed:
        raise ValueError("Explicit --file-offset-mapping-confirmed is required")
    patch = json.loads(Path(patch_json).read_text(encoding="utf-8"))
    if file_sha(source) != patch["source_archive_sha256"]:
        raise ValueError("Patch source archive mismatch")
    group = patch["member"]
    originals = entries(source)
    if group not in [e["name"] for e in originals]:
        raise ValueError("Patch member missing")
    rebuild(source, output, {group: lambda b: change_bytes(b, patch["edits"])})
    affected = [e for e in originals if e["name"] == group][0]
    result = {"status": "PATCH_APPLIED_REVIEW_REQUIRED",
              "original_archive_sha256": file_sha(source),
              "patched_archive_sha256": file_sha(output),
              "member": group, "original_member_sha256": affected["sha256"],
              "edits": patch["edits"], "unmodified_member_sha256": {
                  e["name"]: e["sha256"] for e in originals if e["name"] != group}}
    write_json(receipt, result)
    print(json.dumps({"status": result["status"], "patched_sha256": result["patched_archive_sha256"]}, indent=2))

def revert(source, output, receipt_json):
    receipt = json.loads(Path(receipt_json).read_text(encoding="utf-8"))
    if file_sha(source) != receipt["patched_archive_sha256"]:
        raise ValueError("Patched archive SHA256 mismatch")
    group = receipt["member"]
    rebuild(source, output, {group: lambda b: change_bytes(b, receipt["edits"], True)})
    actual = {e["name"]: e["sha256"] for e in entries(output)}
    if actual[group] != receipt["original_member_sha256"]:
        raise ValueError("Restored member SHA256 mismatch")
    for name, digest in receipt["unmodified_member_sha256"].items():
        if actual.get(name) != digest:
            raise ValueError("Non-target member changed: " + name)
    print(json.dumps({"status": "RESTORED_MEMBER_BYTES_PASS",
                      "reverted_archive_sha256": file_sha(output),
                      "archive_byte_identity_not_implied": True}, indent=2))

def selftest():
    with tempfile.TemporaryDirectory(prefix="sfz3_repro_") as root:
        p = Path(root)
        original = p / "fixture.zip"
        with zipfile.ZipFile(original, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("cpu.bin", bytes(range(256)) * 4)
            z.writestr("other.bin", b"Unchanged")
        roundtrip_fixture = p / "roundtrip.zip"
        rebuild(original, roundtrip_fixture)
        assert verify_members(original, roundtrip_fixture) == 2
        patch = {"source_archive_sha256": file_sha(original),
                 "member": "cpu.bin", "edits": [{"offset": 16, "old_hex": "101112", "new_hex": "f1f2f3"}]}
        spec = p / "patch.json"
        spec.write_text(json.dumps(patch), encoding="utf-8")
        applied = p / "patched.zip"
        receipt = p / "patch_receipt.json"
        apply(original, applied, spec, receipt, mapping_confirmed=True)
        restored = p / "restored.zip"
        revert(applied, restored, receipt)
        assert verify_members(original, restored) == 2
        try:
            apply(original, p / "invalid.zip", spec, p / "invalid_receipt.json", mapping_confirmed=False)
        except ValueError:
            pass
        else:
            raise AssertionError("Mapping confirmation gate failed")
    print("SELFTEST_PASS: fixture member roundtrip, isolated edit, restore, explicit mapping gate")

def main():
    p = argparse.ArgumentParser()
    s = p.add_subparsers(dest="cmd", required=True)
    a = s.add_parser("classify")
    a.add_argument("--source", type=Path, required=True)
    a.add_argument("--report", type=Path, required=True)
    b = s.add_parser("roundtrip")
    b.add_argument("--source", type=Path, required=True)
    b.add_argument("--output", type=Path, required=True)
    b.add_argument("--receipt", type=Path, required=True)
    c = s.add_parser("apply")
    c.add_argument("--source", type=Path, required=True)
    c.add_argument("--output", type=Path, required=True)
    c.add_argument("--patch", type=Path, required=True)
    c.add_argument("--receipt", type=Path, required=True)
    c.add_argument("--file-offset-mapping-confirmed", action="store_true")
    d = s.add_parser("revert")
    d.add_argument("--source", type=Path, required=True)
    d.add_argument("--output", type=Path, required=True)
    d.add_argument("--receipt", type=Path, required=True)
    s.add_parser("selftest")
    x = p.parse_args()
    if x.cmd == "classify": classify(x.source, x.report)
    if x.cmd == "roundtrip": roundtrip(x.source, x.output, x.receipt)
    if x.cmd == "apply": apply(x.source, x.output, x.patch, x.receipt, x.file_offset_mapping_confirmed)
    if x.cmd == "revert": revert(x.source, x.output, x.receipt)
    if x.cmd == "selftest": selftest()

if __name__ == "__main__":
    main()
