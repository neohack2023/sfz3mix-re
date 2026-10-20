#!/usr/bin/env python3
"""Build/query a provenance-aware SFZ3 Mix function SQLite index.
Reads sanitized registry from the repository and optional local CFG. No ROM bytes stored.
"""
import argparse
import json
import sqlite3
from pathlib import Path

SCHEMA = """
PRAGMA foreign_keys=ON;
CREATE TABLE metadata(key TEXT PRIMARY KEY,value TEXT NOT NULL);
CREATE TABLE functions(
 id TEXT PRIMARY KEY, cpu_address INTEGER NOT NULL UNIQUE, address_space TEXT NOT NULL,
 file_member TEXT, file_offset INTEGER, mapping_status TEXT NOT NULL,
 name TEXT, role TEXT, confidence TEXT NOT NULL, status TEXT NOT NULL,
 entry_source TEXT NOT NULL, runtime_confirmed INTEGER NOT NULL,
 bounds_confirmed INTEGER NOT NULL, notes TEXT NOT NULL DEFAULT ''
);
CREATE TABLE issues(id TEXT PRIMARY KEY,title TEXT NOT NULL,source_url TEXT);
CREATE TABLE function_issues(function_id TEXT NOT NULL REFERENCES functions(id),
 issue_id TEXT NOT NULL REFERENCES issues(id),
 relationship TEXT NOT NULL, PRIMARY KEY(function_id,issue_id));
CREATE TABLE evidence(id TEXT PRIMARY KEY,evidence_type TEXT NOT NULL,uri TEXT NOT NULL,
 evidence_status TEXT NOT NULL,description TEXT NOT NULL);
CREATE TABLE function_evidence(function_id TEXT NOT NULL REFERENCES functions(id),
 evidence_id TEXT NOT NULL REFERENCES evidence(id),
 relation TEXT NOT NULL,PRIMARY KEY(function_id,evidence_id));
CREATE TABLE calls(id INTEGER PRIMARY KEY AUTOINCREMENT,
 caller_id TEXT REFERENCES functions(id),callee_id TEXT REFERENCES functions(id),
 site_address INTEGER NOT NULL,target_address INTEGER,
 kind TEXT NOT NULL,confidence TEXT NOT NULL,evidence_id TEXT REFERENCES evidence(id),
 UNIQUE(site_address,target_address,kind));
CREATE INDEX idx_func_address ON functions(cpu_address);
CREATE INDEX idx_calls_caller ON calls(caller_id);
CREATE INDEX idx_calls_callee ON calls(callee_id);
CREATE INDEX idx_issues_func ON function_issues(issue_id);
"""
ISSUES=[
("continue-score","Continue counter in score","https://www.reddit.com/r/romhacking/comments/1xa4ydk/street_fighter_zero_3_mix_is_dead/"),
("continue-sprites","Continue countdown sprite artifacts","https://www.reddit.com/r/romhacking/comments/1xa4ydk/street_fighter_zero_3_mix_is_dead/"),
("karin-roll","Karin rolling delay","https://www.reddit.com/r/romhacking/comments/1xa4ydk/street_fighter_zero_3_mix_is_dead/"),
("alpha-flash","Alpha Counter flash placement","https://www.reddit.com/r/romhacking/comments/1xa4ydk/street_fighter_zero_3_mix_is_dead/"),
("hitboxes","Original hitbox restoration","https://www.reddit.com/r/romhacking/comments/1xa4ydk/street_fighter_zero_3_mix_is_dead/"),
("background-evasion","Background evasion foreground pop","https://www.reddit.com/r/romhacking/comments/1xa4ydk/street_fighter_zero_3_mix_is_dead/"),
("fbneo-floor","FBNeo floor-edge renderer glitch","https://github.com/finalburnneo/FBNeo/issues/1833"),
("max-characters","Alpha 3 MAX character feasibility","https://www.reddit.com/r/romhacking/comments/1xa4ydk/street_fighter_zero_3_mix_is_dead/")
]
ALIASES={"continue-counter: investigative lead only":"continue-score",
         "continue-screen sprite artifact: investigative lead only":"continue-sprites"}
