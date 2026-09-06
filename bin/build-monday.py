#!/usr/bin/env python3
"""Create the monday workspace from docs/monday-schema.yaml. Stdlib + the schema (rendered to JSON first).

  bin/build-monday.py --render      # writes docs/monday-schema.json from the yaml (needs PyYAML once, on any machine)
  bin/build-monday.py --init        # creates workspace, boards, columns, groups, items; writes ops/monday-ids.json
  bin/build-monday.py --verify      # reads every board back and checks ids

Column ids are set explicitly with create_column(id:). Ids can never be reused after deletion, so --init refuses to run
if ops/monday-ids.json already names a board. Views, automations and dashboards are created by hand in the UI tonight
(the API paths for filtered views and widgets are unverified); the schema lists exactly what to click.
"""
import json, pathlib, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from monday_api import gql, me

ROOT = pathlib.Path(__file__).resolve().parent.parent
IDS = ROOT / "ops" / "monday-ids.json"

def load_schema():
    p = ROOT / "docs" / "monday-schema.json"
    if not p.exists():
        sys.exit("run --render first (docs/monday-schema.json missing)")
    return json.loads(p.read_text())

def render():
    import yaml
    d = yaml.safe_load((ROOT / "docs" / "monday-schema.yaml").read_text())
    (ROOT / "docs" / "monday-schema.json").write_text(json.dumps(d, indent=2))
    print("rendered docs/monday-schema.json")

def settings_for(col):
    t = col["type"]
    if t in ("status", "dropdown"):
        labels = col["labels"]
        if t == "status":
            return json.dumps({"labels": {str(i): l for i, l in enumerate(labels)}})
        return json.dumps({"labels": [{"id": i + 1, "name": l} for i, l in enumerate(labels)]})
    return None

def init():
    s = load_schema()
    ids = json.loads(IDS.read_text())
    if ids.get("boards"):
        sys.exit("ops/monday-ids.json already has boards; refusing to re-init (ids cannot be reused)")
    who = me()
    print(f"building as monday user {who['id']} {who['name']}")
    ws = gql('mutation($n:String!){ create_workspace(name:$n, kind: open, description:"Anabtawi OS") { id } }', {"n": s["workspace"]})["create_workspace"]["id"]
    ids["workspace_id"] = ws
    for key, b in s["boards"].items():
        board = gql('mutation($n:String!,$w:ID!,$o:[ID!]){ create_board(board_name:$n, board_kind: public, workspace_id:$w, board_owner_ids:$o){ id } }',
                    {"n": b["name"], "w": ws, "o": [s["owner_user_id"]]})["create_board"]["id"]
        ids["boards"][key] = {"id": board, "name": b["name"], "groups": {}}
        for col in b["columns"]:
            args = {"b": board, "id": col["id"], "t": col["title"], "ty": col["type"]}
            q = 'mutation($b:ID!,$id:String!,$t:String!,$ty:ColumnType!,$d:JSON){ create_column(board_id:$b, id:$id, title:$t, column_type:$ty, defaults:$d){ id } }'
            args["d"] = settings_for(col)
            got = gql(q, args)["create_column"]["id"]
            if got != col["id"]:
                sys.exit(f"column id mismatch on {key}.{col['id']}: got {got}")
            time.sleep(0.3)
        for g in b.get("groups", []):
            gid = gql('mutation($b:ID!,$g:String!){ create_group(board_id:$b, group_name:$g){ id } }', {"b": board, "g": g})["create_group"]["id"]
            ids["boards"][key]["groups"][g] = gid
        for item in b.get("items", []):
            gql('mutation($b:ID!,$n:String!){ create_item(board_id:$b, item_name:$n){ id } }', {"b": board, "n": item})
        IDS.write_text(json.dumps(ids, indent=2))
        print(f"board {b['name']} = {board}")
    print("done. Now in the UI: create the views, automations and the Cockpit dashboard listed in docs/monday-schema.yaml.")

def verify():
    s = load_schema(); ids = json.loads(IDS.read_text()); ok = True
    for key, b in s["boards"].items():
        bid = ids["boards"].get(key, {}).get("id")
        if not bid:
            print(f"MISSING board {key}"); ok = False; continue
        cols = gql('query($b:[ID!]){ boards(ids:$b){ columns { id type } } }', {"b": [bid]})["boards"][0]["columns"]
        have = {c["id"] for c in cols}
        for col in b["columns"]:
            if col["id"] not in have:
                print(f"MISSING column {key}.{col['id']}"); ok = False
    print("verify:", "OK" if ok else "FAIL"); sys.exit(0 if ok else 1)

if __name__ == "__main__":
    a = sys.argv[1:] or ["--help"]
    {"--render": render, "--init": init, "--verify": verify}.get(a[0], lambda: print(__doc__))()
