-- V02 engine recovery: bounded gameplay observations; nil-return taps.
local root="D:/AIOS_SFZ3MIX_V032/"
local stem="collision_engine_v02"
for _,s in ipairs({".tsv","_trace.txt","_console.txt","_launch.json"}) do local x=io.open(root.."evidence/"..stem..s,"r");if x then x:close();error("Preserve existing "..s) end end
local out=assert(io.open(root.."evidence/"..stem..".tsv","w"))
local cpu=manager.machine.devices[":maincpu"];local mem=cpu.spaces["program"];local dbg=manager.machine.debugger
dbg.visible_cpu=cpu
local f,n=0,0;local taps={}
local function reg(k)return cpu.state[k].value end
out:write("frame\tkind\tpc\taddress\tdata\tmask\ta0\ta1\ta4\ta5\ta6\td0\td1\tsp\n")
local function access(kind,a,d,m)
 if f<2939 or f>=2947 or n>=512 then return end
 local pc=reg("CURPC")
 if not ((a==0xff861c or a==0xff8a1c) or (pc>=0x29a10 and pc<0x29ab6)) then return end
 n=n+1
 out:write(string.format("%d\t%s\t%06X\t%06X\t%04X\t%04X\t%08X\t%08X\t%08X\t%08X\t%08X\t%08X\t%08X\t%08X\n",f,kind,pc,a,d,m,reg("A0"),reg("A1"),reg("A4"),reg("A5"),reg("A6"),reg("D0"),reg("D1"),reg("SP")))
end
local p=manager.machine.ioport.ports
local coin=p[":IN2"].fields["Coin 1"];local start=p[":IN2"].fields["1 Player Start"];local btn=p[":IN0"].fields["P1 Button 1"]
local actions={[420]={coin,true},[428]={coin,false},[465]={start,true},[475]={start,false},[545]={btn,true},[555]={btn,false},[660]={btn,true},[670]={btn,false},[780]={btn,true},[790]={btn,false},[900]={btn,true},[910]={btn,false}}
emu.register_frame_done(function()
 f=f+1;local a=actions[f];if a then if a[2] then a[1]:set_value(1) else a[1]:clear_value() end end
 if f==2939 then
  dbg:command("do temp0=0")
  cpu.debug:bpset(0x2c07e,"temp0==0",'printf "WRAP_CALL pc=%X sp=%X",curpc,sp; do temp0=1; trace '..root..'evidence/'..stem..'_trace.txt,0,noloop; g')
  for _,pc in ipairs({0x2c17e,0x2c19a,0x2c186,0x2c18e,0x2c196,0x2c1e0}) do
   cpu.debug:bpset(pc,"temp0==1",'printf "PATH pc=%X a6=%X sp=%X",curpc,a6,sp; g')
  end
  cpu.debug:bpset(0x2c082,"temp0==1",'trace off,0; printf "WRAP_RETURN pc=%X sp=%X",curpc,sp; do temp0=2; g')
  for _,r in ipairs({{0xff8400,0xff8bff},{0xd6580,0xd65ff},{0xf2aca,0xf2b49}}) do
   taps[#taps+1]=mem:install_read_tap(r[1],r[2],"engine_read_"..r[1],function(a,d,m)access("READ",a,d,m)end)
   taps[#taps+1]=mem:install_write_tap(r[1],r[2],"engine_write_"..r[1],function(a,d,m)access("WRITE",a,d,m)end)
  end
 end
 if f==2947 then
  for _,t in ipairs(taps)do t:remove()end;dbg:command("trace off,0")
  out:write("# COMPLETE frames=2939..2946 samples=",n,"\n");out:close()
  for _,r in ipairs({{0x2c070,0x20},{0x2c17e,0x64},{0x29a10,0xa6},{0x27eda,0x22},{0x2f666,0x24}})do
   dbg:command(string.format("dasm %sevidence/%s_%06x.txt,0x%x,0x%x,1,:maincpu",root,stem,r[1],r[1],r[2]))
  end
  local log=assert(io.open(root.."evidence/"..stem.."_console.txt","w"));for i=1,#dbg.consolelog do log:write(tostring(dbg.consolelog[i]),"\n")end;log:close()
  print("ENGINE_V02_COMPLETE samples="..n);manager.machine:exit()
 end
end,"frame")
dbg.execution_state="run"
