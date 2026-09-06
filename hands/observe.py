#!/usr/bin/env python3
"""The observing runner. Contains NO write path to Amazon, DataDoe, QuickBooks or a bank, and refuses to start if a
write-scoped variable is present. Every 5 minutes (or by hand): pull, verify the ledger chain, read pending packets at git
HEAD, project them to monday, read the decision column back, and on Approved move the file and write ONE dry-run ledger
row. Nothing reads approvals/approved/. Rami's tap is recorded intent, not authorization, until the two-identity test passes.
"""
import json, os, pathlib, re, subprocess, sys, datetime
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "bin"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from monday_api import gql
import ledger

ROOT = pathlib.Path(__file__).resolve().parent.parent
os.environ["TZ"] = "Asia/Jerusalem"
NOW = datetime.datetime.now().astimezone()

def refuse_write_env():
    bad = [k for k in os.environ if re.match(r"(DATADOE_WRITE|ADS_|SP_API_|QBO_|QUICKBOOKS_)", k)]
    if bad:
        sys.exit(f"refusing to start: write-scoped variables present: {bad}")

def git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True)

def packet_at_head(path):
    text = git("show", f"HEAD:{path}").stdout
    m = re.search(r"```json\n(.*?)\n```", text, re.S)
    return (json.loads(m.group(1)), text) if m else (None, text)

def valid(pk):
    req = ["id", "schema_version", "department", "tier", "action_class", "status", "mode", "created", "expires", "marketplace", "currency", "estimated_cost", "evidence", "impact", "if_ignored", "metric", "expected", "review_on", "design", "rule_refs"]
    missing = [k for k in req if k not in pk]
    if missing: return f"missing {missing}"
    if pk["schema_version"] != "1.0": return "schema_version"
    if pk["tier"] != "T2": return "runner touches T2 only"
    if pk["mode"] != "dry-run": return "mode must be dry-run"
    if datetime.datetime.fromisoformat(pk["expires"]) < NOW: return "expired"
    if not re.fullmatch(r"-?[0-9]+\.[0-9]{2}", pk["estimated_cost"]): return "estimated_cost not a decimal string"
    return None

def decision_of(dec_id):
    ids = json.loads((ROOT / "ops" / "monday-ids.json").read_text())
    b = ids["boards"]["decisions"]["id"]
    q = 'query($b:[ID!]){ boards(ids:$b){ items_page(limit:200){ items { id column_values(ids:["dec_id","decision"]) { id text } } } } }'
    for it in gql(q, {"b": [b]})["boards"][0]["items_page"]["items"]:
        cv = {c["id"]: c["text"] for c in it["column_values"]}
        if cv.get("dec_id") == dec_id:
            return cv.get("decision"), it["id"]
    return None, None

def main():
    refuse_write_env()
    if (ROOT / "ops" / "PAUSE").exists():
        (ROOT / "state" / "hands.md").write_text(f"# hands · {NOW.date()} · paused\n"); return
    r = git("pull", "--rebase", "--autostash")
    if r.returncode != 0:
        sys.exit("git pull failed; stopping without guessing")
    ledger.verify()
    moved = 0
    for path in sorted((ROOT / "approvals" / "pending").glob("*.md")):
        rel = f"approvals/pending/{path.name}"
        pk, text = packet_at_head(rel)
        if pk is None:
            continue
        why = valid(pk)
        if why:
            dest = ROOT / "approvals" / ("expired" if why == "expired" else "rejected") / path.name
            git("mv", rel, str(dest.relative_to(ROOT)))
            dest.write_text(text + f"\n\n> runner: {why} at {NOW.isoformat(timespec='minutes')}\n")
            continue
        label, item_id = decision_of(pk["id"])
        if label == "Approved":
            pk.update({"status": "approved", "decided_by": "monday-status (identity unverified)", "decided_at": NOW.isoformat(timespec="seconds"), "decision_channel": "monday", "monday_item_id": item_id})
            new_text = re.sub(r"```json\n.*?\n```", "```json\n" + json.dumps(pk, indent=2) + "\n```", text, flags=re.S)
            dest = f"approvals/approved/{path.name}"
            git("mv", rel, dest); (ROOT / dest).write_text(new_text)
            ledger.append({"department": pk["department"], "tier": "T2", "action_class": pk["action_class"], "runtime": "hands-runner",
                           "actor": "hands/observe.py", "marketplace": pk["marketplace"], "currency": pk["currency"], "amount": pk["estimated_cost"],
                           "target": {"skus": pk.get("skus", [])}, "input": {"packet": pk["id"]}, "output": {"status": "dry-run"},
                           "verification": None, "approval_id": pk["id"], "decided_by": pk["decided_by"],
                           "reason": "execution disabled: no write path compiled in", "evidence": pk["evidence"], "rule_refs": pk.get("rule_refs", [])})
            moved += 1
        elif label == "Rejected":
            git("mv", rel, f"approvals/rejected/{path.name}")
    (ROOT / "state" / "hands.md").write_text(f"# hands · {NOW.date()} · tick {NOW.strftime('%H:%M')} · approved_moved:{moved}\n")
    git("add", "-A"); git("commit", "-q", "-m", f"hands: {NOW.date()} tick"); git("push", "-q")

if __name__ == "__main__":
    main()
