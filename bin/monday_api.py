"""Tiny monday GraphQL client. Stdlib only. Token from MONDAY_API_TOKEN. Never prints the token."""
import json, os, sys, urllib.request

API = "https://api.monday.com/v2"

def gql(query, variables=None):
    token = os.environ.get("MONDAY_API_TOKEN")
    if not token:
        sys.exit("MONDAY_API_TOKEN is not set (source ~/.anabtawi/env)")
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(API, data=body, headers={"Authorization": token, "Content-Type": "application/json", "API-Version": "2025-01"})
    with urllib.request.urlopen(req, timeout=60) as r:
        out = json.loads(r.read())
    if out.get("errors"):
        raise RuntimeError(json.dumps(out["errors"])[:800])
    return out["data"]

def me():
    return gql("query { me { id name } }")["me"]
