-- Bounded read-only CPU memory taps. Returning nil preserves all bus data.
local root="D:/AIOS_SFZ3MIX_V032/"
local out=assert(io.open(root.."evidence/collision_access_v01.tsv","w"))
local cpu=assert(manager.machine.devices[":maincpu"])
local mem=assert(cpu.spaces["program"])
local dbg=assert(manager.machine.debugger)
assert(cpu.state["CURPC"],"CURPC unavailable: do not substitute post-instruction PC")
dbg.visible_cpu=cpu
local f,n,busy=0,0,false
local taps,pcs,seen={},{},{}
local ports=manager.machine.ioport.ports
local coin=assert(ports[":IN2"].fields["Coin 1"])
local start=assert(ports[":IN2"].fields["1 Player Start"])
local btn=assert(ports[":IN0"].fields["P1 Button 1"])
local actions={[420]={coin,true},[428]={coin,false},[465]={start,true},[475]={start,false},[545]={btn,true},[555]={btn,false},[660]={btn,true},[670]={btn,false},[780]={btn,true},[790]={btn,false},[900]={btn,true},[910]={btn,false},[2960]={btn,true},[2964]={btn,false},[3000]={btn,true},[3004]={btn,false}}
out:write("frame\taccess\taddress\tbus_data\tbus_mask\tcurpc\tpc_register\tir\ta0\ta1\ta6\tplayer\tstatus\tpointer90\tpointer9c\tselectors\tphase\n")
local function reg(k) return cpu.state[k] and cpu.state[k].value or 0 end
local ranges={{0xff8490,0xff8493,1},{0xff849c,0xff849f,1},{0xff8890,0xff8893,2},{0xff889c,0xff889f,2},{0xff84c8,0xff84cb,1},{0xff88c8,0xff88cb,2}}
local function observe(kind,player,addr,data,mask)
 if busy or f<2940 or f>3060 or n>=512 then return end
 busy=true
 local pc=reg("CURPC")
 local key=string.format("%s:%x:%x:%x",kind,addr,pc,data)
 if not seen[key] then
  seen[key]=true;n=n+1;pcs[pc]=true
  local base=player==1 and 0xff8400 or 0xff8800
  local sel=string.format("%02X%02X%02X%02X",mem:read_u8(base+0xc8),mem:read_u8(base+0xc9),mem:read_u8(base+0xca),mem:read_u8(base+0xcb))
  out:write(string.format("%d\t%s\t%06X\t%04X\t%04X\t%06X\t%06X\t%04X\t%08X\t%08X\t%08X\t%d\t%04X\t%08X\t%08X\t%s\tDETERMINISTIC_ATTACK_WINDOW\n",f,kind,addr,data,mask,pc,reg("PC"),reg("IR"),reg("A0"),reg("A1"),reg("A6"),player,mem:read_u16(base+4),mem:read_u32(base+0x90),mem:read_u32(base+0x9c),sel))
 end
 busy=false
end
for _,range in ipairs(ranges) do
 local player=range[3]
 taps[#taps+1]=mem:install_read_tap(range[1],range[2],"sfz_read_"..range[1],function(a,d,m) observe("READ",player,a,d,m) end)
 taps[#taps+1]=mem:install_write_tap(range[1],range[2],"sfz_write_"..range[1],function(a,d,m) observe("WRITE",player,a,d,m) end)
end
emu.register_frame_done(function()
 f=f+1
 local a=actions[f]
 if a then if a[2] then a[1]:set_value(1) else a[1]:clear_value() end end
 if f==3062 then
  for _,tap in ipairs(taps) do tap:remove() end
  out:flush()
 end
 if f==3100 then
  local count=0
  for pc,_ in pairs(pcs) do
   if count<32 then
    dbg:command(string.format("dasm "..root.."evidence/collision_pc_%06X.txt,%x,10,1,:maincpu",pc,pc))
    count=count+1
   end
  end
  out:write("# COMPLETE frames=",f," samples=",n," disassembly_sites=",count,"\n");out:close()
  print("SFZ_COLLISION_TRACE_COMPLETE samples="..n.." sites="..count)
  manager.machine:exit()
 end
end,"frame")
dbg.execution_state="run"
