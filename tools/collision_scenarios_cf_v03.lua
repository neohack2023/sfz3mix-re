-- Input-triggered collision scenarios; no debugger exports or memory writes.
local root="D:/AIOS_SFZ3MIX_V032/"
local filename=root.."evidence/collision_scenarios_cf_v03.jsonl"
local exists=io.open(filename,"r");if exists then exists:close();error("Preserve prior scenario evidence")end
for _,suffix in ipairs({"_far.txt","_near.txt","_console.txt"})do local x=io.open(root.."evidence/consumer_cf_v03"..suffix,"r");if x then x:close();error("Preserve control evidence")end end
local out=assert(io.open(filename,"w"));local cpu=manager.machine.devices[":maincpu"];local mem=cpu.spaces["program"]
local dbg=manager.machine.debugger;dbg.visible_cpu=cpu
local f,n,bytes=0,0,0;local guard=false;local taps={};local phase="BOOT";local age=0;local seen={}
local function json(x)
 if type(x)=="table"then local a={};for k,v in pairs(x)do a[#a+1]='"'..k..'":'..json(v)end;return "{"..table.concat(a,",").."}"end
 if type(x)=="string"then return '"'..x..'"'end
 return tostring(x)
end
local function emit(x)
 if n>=600 then return end;local s=json(x).."\n";if bytes+#s>900000 then return end
 out:write(s);n=n+1;bytes=bytes+#s
end
local function reg(k)return cpu.state[k].value end
local function player(b)
 return {base=b,active=mem:read_u8(b),state4=mem:read_u16(b+4),x=mem:read_u16(b+0x10),y=mem:read_u16(b+0x14),animation=mem:read_u32(b+0x1c),selectors=mem:read_u32(b+0xc8),pointer9c=mem:read_u32(b+0x9c),edge=mem:read_u16(b+0x21c),flip=mem:read_u8(b+0xb),orientation=mem:read_u8(b+0x2c9)}
end
local function observation(t)
 guard=true;t.frame=f;t.phase=phase;t.age=age;t.p1=player(0xff8400);t.p2=player(0xff8800);emit(t);guard=false
end
local function access(kind,a,d,m)
 if guard or phase=="BOOT"or phase=="DONE"then return end
 local pc=reg("CURPC");local key=phase..kind..pc..a;seen[key]=(seen[key]or 0)+1
 if kind=="WRITE"and seen[key]>4 then return end
 if kind=="READ"and seen[key]>12 then return end
 observation({type="CPU",kind=kind,pc=pc,address=a,data=d,mask=m,ir=reg("IR"),a0=reg("A0"),a1=reg("A1"),a4=reg("A4"),a6=reg("A6"),d0=reg("D0"),d1=reg("D1"),d2=reg("D2"),sr=reg("SR")})
end
local ports=manager.machine.ioport.ports
local coin=ports[":IN2"].fields["Coin 1"];local start=ports[":IN2"].fields["1 Player Start"]
local button=assert(ports[":IN0"].fields["P1 Button 1"]);local right=assert(ports[":IN1"].fields["P1 Right"] or ports[":IN0"].fields["P1 Right"]);local left=assert(ports[":IN1"].fields["P1 Left"] or ports[":IN0"].fields["P1 Left"])
local actions={[420]={coin,true},[428]={coin,false},[465]={start,true},[475]={start,false},[545]={button,true},[555]={button,false},[660]={button,true},[670]={button,false},[780]={button,true},[790]={button,false},[900]={button,true},[910]={button,false}}
local function clear()right:clear_value();left:clear_value();button:clear_value()end
local function setphase(p)
 clear();phase=p;age=0;observation({type="PHASE"})
end
local function finish()
 clear();for _,t in ipairs(taps)do t:remove()end
 dbg:command("trace off,0")
 local log=assert(io.open(root.."evidence/consumer_cf_v03_console.txt","w"));for i=1,#dbg.consolelog do log:write(tostring(dbg.consolelog[i]),"\\n")end;log:close()
 observation({type="COMPLETE",event_count=n,bytes_written=bytes});out:close();print("SCENARIOS_COMPLETE events="..n.." bytes="..bytes);manager.machine:exit()
end
emu.register_frame_done(function()
 f=f+1;local a=actions[f];if a then if a[2]then a[1]:set_value(1)else a[1]:clear_value()end end
 if f==2939 then
  dbg:command("do temp0=0")
  cpu.debug:bpset(0x37a56,"temp0==0",'printf "FAR_ENTRY pc=%X a6=%X",curpc,a6; do temp0=1; trace '..root..'evidence/consumer_cf_v03_far.txt,0,noloop; g')
  cpu.debug:bpset(0x37a56,"temp0==2 && w@(a6+0x21c)<0x30",'printf "NEAR_ENTRY pc=%X a6=%X",curpc,a6; do temp0=3; trace '..root..'evidence/consumer_cf_v03_near.txt,0,noloop; g')
  for _,pc in ipairs({0x37a7c,0x37a80})do
   cpu.debug:bpset(pc,"temp0==1 || temp0==3",'trace off,0; printf "PREDICATE_RETURN pc=%X d0=%X",curpc,d0; do temp0=temp0+1; g')
  end
  for _,base in ipairs({0xff861c,0xff8a1c})do
   taps[#taps+1]=mem:install_read_tap(base,base+1,"scenario_read_"..base,function(a,d,m)access("READ",a,d,m)end)
   taps[#taps+1]=mem:install_write_tap(base,base+1,"scenario_write_"..base,function(a,d,m)access("WRITE",a,d,m)end)
  end
  setphase("BASELINE")
 end
 if phase~="BOOT"then
  age=age+1
  if age%4==0 then observation({type="STATE"})end
  guard=true;local p1=player(0xff8400);local p2=player(0xff8800);guard=false
  if phase=="BASELINE"and age>=8 then setphase("APPROACH")
  elseif phase=="APPROACH"then
   if p1.x<p2.x then right:set_value(1)else left:set_value(1)end
   if math.min(p1.edge,p2.edge)<=48 or age>=150 then setphase("ATTACK");button:set_value(1)end
  elseif phase=="ATTACK"then
   if age==4 then button:clear_value()end
   if age==12 then button:set_value(1)end
   if age==16 then button:clear_value()end
   if age>=28 then setphase("RETREAT")end
  elseif phase=="RETREAT"then
   if p1.x<p2.x then left:set_value(1)else right:set_value(1)end
   if age>=48 then setphase("RELEASE")end
  elseif phase=="RELEASE"and age>=8 then finish()end
 end
 if f>=3190 then finish()end
end,"frame")
manager.machine.debugger.execution_state="run"
