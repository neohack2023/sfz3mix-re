import subprocess,json,time
from pathlib import Path
R=Path(r"D:\AIOS_SFZ3MIX_V032");p=R/"evidence/collision_decisions_controlled_v04_launch.json";assert not p.exists()
args=[str(R/"runtime_hbmame/hbmame.exe"),"sfz3mix","-rompath",str(R/"runtime_hbmame/roms"),"-skip_gameinfo","-nothrottle","-video","none","-sound","none","-debug","-debugger","none","-autoboot_delay","0","-autoboot_script",str(R/"tools/collision_decisions_controlled_v04.lua"),"-seconds_to_run","65"]
t=time.monotonic();r=subprocess.run(args,cwd=R/"runtime_hbmame",capture_output=True,text=True,timeout=80)
v=dict(exit_code=r.returncode,elapsed=time.monotonic()-t,args=args,stdout=r.stdout[-3000:],stderr=r.stderr[-3000:]);p.write_text(json.dumps(v,indent=2));print(json.dumps(v));raise SystemExit(r.returncode)
