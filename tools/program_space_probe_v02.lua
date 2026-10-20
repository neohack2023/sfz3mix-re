-- Read-only wide-range sample of :maincpu program data-space.
-- Values above mapped ROM may be unmapped/banked; never infer instruction fetch parity.
local out=assert(io.open("D:/AIOS_SFZ3MIX_V032/evidence/program_space_probe_v02.tsv","w"))
local space=assert(manager.machine.devices[":maincpu"].spaces["program"])
local addr={0x07FFF0,0x080000,0x0FFFF0,0x100000,0x17FFF0,0x180000,
0x1FFFF0,0x200000,0x27FFF0,0x280000,0x2FFFF0,0x300000,
0x37FFF0,0x380000,0x3FFFF0,0x400000,0x47FFF0,0x480000,
0x4FFFF0,0x500000,0x57FFF0,0x580000,0x5FFFC0}
local done=false
emu.register_frame_done(function()
 if done then return end
 done=true
 out:write("emulator_cpu_address\tprogram_space_read_u8_32bytes\n")
 for _,a in ipairs(addr) do
  local bytes={}
  local ok,err=pcall(function()
   for i=0,31 do bytes[#bytes+1]=string.format("%02x",space:read_u8(a+i)) end
  end)
  if ok then out:write(string.format("%06X\t%s\n",a,table.concat(bytes)))
  else out:write(string.format("%06X\tERROR:%s\n",a,tostring(err))) end
 end
 out:close();manager.machine:exit()
end,"frame")
