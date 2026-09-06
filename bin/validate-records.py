#!/usr/bin/env python3
"""Validate the day-1 records: state files, observations, packets, briefs. Stdlib only. Exit 1 on any failure."""
import json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
errors = []
for p in (ROOT / "state").glob("*.md"):
    if p.name in ("locks.md", "calendar.md", "hands.md"): continue
    head = p.read_text().splitlines()[0] if p.read_text().strip() else ""
    if not re.match(r"^# [a-z-]+ · \d{4}-\d{2}-\d{2} · job:[a-z.-]+", head):
        errors.append(f"{p}: bad header line: {head!r}")
for p in (ROOT / "departments").glob("*/memory/????-??-??.md"):
    for i, line in enumerate(p.read_text().splitlines(), 1):
        if line.startswith("- ") and not re.match(r"^- obs-\d{8}-[a-z-]+-\d{2} · .+ · scope:.+ · .+ · source:.+", line):
            errors.append(f"{p}:{i}: observation line malformed")
schema = json.loads((ROOT / "docs" / "schemas" / "approval-packet.schema.json").read_text())
for p in (ROOT / "approvals").glob("*/*.md"):
    m = re.search(r"```json\n(.*?)\n```", p.read_text(), re.S)
    if not m: errors.append(f"{p}: no json front matter block"); continue
    try: pk = json.loads(m.group(1))
    except Exception as e: errors.append(f"{p}: json error {e}"); continue
    for k in schema["required"]:
        if k not in pk: errors.append(f"{p}: missing {k}")
    for k, spec in schema["properties"].items():
        if k in pk and "enum" in spec and pk[k] not in spec["enum"]: errors.append(f"{p}: {k} not in enum")
        if k in pk and "pattern" in spec and isinstance(pk[k], str) and not re.fullmatch(spec["pattern"], pk[k]): errors.append(f"{p}: {k} fails pattern")
for p in (ROOT / "briefs").glob("*-decisions.md"):
    head = p.read_text().splitlines()[0]
    if not head.startswith("# decisions · "): errors.append(f"{p}: bad header")
print("\n".join(errors) if errors else "records OK")
sys.exit(1 if errors else 0)
