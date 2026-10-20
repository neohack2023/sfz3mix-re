-- Bounded HBMAME disassembly of Motorola 68000 reset/exception vector targets.
-- Candidate locations only; no full CFG/function bounds proven.
local dbg = assert(manager.machine.debugger)
dbg.visible_cpu = manager.machine.devices[":maincpu"]
local out = assert(io.open("D:/AIOS_SFZ3MIX_V032/evidence/vector_entry_disasm_v01_log.txt","w"))
local list = {
  {"reset_000976", "976", "120"},
  {"exception_0000c0", "c0", "80"},
  {"exception_0000d0", "d0", "80"},
  {"exception_0011de", "11de", "80"}
}
for _, r in ipairs(list) do
  local cmd="dasm D:/AIOS_SFZ3MIX_V032/evidence/vector_"..r[1]..".txt,"..r[2]..","..r[3]..",1,:maincpu"
  local ok,err=pcall(function() dbg:command(cmd) end)
  out:write("TARGET ",r[1]," STATUS ",tostring(ok)," ",tostring(err),"\n")
end
for i=1,#dbg.consolelog do out:write("CONSOLE ",tostring(dbg.consolelog[i]),"\n") end
out:close()
dbg.execution_state="run"
