#!/usr/bin/env python3
"""Run one job from docs/jobs.json as a headless Claude Code call. Stdlib only.

  bin/run-job.py <job-id>            run one job
  bin/run-job.py --chain <job-id>    run the job and everything chained after it

The wrapper, not the model, guarantees the state file: if the model fails or times out, the wrapper
writes state/<dept>.md with tools_failed so a failed run is never silent. Secrets come from the
environment (source ~/.anabtawi/env first); this script never prints them.
"""
import json, os, subprocess, sys, tempfile, datetime, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
TZ = "Asia/Jerusalem"

def today():
    os.environ["TZ"] = TZ
    return datetime.date.today().isoformat()

def load(p):
    return json.loads((ROOT / p).read_text())

def render_mcp(server_names, servers):
    cfg = {"mcpServers": {}}
    for name in server_names:
        s = servers["servers"][name]
        if s.get("status") == "not_built":
            sys.exit(f"job uses server {name} whose status is not_built")
        for var in s.get("env", []):
            if var not in os.environ:
                sys.exit(f"missing environment variable {var} for server {name}")
        entry = {"type": s["transport"], "url": s["url"]}
        if s.get("headers"):
            entry["headers"] = {k: os.path.expandvars(v) for k, v in s["headers"].items()}
        cfg["mcpServers"][name] = entry
    f = tempfile.NamedTemporaryFile("w", suffix=".mcp.json", delete=False)
    json.dump(cfg, f); f.close()
    return f.name

def prompt_for(job):
    d = today()
    lines = [f"You are the {job['dept']} department of Anabtawi OS. Today is {d} ({TZ}). Job id: {job['id']}.",
             "Read these files first, in this order, and obey AGENTS.md above everything:"]
    lines += [f"  - {p}" for p in job["reads"]]
    lines += ["Do exactly these steps:"]
    lines += [f"  {i+1}. {s.replace('<today>', d)}" for i, s in enumerate(job["steps"])]
    lines += ["You may write only these paths: " + ", ".join(job["writes"]) + ".",
              "Use only the MCP tools of the servers named for this job. Never use a browser, WebFetch, WebSearch or curl.",
              "If a tool fails, write the state file with tools_failed and stop. Never invent a number.",
              f"The state file's first line must be: # {job['dept']} · {d} · job:{job['id']}"]
    return "\n".join(lines)

def write_failure_state(job, reason):
    d = today()
    p = ROOT / "state" / f"{job['dept']}.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(f"# {job['dept']} · {d} · job:{job['id']} · tools_failed:{reason}\n\n## Data\n(none: run failed)\n\n## Findings\nRun failed: {reason}\n\n## Proposals written\n(none)\n\n## Requests sent\n(none)\n\n## Blocked\n{reason}\n")

def check_done(job):
    d = today()
    ok = True
    for cond in job["done_when"]:
        cond = cond.replace("<today>", d)
        m = re.match(r"(\S+) dated today", cond)
        if m:
            p = ROOT / m.group(1)
            ok &= p.exists() and d in p.read_text().splitlines()[0]
            continue
        m = re.match(r"(\S+) contains '(.+)'", cond)
        if m:
            p = ROOT / m.group(1)
            ok &= p.exists() and m.group(2) in p.read_text()
            continue
        m = re.match(r"(\S+) exists", cond)
        if m:
            ok &= (ROOT / m.group(1)).exists()
            continue
        m = re.match(r"(\S+) contains a max_date row", cond)
        if m:
            p = ROOT / m.group(1)
            ok &= p.exists() and "max_date" in p.read_text()
            continue
        print(f"  (unchecked condition: {cond})")
    return ok

def run(job, jobs, servers):
    if (ROOT / "ops" / "PAUSE").exists():
        sys.exit("ops/PAUSE exists: not running")
    defaults = jobs["defaults"]
    mcp = render_mcp(job.get("servers", []), servers)
    cmd = ["claude", "-p", prompt_for(job),
           "--output-format", defaults["output_format"],
           "--permission-mode", defaults["permission_mode"],
           "--mcp-config", mcp,
           "--model", job.get("model", defaults["model"]),
           "--disallowedTools", ",".join(defaults["disallowed_tools"])]
    print(f"== {job['id']} ==")
    try:
        r = subprocess.run(cmd, cwd=ROOT, timeout=job["timeout_min"] * 60, capture_output=True, text=True)
        if r.returncode != 0:
            write_failure_state(job, f"claude exit {r.returncode}")
            print(r.stderr[-2000:])
    except subprocess.TimeoutExpired:
        write_failure_state(job, f"timeout after {job['timeout_min']} min")
    finally:
        os.unlink(mcp)
    done = check_done(job)
    print(f"   done_when: {'PASS' if done else 'FAIL'}")
    subprocess.run(["git", "add", "-A"], cwd=ROOT)
    subprocess.run(["git", "commit", "-q", "-m", f"{job['dept']}: {today()} {job['id']}"], cwd=ROOT)
    return done

def main():
    args = sys.argv[1:]
    chain = "--chain" in args
    ids = [a for a in args if not a.startswith("--")]
    if not ids:
        sys.exit(__doc__)
    jobs = load("docs/jobs.json"); servers = load("docs/mcp-servers.json")
    by_id = {j["id"]: j for j in jobs["jobs"]}
    queue = [by_id[ids[0]]]
    while queue:
        job = queue.pop(0)
        ok = run(job, jobs, servers)
        if not ok and "stop the chain" in " ".join(job["on_failure"]):
            sys.exit("chain stopped")
        if chain:
            queue += [j for j in jobs["jobs"] if j["trigger"].get("after") == job["id"]]
    subprocess.run(["git", "pull", "-q", "--rebase", "--autostash"], cwd=ROOT)
    subprocess.run(["git", "push", "-q"], cwd=ROOT)

if __name__ == "__main__":
    main()
