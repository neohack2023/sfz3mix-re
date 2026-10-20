-- One invocation instruction trace plus one frame of bounded operand accesses.
local root="D:/AIOS_SFZ3MIX_V032/"
local names={"collision_recovery_v02.tsv","collision_recovery_trace_v02.txt","collision_recovery_disasm_v02.txt","collision_recovery_console_v02.txt"}
for _,name in ipairs(names) do local x=io.open(root.."evidence/"..name,"r");if x then x:close();error("Preserve existing evidence before rerun: "..name) end end
local out=assert(io.open(root.."evidence/"..names[1],"w"))
local cpu=assert(manager.machine.devices[":maincpu"])
local mem=assert(cpu.spaces["program"])
local dbg=assert(manager.machine.debugger)
dbg.visible_cpu=cpu
local f,n=0,0
local taps={}
local stack=assert(cpu.state["SP"] or cpu.state["A7"],"No stack pointer state available")
local function reg(k) if k=="A7" then return stack.value end;return assert(cpu.state[k],"Missing register "..k).value end
out:write("frame\tkind\tpc\taddress\tdata\tmask\ta0\ta4\ta5\ta6\td0\td1\ta7\n")
local function access(kind,a,d,m)
 local pc=reg("CURPC")
 if f~=2939 or pc<0x2c19a or pc>0x2c1e0 or n>=128 then return end
 n=n+1
 out:write(string.format("%d\t%s\t%06X\t%06X\t%04X\t%04X\t%08X\t%08X\t%08X\t%08X\t%08X\t%08X\t%08X\n",f,kind,pc,a,d,m,reg("A0"),reg("A4"),reg("A5"),reg("A6"),reg("D0"),reg("D1"),reg("A7")))
end
local ports=manager.machine.ioport.ports
local coin=assert(ports[":IN2"].fields["Coin 1"])
local start=assert(ports[":IN2"].fields["1 Player Start"])
local btn=assert(ports[":IN0"].fields["P1 Button 1"])
local actions={[420]={coin,true},[428]={coin,false},[465]={start,true},[475]={start,false},[545]={btn,true},[555]={btn,false},[660]={btn,true},[670]={btn,false},[780]={btn,true},[790]={btn,false},[900]={btn,true},[910]={btn,false}}
emu.register_frame_done(function()
 f=f+1
 local a=actions[f];if a then if a[2] then a[1]:set_value(1) else a[1]:clear_value() end end
 if f==2939 then
  dbg:command("do temp0=0")
  cpu.debug:bpset(0x2c19a,"temp0==0",'do temp0=1; printf "REC_ENTRY pc=%X a5=%X a6=%X sp=%X ret=%X",curpc,a5,a6,sp,d@sp; trace '..root..'evidence/'..names[2]..',0,noloop; g')
  cpu.debug:bpset(0x2c1ac,"temp0==1",'printf "REC_POINTER pc=%X a4=%X a6=%X selector=%X",curpc,a4,a6,d0; g')
  cpu.debug:bpset(0x2c1b6,"temp0==1",'printf "REC_TABLE pc=%X a0=%X a4=%X",curpc,a0,a4; g')
  cpu.debug:bpset(0x2c1e0,"temp0==1",'trace off,0; printf "REC_RTS pc=%X sp=%X ret=%X",curpc,sp,d@sp; do temp0=2; g')
  cpu.debug:bpset(0x2c186,"temp0==2",'printf "REC_RETURN pc=%X sp=%X",curpc,sp; do temp0=3; g')
  for _,r in ipairs({{0xff8400,0xff8bff},{0xd6580,0xd65ff},{0xf2aca,0xf2b49}}) do
   taps[#taps+1]=mem:install_read_tap(r[1],r[2],"recovery_read_"..r[1],function(a,d,m) access("READ",a,d,m) end)
  end
  taps[#taps+1]=mem:install_write_tap(0xff8400,0xff8bff,"recovery_write",function(a,d,m) access("WRITE",a,d,m) end)
 end
 if f==2940 then
  for _,t in ipairs(taps) do t:remove() end
  dbg:command("trace off,0")
  out:write("# COMPLETE frame=",f," samples=",n,"\n");out:close()
  dbg:command("dasm "..root.."evidence/"..names[3]..",2c17e,64,1,:maincpu")
  local log=assert(io.open(root.."evidence/"..names[4],"w"))
  for i=1,#dbg.consolelog do log:write(tostring(dbg.consolelog[i]),"\n") end
  log:close()
  print("COLLISION_RECOVERY_COMPLETE samples="..n)
  manager.machine:exit()
 end
end,"frame")
dbg.execution_state="run"
