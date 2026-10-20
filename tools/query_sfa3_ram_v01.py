#!/usr/bin/env python3
"""Search RAM objects and source-backed field candidates in SFZ3Mix local SQLite knowledgebase."""
import argparse,json,sqlite3
p=argparse.ArgumentParser()
p.add_argument("--database",required=True)
p.add_argument("--address",help="CPU RAM address, for example 0xFF8400")
p.add_argument("--issue",help="Community issue id, for example hitboxes")
args=p.parse_args()
if bool(args.address)==bool(args.issue):p.error("Specify exactly one of --address or --issue")
db=sqlite3.connect(args.database)
db.row_factory=sqlite3.Row
out=[]
if args.address:
    addr=int(args.address,16)
    sources=db.execute("""SELECT rs.*,sl.slot,sl.cpu_address,sl.status AS slot_status,sl.observed_states,sl.active_marker_states
      FROM ram_slots sl JOIN ram_structures rs ON rs.id=sl.structure_id
      WHERE sl.cpu_address<=? AND ?<sl.cpu_address+rs.slot_stride ORDER BY rs.id,sl.slot""",(addr,addr)).fetchall()
else:
    sources=db.execute("""SELECT rs.*,sl.slot,sl.cpu_address,sl.status AS slot_status,sl.observed_states,sl.active_marker_states
      FROM ram_slots sl JOIN ram_structures rs ON rs.id=sl.structure_id
      JOIN ram_issue_links ril ON ril.structure_id=rs.id
      WHERE ril.issue_id=? ORDER BY rs.id,sl.slot LIMIT 40""",(args.issue,)).fetchall()
for s in sources:
    obj=dict(s)
    addr=obj["cpu_address"]
    obj["cpu_address"]=f"0x{addr:06X}"
    obj["fields"]=[dict(x) for x in db.execute("SELECT field,offset,semantics,status FROM ram_fields WHERE structure_id=? ORDER BY offset",(obj["id"],)).fetchall()]
    obj["observations"]=[dict(x) for x in db.execute("SELECT frame,nonzero_first_256,state_label FROM ram_observations WHERE structure_id=? AND slot=?",(obj["id"],obj["slot"])).fetchall()]
    obj["function_xrefs"]=[dict(x) for x in db.execute("SELECT * FROM function_ram_xrefs WHERE structure_id=?",(obj["id"],)).fetchall()]
    out.append(obj)
print(json.dumps({"results":out,"count":len(out)},indent=2))
db.close()
