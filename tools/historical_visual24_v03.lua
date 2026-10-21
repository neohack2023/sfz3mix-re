local out=assert(io.open("probe.jsonl","w"))
local cpu=manager.machine.devices[":maincpu"];local mem=cpu.spaces.program
local f=0;local count=0;local guard=false;local taps={};local inputs={}
local function emit(s) if count<1000 then out:write(s.."\n");count=count+1 end end
local function state(b)
 return string.format('{"base":%d,"active":%d,"state":%d,"mode":%d,"x":%d,"y":%d,"anim":%d,"selector":%d}',b,mem:read_u8(b),mem:read_u16(b+4),mem:read_u8(b+6),mem:read_u16(b+16),mem:read_u16(b+20),mem:read_u32(b+28),mem:read_u32(b+200))
end
local function snap(kind,extra)
 guard=true;emit('{"type":"'..kind..'","frame":'..f..',"p1":'..state(0xff8400)..',"p2":'..state(0xff8800)..(extra or "")..'}');guard=false
end
for _,port in pairs(manager.machine.ioport.ports)do for name,field in pairs(port.fields)do inputs[name]=field end end
local function press(name,on)
 local p=assert(inputs[name],"Missing input "..name);if on then p:set_value(1)else p:clear_value()end
 snap("INPUT",',"name":"'..name..'","on":'..tostring(on))
end
local events={[420]={"Coin 1",true},[428]={"Coin 1",false},[465]={"1 Player Start",true},[475]={"1 Player Start",false},[545]={"P1 Button 1",true},[555]={"P1 Button 1",false},[660]={"P1 Button 1",true},[670]={"P1 Button 1",false},[780]={"P1 Button 1",true},[790]={"P1 Button 1",false},[900]={"P1 Button 1",true},[910]={"P1 Button 1",false},[2960]={"P1 Down",true},[2980]={"P1 Down",false},[3020]={"P1 Button 1",true},[3022]={"P1 Button 1",false},[3080]={"P1 Up",true},[3082]={"P1 Up",false}}
local edges={}
for _,t in ipairs({3000,3120,3124,3160,3200,3280})do edges[t]=true;edges[t+1]=false end
local unique={}
emu.register_frame_done(function()
 f=f+1
 if events[f]then press(events[f][1],events[f][2])end
 if edges[f]~=nil then press("P1 Button 1",edges[f]);press("P1 Button 4",edges[f])end
 if f==500 or f==1000 or f==2900 then
  for _,s in pairs(manager.machine.screens)do s:snapshot("frame_"..f..".png");break end
 end
 if f==2900 then
  for _,b in ipairs({0xff8404,0xff8804})do
   taps[#taps+1]=mem:install_write_tap(b,b+3,"state"..b,function(a,d,m)
    if guard then return end
    local pc=cpu.state.CURPC.value;local k=pc..":"..a..":"..d
    if not unique[k] and count<800 then
     unique[k]=true;snap("WRITE",string.format(',"pc":%d,"ir":%d,"romword":%d,"address":%d,"data":%d,"mask":%d',pc,cpu.state.IR.value,mem:read_u16(pc),a,d,m))
    end
   end)
  end
 end
 if f>=2900 and f%2==0 then snap("STATE")end
 if f>=3360 then
  for _,t in ipairs(taps)do t:remove()end
  snap("COMPLETE");out:close();print("V03_COMPLETE "..f.." "..count);manager.machine:exit()
 end
end,"frame")
manager.machine.debugger.execution_state="run"
