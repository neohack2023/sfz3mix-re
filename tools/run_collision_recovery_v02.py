import subprocess,json,time
from pathlib import Path
root=Path(r"D:\AIOS_SFZ3MIX_V032")
args=[str(root/"runtime_hbmame/hbmame.exe"),"sfz3mix","-rompath",str(root/"runtime_hbmame/roms"),"-skip_gameinfo","-nothrottle","-video","none","-sound","none","-debug","-debugger","none","-autoboot_delay","0","-autoboot_script",str(root/"tools/collision_recovery_v02.lua"),"-seconds_to_run","60"]
start=time.monotonic()
r=subprocess.run(args,cwd=root/"runtime_hbmame",capture_output=True,text=True,timeout=80)
receipt={"args":args,"exit_code":r.returncode,"elapsed":round(time.monotonic()-start,2),"stdout_tail":r.stdout[-6000:],"stderr_tail":r.stderr[-2000:]}
(root/"evidence/collision_recovery_launch_v02.json").write_text(json.dumps(receipt,indent=2))
print(json.dumps(receipt))
raise SystemExit(r.returncode)
