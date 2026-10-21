-- Input-triggered collision scenarios; no debugger exports or memory writes.
local root="D:/AIOS_SFZ3MIX_V032/"
local filename=root.."evidence/collision_decisions_crouch_v04.jsonl"
local exists=io.open(filename,"r");if exists then exists:close();error("Preserve prior scenario evidence")end
local out=assert(io.open(filename,"w"));local cpu=manager.machine.devices[":maincpu"];local mem=cpu.spaces["program"]
local f,n,bytes=0,0,0;local guard=false;local taps={};local phase="BOOT";local age=0;local seen={}
local function json(x)
 if type(x)=="table"then local a={};for k,v in pairs(x)do a[#a+1]='"'..k..'":'..json(v)end;return "{"..table.concat(a,",").."}"end
 if type(x)=="string"then return '"'..x..'"'end
 return tostring(x)
end
local function emit(x)
 if n>=450 and x.type~="COMPLETE"then return end;local s=json(x).."\n";if bytes+#s>900000 then return end
 out:write(s);n=n+1;bytes=bytes+#s
end
local function reg(k)return cpu.state[k].value end
local function player(b)
 local ap=mem:read_u32(b+0x1c)
 return {base=b,active=mem:read_u8(b),state4=mem:read_u16(b+4),x=mem:read_u16(b+0x10),y=mem:read_u16(b+0x14),animation=ap,animation8=(ap>0 and ap<0x5ffff8)and mem:read_u32(ap+8)or 0,selectors=mem:read_u32(b+0xc8),pointer9c=mem:read_u32(b+0x9c),edge=mem:read_u16(b+0x21c),flip=mem:read_u8(b+0xb),orientation=mem:read_u8(b+0x2c9),state6=mem:read_u8(b+6),flag31=mem:read_u8(b+0x31),a9=mem:read_u8(b+0xa9),mask240=mem:read_u16(b+0x240),decision=mem:read_u8(b+0x21e),command206=mem:read_u16(b+0x206)}
end
local function observation(t)
 guard=true;t.frame=f;t.phase=phase;t.age=age;t.p1=player(0xff8400);t.p2=player(0xff8800);emit(t);guard=false
end
local success_frame=nil
local function access(kind,a,d,m)
 if guard or phase=="BOOT"or phase=="DONE"then return end
 local pc=reg("CURPC")
 if kind=="WRITE"and pc==0x37a3e and d==0 then success_frame=f end
 if a~=0xff861c and a~=0xff8a1c and a~=0xff861e and a~=0xff8a1e and not success_frame then return end
 local key=phase..kind..pc..a;seen[key]=(seen[key]or 0)+1
 if kind=="WRITE"and seen[key]>2 then return end
 if kind=="READ"and seen[key]>4 then return end
 observation({type="CPU",kind=kind,pc=pc,address=a,data=d,mask=m,ir=reg("IR"),d5=reg("D5"),d6=reg("D6"),a0=reg("A0"),a1=reg("A1"),a4=reg("A4"),a6=reg("A6"),d0=reg("D0"),d1=reg("D1"),d2=reg("D2"),sr=reg("SR")})
end
local ports=manager.machine.ioport.ports
local coin=ports[":IN2"].fields["Coin 1"];local start=ports[":IN2"].fields["1 Player Start"]
local button=assert(ports[":IN0"].fields["P1 Button 1"]);local right=assert(ports[":IN1"].fields["P1 Right"] or ports[":IN0"].fields["P1 Right"]);local left=assert(ports[":IN1"].fields["P1 Left"] or ports[":IN0"].fields["P1 Left"])
local down=assert(ports[":IN1"].fields["P1 Down"] or ports[":IN0"].fields["P1 Down"])
local mp=assert(ports[":IN0"].fields["P1 Button 2"]);local hp=assert(ports[":IN0"].fields["P1 Button 3"]);local buttons={button,mp,hp}
local dbg=manager.machine.debugger;dbg.visible_cpu=cpu
local attempt=1
local actions={[420]={coin,true},[428]={coin,false},[465]={start,true},[475]={start,false},[545]={button,true},[555]={button,false},[660]={button,true},[670]={button,false},[780]={button,true},[790]={button,false},[900]={button,true},[910]={button,false}}
local function clear()down:clear_value();right:clear_value();left:clear_value();button:clear_value();mp:clear_value();hp:clear_value()end
local function setphase(p)
 clear();phase=p;age=0;observation({type="PHASE"})
end
local shots=0
local function shot(tag)
 if shots>=3 then return end
 for _,screen in pairs(manager.machine.screens)do local e=screen:snapshot(root.."evidence/decision_crouch_v04_"..tag..".png");print("SNAPSHOT "..tag.." error="..tostring(e));break end
 shots=shots+1
end
local function finish()
 clear();for _,t in ipairs(taps)do t:remove()end
 dbg:command("trace off,0")
 local log=assert(io.open(root.."evidence/decision_crouch_v04_console.txt","w"));for i=1,#dbg.consolelog do log:write(tostring(dbg.consolelog[i]),"\n")end;log:close()
 observation({type="COMPLETE",event_count=n,bytes_written=bytes});out:close();print("SCENARIOS_COMPLETE events="..n.." bytes="..bytes);manager.machine:exit()
end
emu.register_frame_done(function()
 f=f+1;local a=actions[f];if a then if a[2]then a[1]:set_value(1)else a[1]:clear_value()end end
 if f==2939 then
  dbg:command("do temp0=0; do temp1=0; do temp2=0; do temp3=0; do temp6=0")
  cpu.debug:bpset(0x37a64,"temp6==0",'printf "VALID_NEAR pc=%X a6=%X",curpc,a6; trace '..root..'evidence/decision_crouch_v04_valid_near.txt,0,noloop; do temp6=1; g')
  cpu.debug:bpset(0x379b8,"temp6==1",'trace off,0; printf "VALID_NEAR_RETURN d0=%X d6=%X sr=%X",d0,d6,sr; do temp6=2; g')
  cpu.debug:bpset(0x379b8,"temp1<12 || (d0!=0 && temp1<48)",'printf "DEC_RETURN a6=%X d0=%X d6=%X sr=%X",a6,d0,d6,sr; do temp1=temp1+1; g')
  cpu.debug:bpset(0x2c58a,"temp3<16 || (d0!=0 && temp3<48)",'printf "OUTER_RETURN a6=%X d0=%X sr=%X",a6,d0,sr; do temp3=temp3+1; g')

  for _,base in ipairs({0xff861c,0xff8a1c,0xff861e,0xff8a1e})do
   taps[#taps+1]=mem:install_read_tap(base,base+1,"scenario_read_"..base,function(a,d,m)access("READ",a,d,m)end)
   taps[#taps+1]=mem:install_write_tap(base,base+1,"scenario_write_"..base,function(a,d,m)access("WRITE",a,d,m)end)
  end
  for _,range in ipairs({{0xff8404,0xff8407},{0xff8804,0xff8807},{0xff8606,0xff8607},{0xff8a06,0xff8a07}})do
   taps[#taps+1]=mem:install_write_tap(range[1],range[2],"outcome_"..range[1],function(a,d,m)access("WRITE",a,d,m)end)
  end
  setphase("BASELINE")
 end
 if phase~="BOOT"then
  age=age+1
  if age%8==0 then observation({type="STATE"})end
  guard=true;local p1=player(0xff8400);local p2=player(0xff8800);guard=false
  if phase=="BASELINE"and age>=4 then setphase("ARM_1")
  elseif phase:find("ARM")==1 then
   clear()
   if p2.edge>44 then if p1.x<p2.x then right:set_value(1)else left:set_value(1)end
   elseif p2.edge<40 then if p1.x<p2.x then left:set_value(1)else right:set_value(1)end end
   local eligible=p1.state4==0x200 and p1.flag31==0 and p1.state6~=10 and p2.state4==0x200 and p2.flag31==0 and (p2.state6==0 or p2.state6==2 or p2.state6==4)
   if p2.edge>=36 and p2.edge<48 and eligible then setphase("PUNCH_"..attempt);down:set_value(1)end
  elseif phase:find("PUNCH")==1 then
   if age==2 then button:set_value(1)end
   if age==3 then button:clear_value()end
   if age==5 and attempt<=2 then shot("punch_"..attempt)end
   if age>=24 then attempt=attempt+1;if attempt<=2 then setphase("ARM_"..attempt)else setphase("RELEASE")end end
  elseif phase=="RELEASE"and age>=8 then finish()end
  if success_frame and f>=success_frame+12 then shot("success");finish()end
 end
 if f>=3480 then shot("limit");finish()end
end,"frame")
manager.machine.debugger.execution_state="run"
