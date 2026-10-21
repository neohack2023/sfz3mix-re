#!/usr/bin/env python3
"""Bounded, temporary historical SFZ3 Mix comparison. No ROM contents emitted."""
import hashlib, json, os, shutil, subprocess, tempfile, urllib.request, zlib
from pathlib import Path

VERSIONS = range(23, 28)
URL = "https://sfz3mix.github.io/download/{version}/sfz3mix.7z"
SEVENZIP = Path(r"C:\Program Files\7-Zip\7z.exe")
ROOT = Path(os.environ.get("SFZ3MIX_TEMP_ROOT",r"C:\AIOS\_TEMP"))
PAGE = 4096

def sha(b): return hashlib.sha256(b).hexdigest()
def category(p):
    n=p.name.lower()
    if n in {"sfz3mix.p1","sz3mx.03","maincpu.bin"}:return "cpu"
    if n in {"sfz3mix.c1","sfz3mix.c2","sz3mx.13m","sz3mx.21m","gfx.bin","gfx2.bin"}:return "graphics"
    if n in {"sfz3mix.m1","sz3mx.01","audiocpu.bin"}:return "soundcpu"
    if n in {"sfz3mix.q1","sz3mx.11m","qsound.bin"}:return "samples"
    return "other"
def boundaries(a,b):
    shared=min(len(a),len(b));modified=[]
    for start in range(0,shared,PAGE):
        aa=a[start:start+PAGE]; bb=b[start:start+PAGE]
        if aa!=bb:modified.append({"offset":start,"changed_bytes":sum(x!=y for x,y in zip(aa,bb)),"sha_before":sha(aa)[:12],"sha_after":sha(bb)[:12]})
    groups=[]
    for p in modified:
        if groups and p["offset"]==groups[-1]["end"]:
            groups[-1]["end"]+=PAGE;groups[-1]["changed_bytes"]+=p["changed_bytes"];groups[-1]["pages"]+=1
        else:groups.append({"start":p["offset"],"end":p["offset"]+PAGE,"pages":1,"changed_bytes":p["changed_bytes"]})
    return {"shared_bytes":shared,"changed_pages":len(modified),"total_shared_pages":(shared+PAGE-1)//PAGE,"different_bytes":sum(p["changed_bytes"] for p in modified),"trailing_bytes":abs(len(a)-len(b)),"ranges":groups[:80],"ranges_omitted":max(0,len(groups)-80),"sample_pages":modified[:12]}
def main():
    if not SEVENZIP.exists():raise RuntimeError("7zip binary missing")
    ROOT.mkdir(parents=True,exist_ok=True)
    if shutil.disk_usage(ROOT).free < 2*1024**3:raise RuntimeError("Require >=2GiB available C:")
    result={"schema":"sfz3mix_historical_23_27_binary_slice_v01","status":"STRUCTURAL_ONLY","generation":"CPS2Turbo","versions":[],"adjacent_pairs":[],"caveats":["Differences are bytes/chunks, not identified routines or gameplay causes.","Prior to v0.26 program file renamed, compare by content role.","No executable or proprietary bytes are emitted.","No gameplay traces or patches performed."]}
    previous=None
    for n in VERSIONS:
        version=f"0.{n}"
        with tempfile.TemporaryDirectory(prefix="sfz3mix_hist_",dir=ROOT) as d:
            tmp=Path(d);arc=tmp/"ref.7z";extract=tmp/"members";extract.mkdir()
            req=urllib.request.Request(URL.format(version=version),headers={"User-Agent":"SFZ3Mix-Historical-Research/1.0"})
            with urllib.request.urlopen(req,timeout=75) as response, arc.open("wb") as fd:
                shutil.copyfileobj(response,fd,1024*1024)
            tested=subprocess.run([str(SEVENZIP),"t",str(arc)],capture_output=True,text=True,timeout=120)
            if tested.returncode:raise RuntimeError(f"{version} 7z test failed: {tested.stderr[-500:]}")
            done=subprocess.run([str(SEVENZIP),"x","-y",f"-o{extract}",str(arc)],capture_output=True,text=True,timeout=150)
            if done.returncode:raise RuntimeError(f"{version} extraction failed: {done.stderr[-500:]}")
            members=[]
            for p in sorted(extract.rglob("*")):
                if not p.is_file():continue
                if p.is_symlink():raise RuntimeError("symlink prohibited")
                data=p.read_bytes()
                members.append({"name":str(p.relative_to(extract)).replace("\\","/"),"bytes":len(data),"sha256":sha(data),"crc32":f"{zlib.crc32(data)&0xffffffff:08x}","role":category(p)})
            cpus=[p for p in members if p["role"]=="cpu"]
            if len(cpus)!=1:raise RuntimeError(f"{version}: exactly one CPU program required, got {len(cpus)}; members={members}")
            cpupath=extract/Path(cpus[0]["name"])
            current=cpupath.read_bytes()
            result["versions"].append({"version":version,"source":URL.format(version=version),"archive_size":arc.stat().st_size,"archive_sha256":sha(arc.read_bytes()),"members":members})
            if previous is not None:
                report=boundaries(previous[1],current);report.update({"from":previous[0],"to":version,"cpu_sha_from":sha(previous[1]),"cpu_sha_to":sha(current)})
                result["adjacent_pairs"].append(report)
            previous=(version,current)
            print(f"VERIFIED {version}: {len(members)} members; CPU {len(current)} bytes sha256={sha(current)[:18]}",flush=True)
    print("RESULT_JSON_BEGIN");print(json.dumps(result,separators=(",",":")));print("RESULT_JSON_END")
if __name__=="__main__":main()
