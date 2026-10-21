"""ROM-backed bounded M68000 export. No debugger expression evaluation."""
import argparse,hashlib,json,sys
from pathlib import Path
ROOT=Path(r"D:\AIOS_SFZ3MIX_V032")
sys.path.insert(0,str(ROOT/"tools/.vendor"))
from capstone import Cs,CS_ARCH_M68K,CS_MODE_BIG_ENDIAN,CS_MODE_M68K_000
def decode(data,start,length):
 if type(start) is not int or type(length) is not int:raise ValueError("Addresses and lengths must be integers, not expressions")
 if start<0 or start%2 or length<2 or length>256 or length%2 or start+length>len(data):raise ValueError("Unaligned/out-of-bounds range or 256-byte budget exceeded")
 md=Cs(CS_ARCH_M68K,CS_MODE_BIG_ENDIAN|CS_MODE_M68K_000)
 rows=[];pc=start
 while pc<start+length:
  i=next(md.disasm(data[pc:pc+24]+bytes(24),pc,count=1),None)
  if i is None or i.size<2 or i.address!=pc or i.mnemonic=="dc.w" or pc+i.size>start+length:raise ValueError(f"Incomplete/invalid instruction at {pc:X}")
  rows.append(dict(pc=pc,size=i.size,opcode=i.bytes.hex(),instruction=i.mnemonic+" "+i.op_str))
  if len(rows)>128:raise ValueError("Instruction budget exceeded")
  pc+=i.size
 return rows
def fixture():
 data=bytes.fromhex("4e7170004e75")
 x=decode(data,0,6);assert [i["pc"] for i in x]==[0,2,4]
 assert [i["instruction"].split()[0] for i in x]==["nop","moveq","rts"]
 negatives=[(0,"a6"),(0,"0xa6"),(0,258),(1,2),(0,8),(0,1),(0,-2)]
 for a,n in negatives:
  try:decode(data,a,n)
  except ValueError:pass
  else:raise AssertionError((a,n))
 try:decode(bytes.fromhex("203c0000"),0,4)
 except ValueError:pass
 else:raise AssertionError("Truncated longword accepted")
 return dict(status="PASS",fixture_bytes=6,instructions=3,negative_cases=8,maximum_export_bytes=256,debugger_commands=0)
def main():
 p=argparse.ArgumentParser();p.add_argument("--fixture",action="store_true");p.add_argument("--start",type=lambda x:int(x,0));p.add_argument("--length",type=lambda x:int(x,0));p.add_argument("--output",type=Path);a=p.parse_args()
 if a.fixture:print(json.dumps(fixture()));return
 b=(ROOT/"tools/sz3mx.03").read_bytes()
 assert hashlib.sha256(b).hexdigest()=="b5f7a1598e4f91a5113c506505b482b2cd1a19e366fe31471740e45dbd204691"
 out=dict(start=a.start,end_exclusive=a.start+a.length,instructions=decode(b,a.start,a.length),mapping="STATIC_ROM_BYTES_ONLY")
 text=json.dumps(out,indent=2);assert len(text)<65536
 with a.output.open("x") as f:f.write(text)
 print(json.dumps(dict(status="PASS",output=str(a.output),bytes=a.length,instructions=len(out["instructions"]))))
if __name__=="__main__":main()
