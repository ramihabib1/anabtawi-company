"""Append-only hash-chained ledger. The only writer of ledger/actions.jsonl. Stdlib only."""
import json, hashlib, pathlib, datetime, os, subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
LEDGER = ROOT / "ledger" / "actions.jsonl"

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()

def rows():
    if not LEDGER.exists() or LEDGER.stat().st_size == 0:
        return []
    return [json.loads(l) for l in LEDGER.read_text().splitlines() if l.strip()]

def verify():
    prev = "GENESIS"
    for i, r in enumerate(rows(), 1):
        body = {k: v for k, v in r.items() if k != "hash"}
        if r["seq"] != i or r["prev_hash"] != prev or hashlib.sha256(canonical(body)).hexdigest() != r["hash"]:
            raise SystemExit(f"ledger chain broken at seq {r.get('seq')}")
        prev = r["hash"]
    return prev

def append(entry):
    prev = verify()
    seq = len(rows()) + 1
    os.environ["TZ"] = "Asia/Jerusalem"
    entry = {**entry, "seq": seq, "ts": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
             "schema_version": "1.0", "prev_hash": prev}
    if seq == 1 or datetime.datetime.now().hour < 1:
        entry["git_anchor"] = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip() or None
    entry["hash"] = hashlib.sha256(canonical(entry)).hexdigest()
    with LEDGER.open("a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry
