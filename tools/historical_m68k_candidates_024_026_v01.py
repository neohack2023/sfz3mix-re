#!/usr/bin/env python3
"""Verify 0.24-0.26 historical CPU programs, compare stable anchors, inspect candidate 68k windows.
Read-only. Only archive hashes and sanitized numerical summaries emitted. Temporary archives removed.
"""
import hashlib,json,subprocess,tempfile,urllib.request,sys,collections
from pathlib import Path
sys.path.insert(0,r"D:\AIOS_SFZ3MIX_V032\tools\.vendor")
from capstone import Cs, CS_ARCH_M68K, CS_MODE_BIG_ENDIAN
EXPECTED={
24:("9082929fd7075502a35e5f977f3ccb6cc3dbafc35fd9e693e7508fe61ae7b9d7","2fba55f17fa2801cb05ce07a9ba66ed515cb1163dde69592728214a6a77b2f8f","sfz3mix.p1"),
25:("cdde7583917bfb13d0c985184c2ee2fa1b99a266610e544fc1b8f545cbb6a4c6","5ff23470ddec1dadc9935c370adfef4408beb92f0cccac94181d1dfe81e948c4","sfz3mix.p1"),
26:("7bc49cc6c88460efe67a38f8c405081af4eee53ac71230bc2f9732128da4290c","7724bf1ea71d9a85f88054307c1a195637736d372e1a92c4831dc43d25b9452e","sz3mx.03"),
}
def digest(blob):return hashlib.sha256(blob).hexdigest()
def recovered(a,b):
    same=sum(x==y for x,y in zip(a,b))
    chunks={}
    for n in (16,32,64,128,256):
        chunks[str(n)]={"identical_aligned_blocks":sum(a[i:i+n]==b[i:i+n] for i in range(0,len(a),n)), "total_blocks":(len(a)+n-1)//n}
    offsets=[0x379AE,0x37A46,0x37A56,0x37AD2,0x2C584]
    anchors=[]
    for off in offsets:
        d=min(256,len(a)-off)
        exact=sum(x==y for x,y in zip(a[off:off+d],b[off:off+d]))
        anchors.append({"v032_research_offset":hex(off),"size":d,"same_position_equal_bytes":exact,"bytes_checked":d,"cross_release_address_semantics_unverified":True})
    islands=[]
    limit=0x20000;i=0
    while i<limit:
        if a[i]==b[i]:i+=1;continue
        start=i
        while i<limit and a[i]!=b[i]:i+=1
        if i-start<=20 and start>=16 and i+16<=limit and a[start-16:start]==b[start-16:start] and a[i:i+16]==b[i:i+16]:
            islands.append({"offset":hex(start),"length":i-start,"before_instructions":inspect(a,max(0,(start-8)&~1),20),"after_instructions":inspect(b,max(0,(start-8)&~1),20)})
        if len(islands)>=25:break
    return {"same_position_equal_bytes":same,"total_bytes":len(a),"aligned_blocks":chunks,"v032_address_probe_only":anchors,"sparse_candidate_sites_in_first_128KiB":islands}
dis=Cs(CS_ARCH_M68K,CS_MODE_BIG_ENDIAN)
def inspect(b,p,n):return [{"offset":hex(x.address),"mnemonic":x.mnemonic,"operands":x.op_str} for x in list(dis.disasm(b[p:p+n],p))[:7]]
def main():
    data={}
    with tempfile.TemporaryDirectory(prefix="sfz3mix_semantic_",dir=r"C:\AIOS\_TEMP") as d:
        for v in EXPECTED:
            ark,cpu,member=EXPECTED[v];f=Path(d)/f"{v}.7z"
            with urllib.request.urlopen(f"https://sfz3mix.github.io/download/0.{v}/sfz3mix.7z",timeout=90) as inp, f.open("wb") as out:
                import shutil;shutil.copyfileobj(inp,out)
            assert digest(f.read_bytes())==ark,f"archive SHA failed {v}"
            test=subprocess.run([r"C:\Program Files\7-Zip\7z.exe","t",str(f)],capture_output=True,timeout=100)
            assert test.returncode==0,f"7z test failed {v}"
            p=subprocess.run([r"C:\Program Files\7-Zip\7z.exe","e","-so",str(f),member],capture_output=True,timeout=100)
            assert p.returncode==0 and digest(p.stdout)==cpu,f"CPU hash failed {v}"
            data[v]=p.stdout
            f.unlink()
            print("VERIFIED",v,len(p.stdout),cpu,flush=True)
    res={"status":"STRUCTURAL_CANDIDATES_NOT_FUNCTION_RECOVERY","sample":"verified historical 0.24 0.25 0.26","comparisons":{"0.24_to_0.25":recovered(data[24],data[25]),"0.25_to_0.26":recovered(data[25],data[26])}}
    print("JSON_BEGIN");print(json.dumps(res,separators=(",",":")));print("JSON_END")
if __name__=="__main__":main()
