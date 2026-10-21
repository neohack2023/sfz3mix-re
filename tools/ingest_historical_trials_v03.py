"""Add V03 trial receipts without assigning gameplay semantics or function owners."""
import hashlib,json,sqlite3
from pathlib import Path
R=Path(r"D:\AIOS_SFZ3MIX_V032")
E=Path(r"C:\AIOS\_TEMP\SFZ3MIX_V03_EVIDENCE_RETRY02")
def rows_digest(c,t):
 h=hashlib.sha256()
 for row in c.execute('SELECT * FROM "'+t+'" ORDER BY rowid'):
  h.update(repr(row).encode())
 return h.hexdigest()
def main():
 data=json.loads((E/"receipt.json").read_text())
 assert len(data)==3
 c=sqlite3.connect(R/"evidence/functions_v01.sqlite")
 assert c.execute("pragma integrity_check").fetchall()==[("ok",)]
 assert not c.execute("pragma foreign_key_check").fetchall()
 tables=[x[0] for x in c.execute("select name from sqlite_master where type='table' and name not like 'sqlite_%'")]
 before={t:rows_digest(c,t) for t in tables}
 backup=E/"functions_v01_before_historical_v03.sqlite"
 assert not backup.exists()
 with sqlite3.connect(backup) as b:c.backup(b)
 with c:
  c.execute("CREATE TABLE historical_execution_trials_v03 (version TEXT PRIMARY KEY, driver TEXT NOT NULL, evidence_class TEXT NOT NULL, receipt_json TEXT NOT NULL, log_sha256 TEXT, roll_verified INTEGER NOT NULL CHECK(roll_verified=0), function_owner TEXT CHECK(function_owner IS NULL))")
  for r in data:
   if r.get("log_sha256"):
    assert hashlib.sha256((E/("v"+r["version"].split(".")[1]+"_probe.jsonl")).read_bytes()).hexdigest()==r["log_sha256"]
   c.execute("INSERT INTO historical_execution_trials_v03 VALUES(?,?,?,?,?,0,NULL)",(r["version"],r["driver"],"BOUNDED_EXECUTION_ATTEMPT_NOT_GAMEPLAY_VALIDATED",json.dumps(r,sort_keys=True),r.get("log_sha256")))
  assert {t:rows_digest(c,t) for t in tables}==before
  assert c.execute("pragma integrity_check").fetchall()==[("ok",)]
  assert not c.execute("pragma foreign_key_check").fetchall()
 result={"status":"PASS","previous_tables_preserved":len(tables),"new_trials":3,"integrity":"ok","foreign_key_violations":0,"function_owners_added":0,"backup":str(backup)}
 (E/"sqlite_receipt.json").write_text(json.dumps(result,indent=2));print(json.dumps(result))
if __name__=="__main__":main()
