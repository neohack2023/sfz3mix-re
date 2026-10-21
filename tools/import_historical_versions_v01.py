#!/usr/bin/env python3
"""Import author-hosted historical SFZ3 Mix releases, never touch canonical v0.32.
Requires 7z or 7za installed for .7z releases. ZIP uses Python stdlib.
Fails closed on path traversal, space constraints, corrupt or missing releases.
"""
import argparse, hashlib, json, shutil, subprocess, urllib.request, zipfile
from pathlib import Path

SOURCES = {"0.13": "https://sfz3mix.github.io/download/0.13/sfz3mix13.zip"}
SOURCES.update({f"0.{n}":f"https://sfz3mix.github.io/download/0.{n}/sfz3mix.7z" for n in range(23,32)})
def digest(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""):h.update(block)
    return h.hexdigest()
def safe_name(value):
    p=Path(value.replace("\\","/"))
    return bool(value and not p.is_absolute() and ".." not in p.parts and not (len(p.parts[0])>1 and ":" in p.parts[0]))
def main():
    a=argparse.ArgumentParser()
    a.add_argument("--destination",type=Path,required=True)
    a.add_argument("--versions",nargs="+",choices=list(SOURCES),default=list(SOURCES))
    a.add_argument("--minimum-headroom-mib",type=int,default=512)
    x=a.parse_args()
    root=x.destination.resolve()
    root.mkdir(parents=True,exist_ok=True)
    arch=root/"archives"; arch.mkdir(exist_ok=True)
    records=root/"manifest";records.mkdir(exist_ok=True)
    tool=shutil.which("7z") or shutil.which("7za")
    for version in x.versions:
        url=SOURCES[version]; ext=".zip" if version=="0.13" else ".7z"
        file=arch/("sfz3mix_"+version.replace(".","_")+ext)
        folder=root/"extracted"/version
        record=records/(version.replace(".","_")+".json")
        if record.exists():
            print(version,"SKIP receipt exists, verify separately before adopting")
            continue
        if folder.exists():
            print(version,"SKIP existing extracted folder; no overwrite");continue
        if shutil.disk_usage(root).free < x.minimum_headroom_mib*1024*1024:
            print(version,"BLOCK low disk space");break
        if not file.exists():
            part=file.with_suffix(file.suffix+".partial")
            if part.exists():raise RuntimeError("partial download exists; manually inspect "+str(part))
            print(version,"downloading",url,flush=True)
            try:
                with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"SFZ3Mix-Research-Importer/1.0"}), timeout=60) as src,part.open("xb") as dest:
                    shutil.copyfileobj(src,dest,1024*1024)
                part.replace(file)
            except Exception:
                part.unlink(missing_ok=True); raise
        if file.stat().st_size==0: raise ValueError("empty archive "+str(file))
        filehash=digest(file)
        folder.parent.mkdir(parents=True,exist_ok=True)
        staged=folder.with_name(folder.name+".partial")
        if staged.exists():raise RuntimeError("partial extraction exists "+str(staged))
        staged.mkdir()
        try:
            if ext==".zip":
                with zipfile.ZipFile(file) as z:
                    bad=z.testzip()
                    if bad:raise RuntimeError("ZIP CRC fails: "+bad)
                    for m in z.infolist():
                        if not safe_name(m.filename):raise ValueError("unsafe member path "+m.filename)
                        if (m.external_attr>>16)&0o170000 == 0o120000:raise ValueError("symlink prohibited")
                    z.extractall(staged)
            else:
                if not tool:raise RuntimeError("7z not installed; archive retained")
                listing=subprocess.run([tool,"l","-slt",str(file)],capture_output=True,text=True,check=True)
                # Require conservative file path checks from 7z list.
                for line in listing.stdout.splitlines():
                    if line.startswith("Path = "):
                        member=line[7:]
                        if member==str(file):continue
                        if not safe_name(member):raise ValueError("unsafe 7z member "+member)
                    if line.startswith("Symbolic Link = "):raise ValueError("7z symlink blocked")
                subprocess.run([tool,"t",str(file)],check=True,stdout=subprocess.DEVNULL)
                subprocess.run([tool,"x","-y",f"-o{staged}",str(file)],check=True,stdout=subprocess.DEVNULL)
            items=[]
            for p in sorted(staged.rglob("*")):
                if p.is_symlink():raise ValueError("symlink in output")
                if p.is_file():
                    items.append({"path":p.relative_to(staged).as_posix(),"bytes":p.stat().st_size,"sha256":digest(p)})
            if not items:raise ValueError("archive contains no files")
            staged.replace(folder)
            report={"version":version,"source_url":url,"archive":str(file),"archive_bytes":file.stat().st_size,
                    "archive_sha256":filehash,"extracted":str(folder),"members":items,
                    "status":"DOWNLOADED_EXTRACTED_HASHED_NOT_GAMEPLAY_VERIFIED"}
            record.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
            print(version,"IMPORTED",len(items),"members",flush=True)
        except Exception:
            shutil.rmtree(staged,ignore_errors=True)
            raise
if __name__=="__main__":main()
