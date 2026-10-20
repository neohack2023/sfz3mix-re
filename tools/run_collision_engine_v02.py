import subprocess,json,time
from pathlib import Path
root=Path(r"D:\AIOS_SFZ3MIX_V032")
p=root/"evidence/collision_engine_v02_launch.json"
assert not p.exists()
args=[str(root/"runtime_hbmame/hbmame.exe"),"sfz3mix","-rompath",str(root/"runtime_hbmame/roms"),"-skip_gameinfo","-nothrottle","-video","none","-sound","none","-debug","-debugger","none","-autoboot_delay","0","-autoboot_script",str(root/"tools/collision_engine_v02.lua"),"-seconds_to_run","60"]
t=time.monotonic();r=subprocess.run(args,cwd=root/"runtime_hbmame",capture_output=True,text=True,timeout=80)
v=dict(args=args,exit_code=r.returncode,elapsed=time.monotonic()-t,stdout_tail=r.stdout[-3000:],stderr_tail=r.stderr[-3000:]);p.write_text(json.dumps(v,indent=2));print(json.dumps(v));raise SystemExit(r.returncode)
