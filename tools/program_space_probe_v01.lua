-- Read-only test of HBMAME :maincpu program-space byte/address correspondence.
-- This DOES NOT prove that opcode fetches (potentially decrypted) match data reads.
local out = assert(io.open("D:/AIOS_SFZ3MIX_V032/evidence/program_space_probe_v01.tsv", "w"))
local cpu = assert(manager.machine.devices[":maincpu"])
local space = assert(cpu.spaces["program"])
local addresses = {0x000000, 0x000008, 0x000100, 0x0032A0, 0x00331C, 0x025C40, 0x025CC0, 0x026438, 0x05FF00}
local completed = false
emu.register_frame_done(function()
  if completed then return end
  completed = true
  out:write("emulator_cpu_address\tprogram_space_read_u8_32bytes\n")
  for _, address in ipairs(addresses) do
    local bytes = {}
    local ok, err = pcall(function()
      for i = 0, 31 do
        bytes[#bytes + 1] = string.format("%02x", space:read_u8(address + i))
      end
    end)
    if ok then
      out:write(string.format("%06X\t%s\n", address, table.concat(bytes)))
    else
      out:write(string.format("%06X\tERROR:%s\n", address, tostring(err)))
    end
  end
  out:flush()
  out:close()
  manager.machine:exit()
end, "frame")