def build(registry,cfg,database):
    if database.exists(): raise FileExistsError(database)
    source=json.loads(registry.read_text(encoding="utf-8"))
    con=sqlite3.connect(database)
    try:
        con.executescript(SCHEMA)
        for key in ("schema","source_archive_sha256","cpu_program_sha256","derived_from"):
            con.execute("INSERT INTO metadata VALUES (?,?)",(key,str(source[key])))
        con.executemany("INSERT INTO issues VALUES (?,?,?)",ISSUES)
        con.execute("INSERT INTO evidence VALUES (?,?,?,?,?)",
                    ("registry-v01","static_registry","docs/FUNCTION_REGISTRY_V01.json",
                     "UNVERIFIED","Host 02 sanitized static CFG seed registry"))
        addr_to_id={}
        for fn in source["entries"]:
            addr=int(fn["cpu_address"],16)
            addr_to_id[addr]=fn["id"]
            con.execute("""INSERT INTO functions
            (id,cpu_address,address_space,file_member,file_offset,mapping_status,
            name,role,confidence,status,entry_source,runtime_confirmed,bounds_confirmed,notes)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (fn["id"],addr,"HBMAME :maincpu program address",
             "sz3mx.03",None,"SAMPLED_MAPPING_ONLY",None,None,"LOW",
             fn["status"],fn["source"],int(fn["runtime_confirmed"]),
             int(fn["function_bounds_confirmed"]),"file offset not assigned until verified for this entry"))
            con.execute("INSERT INTO function_evidence VALUES (?,?,?)",
                        (fn["id"],"registry-v01","candidate provenance"))
            for item in fn.get("linked_community_todos",[]):
                issue=ALIASES.get(item)
                if issue:con.execute("INSERT INTO function_issues VALUES (?,?,?)",
                     (fn["id"],issue,"investigative_candidate_not_causal"))
        if cfg:
            graph=json.loads(cfg.read_text(encoding="utf-8"))
            if graph["cpu_sha256"]!=source["cpu_program_sha256"]:
                raise ValueError("CFG/registry CPU hashes differ")
            con.execute("INSERT INTO evidence VALUES (?,?,?,?,?)",
                  ("cfg-local","static_cfg",str(cfg),"STATIC_CANDIDATE",
                   "Local Capstone CFG; targets do not prove executed calls"))
            for edge in graph["edges"]:
                if edge["kind"]!="call" or edge["to"] is None:continue
                site=int(edge["from"],16); target=int(edge["to"],16)
                # Caller owners require control-flow function boundaries, not merely closest address.
                con.execute("""INSERT OR IGNORE INTO calls
                (caller_id,callee_id,site_address,target_address,kind,confidence,evidence_id)
                VALUES (?,?,?,?,?,?,?)""",
                (None,addr_to_id.get(target),site,target,"static_direct_call","LOW","cfg-local"))
        con.commit()
        print(json.dumps({"status":"PASS","function_candidates":con.execute("SELECT count(*) FROM functions").fetchone()[0],
              "static_calls":con.execute("SELECT count(*) FROM calls").fetchone()[0],
              "unresolved_call_owners":con.execute("SELECT count(*) FROM calls WHERE caller_id IS NULL").fetchone()[0],
              "issue_links":con.execute("SELECT count(*) FROM function_issues").fetchone()[0],
              "db":str(database)},indent=2))
    except Exception:
        con.close()
        database.unlink(missing_ok=True)
        raise
    finally: con.close()
def query(database,term,limit):
    con=sqlite3.connect(database)
    try:
        con.row_factory=sqlite3.Row
        term=term.strip()
        if term.startswith("0x"):
            query="SELECT * FROM functions WHERE cpu_address=?";args=(int(term,16),)
        else:
            query="""SELECT DISTINCT f.* FROM functions f
               LEFT JOIN function_issues fi ON fi.function_id=f.id
               LEFT JOIN issues i ON i.id=fi.issue_id
               WHERE f.id LIKE ? OR COALESCE(f.name,'') LIKE ? OR
               COALESCE(f.role,'') LIKE ? OR i.title LIKE ?
               ORDER BY f.cpu_address LIMIT ?"""
            args=tuple(["%"+term+"%"]*4+[limit])
        rows=[dict(x) for x in con.execute(query,args).fetchall()]
        for row in rows:
            row["incoming_calls"]=[dict(x) for x in con.execute(
                "SELECT site_address,target_address,kind,confidence FROM calls WHERE callee_id=?",
                (row["id"],)).fetchall()]
            row["outgoing_calls"]=[dict(x) for x in con.execute(
                "SELECT site_address,target_address,kind,confidence FROM calls WHERE caller_id=?",
                (row["id"],)).fetchall()]
            row["issues"]=[dict(x) for x in con.execute(
                "SELECT i.id,i.title,fi.relationship FROM issues i JOIN function_issues fi ON fi.issue_id=i.id WHERE fi.function_id=?",
                (row["id"],)).fetchall()]
            row["evidence"]=[dict(x) for x in con.execute(
                "SELECT e.id,e.uri,e.evidence_status FROM evidence e JOIN function_evidence fe ON fe.evidence_id=e.id WHERE fe.function_id=?",
                (row["id"],)).fetchall()]
        print(json.dumps({"results":rows},indent=2))
    finally:con.close()
def main():
    p=argparse.ArgumentParser()
    s=p.add_subparsers(dest="cmd",required=True)
    b=s.add_parser("build");b.add_argument("--registry",type=Path,required=True)
    b.add_argument("--cfg",type=Path);b.add_argument("--database",type=Path,required=True)
    q=s.add_parser("query");q.add_argument("--database",type=Path,required=True)
    q.add_argument("--term",required=True);q.add_argument("--limit",type=int,default=20)
    a=p.parse_args()
    if a.cmd=="build":build(a.registry,a.cfg,a.database)
    else:query(a.database,a.term,a.limit)
if __name__=="__main__":main()
