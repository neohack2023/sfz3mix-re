"""Bounded historical boot/input probe; no gameplay writes or ROM retention."""
import hashlib,json,shutil,subprocess,tempfile,urllib.request,zlib,xml.etree.ElementTree as ET
from pathlib import Path
R=Path(r"D:\AIOS_SFZ3MIX_V032")
EXE=R/"runtime_hbmame/hbmame.exe"
OUT=Path(r"C:\AIOS\_TEMP\SFZ3MIX_V03_VISUAL24")
PINS={
24:("9082929fd7075502a35e5f977f3ccb6cc3dbafc35fd9e693e7508fe61ae7b9d7","2fba55f17fa2801cb05ce07a9ba66ed515cb1163dde69592728214a6a77b2f8f"),
25:("cdde7583917bfb13d0c985184c2ee2fa1b99a266610e544fc1b8f545cbb6a4c6","5ff23470ddec1dadc9935c370adfef4408beb92f0cccac94181d1dfe81e948c4"),
26:("7bc49cc6c88460efe67a38f8c405081af4eee53ac71230bc2f9732128da4290c","7724bf1ea71d9a85f88054307c1a195637736d372e1a92c4831dc43d25b9452e")}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 assert sha(R/"tools/sz3mx.03")=="b5f7a1598e4f91a5113c506505b482b2cd1a19e366fe31471740e45dbd204691"
 assert shutil.disk_usage("C:/").free>2*1024**3
 OUT.mkdir(parents=True,exist_ok=True)
 assert not (OUT/"receipt.json").exists(),"preserve previous run"
 reports=[]
 for v,(archive_hash,cpu_hash) in PINS.items():
  result={"version":f"0.{v}","driver":f"sfz3mix{v}"}
  try:
   with tempfile.TemporaryDirectory(prefix=f"sfz3mix_v03_{v}_",dir=OUT.parent) as td:
    w=Path(td);arc=w/"source.7z"
    with urllib.request.urlopen(f"https://sfz3mix.github.io/download/0.{v}/sfz3mix.7z",timeout=60) as inp,arc.open("wb") as out:shutil.copyfileobj(inp,out)
    assert sha(arc)==archive_hash
    subprocess.run([r"C:\Program Files\7-Zip\7z.exe","t",str(arc)],capture_output=True,timeout=60,check=True)
    members=w/"members"
    subprocess.run([r"C:\Program Files\7-Zip\7z.exe","x","-y",f"-o{members}",str(arc)],capture_output=True,timeout=60,check=True)
    files=[p for p in members.rglob("*") if p.is_file()]
    cpu=next(p for p in files if p.name.lower() in ("sfz3mix.p1","sz3mx.03"))
    assert sha(cpu)==cpu_hash
    result.update(archive_sha256=archive_hash,cpu_sha256=cpu_hash,archive_integrity="PASS")
    xml=subprocess.run([str(EXE),"-listxml",f"sfz3mix{v}"],capture_output=True,text=True,timeout=30,check=True)
    machine=next(m for m in ET.fromstring(xml.stdout).findall("machine") if m.get("name")==f"sfz3mix{v}")
    romdir=w/f"sfz3mix{v}";romdir.mkdir()
    mapped=[]
    for rom in machine.findall("rom"):
     crc=int(rom.get("crc"),16);size=int(rom.get("size"))
     p=next((p for p in files if p.exists() and p.stat().st_size==size and zlib.crc32(p.read_bytes())&0xffffffff==crc),None)
     if p is None:raise RuntimeError("Missing driver member "+rom.get("name"))
     shutil.move(str(p),romdir/rom.get("name"));mapped.append({"name":rom.get("name"),"crc":rom.get("crc"),"bytes":size})
    bios=next((p for p in files if p.exists() and p.name=="dl-1425.bin"),None)
    if bios: shutil.copyfile(bios,romdir/"dl-1425.bin")
    else:
     from zipfile import ZipFile
     with ZipFile(R/"runtime_hbmame/roms/sfz3mix.zip") as z:
      data=z.read("dl-1425.bin");assert zlib.crc32(data)&0xffffffff==0xd6cf5ef5
      (romdir/"dl-1425.bin").write_bytes(data)
    shutil.copyfile(R/"tools/historical_visual24_v03.lua",w/"probe.lua")
    args=[str(EXE),f"sfz3mix{v}","-rompath",str(w),"-skip_gameinfo","-nothrottle","-video","none","-sound","none","-debug","-debugger","none","-autoboot_delay","0","-autoboot_script",str(w/"probe.lua"),"-seconds_to_run","65"]
    run=subprocess.run(args,cwd=w,capture_output=True,text=True,timeout=90)
    result.update(exit_code=run.returncode,stdout=run.stdout[-2000:],stderr=run.stderr[-3000:],members=mapped)
    for image in w.glob("frame_*.png"):shutil.copyfile(image,OUT/image.name)
    log=w/"probe.jsonl"
    if log.exists():
     dest=OUT/f"v{v}_probe.jsonl";shutil.copyfile(log,dest);result["log_sha256"]=sha(dest)
     rows=[json.loads(x) for x in dest.read_text().splitlines()]
     result["complete"]=any(x["type"]=="COMPLETE" for x in rows)
     result["rows"]=len(rows)
     writes=[x for x in rows if x["type"]=="WRITE"]
     result["state_write_pcs"]=sorted(set(x["pc"] for x in writes))
     result["opcode_word_matches"]=sum(x["ir"]==x["romword"] for x in writes)
     result["opcode_samples"]=len(writes)
     result["observed_p1_states"]=sorted(set((x["p1"]["state"],x["p1"]["mode"]) for x in rows if x["frame"]>=2900))
     result["input_state_windows"]=[x for x in rows if x["type"]=="STATE" and x["frame"] in (2998,3000,3002,3004,3010,3018,3080,3100,3120,3122,3124,3130,3140,3160,3200,3280)]
  except Exception as e:result["error"]=str(e)
  reports.append(result);(OUT/"receipt.json").write_text(json.dumps(reports,indent=2))
  print(json.dumps(result),flush=True)
 assert sha(R/"tools/sz3mx.03")=="b5f7a1598e4f91a5113c506505b482b2cd1a19e366fe31471740e45dbd204691"
if __name__=="__main__":
 PINS={24:PINS[24]}
 main()
