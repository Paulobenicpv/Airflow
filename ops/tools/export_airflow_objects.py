#!/usr/bin/env python

import json, subprocess, sys

def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(r.stderr)
    return r.stdout.strip()

def list_variables():
    out = run("airflow variables list --output json")
    return json.loads(out)

def list_connections():
    out = run("airflow connections list --output json")
    return json.loads(out)

def main():
    vars_ = list_variables()
    conns = list_connections()
    print(json.dumps({"variables": vars_, "connections": conns}, indent=2))

if __name__ == "__main__":
    main()