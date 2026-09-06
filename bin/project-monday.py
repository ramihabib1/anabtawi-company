#!/usr/bin/env python3
"""Project the repository into monday. The only process that writes monday. Stdlib only.

Writes: Run Health (from state/*.md), Decisions (from approvals/pending and briefs/), never deletes, never touches the
`decision` column. Upserts Decisions by dec_id. Exits non-zero if ops/monday-ids.json lacks a board it needs.
"""
import json, pathlib, sys, re, datetime, os, subprocess
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from monday_api import gql

ROOT = pathlib.Path(__file__).resolve().parent.parent
IDS = json.loads((ROOT / "ops" / "monday-ids.json").read_text())
os.environ["TZ"] = "Asia/Jerusalem"
TODAY = datetime.date.today().isoformat()
DEPTS = ["ceo", "finance", "supply-chain", "advertising", "catalog", "pricing-intel", "customer", "account-health", "expansion", "ops"]
REPO_URL = subprocess.run(["git", "config", "--get", "remote.origin.url"], cwd=ROOT, capture_output=True, text=True).stdout.strip().removesuffix(".git")

def board(key):
    b = IDS["boards"].get(key)
    if not b:
        sys.exit(f"ops/monday-ids.json has no board {key}; run bin/build-monday.py --init")
    return b

def items(board_id):
    out, cursor = {}, None
    while True:
        q = 'query($b:[ID!],$c:String){ boards(ids:$b){ items_page(limit:200, cursor:$c){ cursor items { id name column_values { id text } } } } }'
        page = gql(q, {"b": [board_id], "c": cursor})["boards"][0]["items_page"]
        for it in page["items"]:
            out[it["name"]] = it
        cursor = page["cursor"]
        if not cursor:
            return out

def set_values(board_id, item_id, values):
    gql('mutation($b:ID!,$i:ID!,$v:JSON!){ change_multiple_column_values(board_id:$b, item_id:$i, column_values:$v){ id } }',
        {"b": board_id, "i": item_id, "v": json.dumps(values)})

def create(board_id, name, values, group_id=None):
    q = 'mutation($b:ID!,$n:String!,$v:JSON!,$g:String){ create_item(board_id:$b, item_name:$n, column_values:$v, group_id:$g){ id } }'
    return gql(q, {"b": board_id, "n": name, "v": json.dumps(values), "g": group_id})["create_item"]["id"]

def scheduled_today():
    jobs = json.loads((ROOT / "docs" / "jobs.json").read_text())["jobs"]
    return {j["dept"] for j in jobs}

def run_health():
    b = board("run_health"); existing = items(b["id"]); sched = scheduled_today()
    for d in DEPTS:
        p = ROOT / "state" / f"{d}.md"
        if d == "ops":
            p = ROOT / "state" / "preflight.md"
        if d not in sched:
            vals = {"status": {"label": "Not scheduled"}}
        elif not p.exists():
            vals = {"status": {"label": "Stale"}, "tools_failed": "no state file"}
        else:
            head = p.read_text().splitlines()[0]
            m = re.search(r"(\d{4}-\d{2}-\d{2})", head)
            date = m.group(1) if m else ""
            failed = "tools_failed" in head
            vals = {"status": {"label": "Failed" if failed else ("OK" if date == TODAY else "Stale")},
                    "state_date": {"date": date} if date else None,
                    "last_run": {"date": TODAY, "time": datetime.datetime.now().strftime("%H:%M:%S")},
                    "harness": {"labels": ["claude-code"]},
                    "tools_failed": head.split("tools_failed:")[-1] if failed else "",
                    "log": {"url": f"{REPO_URL}/blob/main/state/{p.name}", "text": "state file"}}
            vals = {k: v for k, v in vals.items() if v is not None}
        if d in existing:
            set_values(b["id"], existing[d]["id"], vals)
        else:
            create(b["id"], d, vals)
    print("run health projected")

def parse_packet(path):
    text = path.read_text()
    m = re.search(r"```json\n(.*?)\n```", text, re.S)
    return json.loads(m.group(1)) if m else None

def decisions():
    b = board("decisions"); existing = items(b["id"])
    group_today = b["groups"].get("Today")
    rank = 0
    for path in sorted((ROOT / "approvals" / "pending").glob("*.md")):
        pk = parse_packet(path)
        if not pk:
            continue
        rank += 1
        vals = {"dec_id": pk["id"], "rank": str(rank), "tier": {"label": pk["tier"]}, "dept": {"labels": [pk["department"]]},
                "impact_cad": pk.get("estimated_cost", "0.00"),
                "expires": {"date": pk["expires"][:10], "time": pk["expires"][11:16] + ":00"},
                "if_ignored": {"text": pk["if_ignored"][:1990]}, "evidence": {"text": "\n".join(pk["evidence"])[:1990]},
                "approval_file": {"url": f"{REPO_URL}/blob/main/approvals/pending/{path.name}", "text": path.name}}
        title = pk.get("impact", pk["id"])[:60]
        if pk["id"] in {v["column_values"][0]["text"] if v["column_values"] else "" for v in existing.values()} or title in existing:
            it = existing.get(title)
            if it:
                set_values(b["id"], it["id"], vals)
        else:
            vals["decision"] = {"label": "Pending"}
            create(b["id"], title, vals, group_today)
    print(f"decisions projected: {rank} pending")

if __name__ == "__main__":
    run_health()
    decisions()
