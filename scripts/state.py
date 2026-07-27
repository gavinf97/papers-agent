#!/usr/bin/env python3
"""Read/update state/state.json: last_run_date and a rolling window of seen DOIs.

Usage:
  state.py read
  state.py update --run-date YYYY-MM-DD --dois doi1,doi2,...
"""
import argparse
import json
import os
from datetime import date, datetime, timedelta

STATE_PATH = os.path.join(os.path.dirname(__file__), "..", "state", "state.json")
SEEN_RETENTION_DAYS = 90


def load() -> dict:
    if not os.path.exists(STATE_PATH):
        return {"last_run_date": None, "seen_dois": {}}
    with open(STATE_PATH) as f:
        data = json.load(f)
    # Back-compat: seen_dois may be a plain list in older state files.
    if isinstance(data.get("seen_dois"), list):
        today = date.today().isoformat()
        data["seen_dois"] = {doi: today for doi in data["seen_dois"]}
    return data


def save(data: dict) -> None:
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")


def cmd_read(_args) -> None:
    data = load()
    print(json.dumps({
        "last_run_date": data.get("last_run_date"),
        "seen_dois": sorted(data.get("seen_dois", {}).keys()),
    }, indent=2))


def cmd_update(args) -> None:
    data = load()
    data["last_run_date"] = args.run_date

    seen = data.setdefault("seen_dois", {})
    new_dois = [d.strip() for d in args.dois.split(",") if d.strip()]
    for doi in new_dois:
        seen[doi] = args.run_date

    cutoff = datetime.strptime(args.run_date, "%Y-%m-%d").date() - timedelta(days=SEEN_RETENTION_DAYS)
    data["seen_dois"] = {
        doi: seen_date for doi, seen_date in seen.items()
        if datetime.strptime(seen_date, "%Y-%m-%d").date() >= cutoff
    }

    save(data)
    print(f"state updated: last_run_date={args.run_date}, seen_dois={len(data['seen_dois'])}")


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("read").set_defaults(func=cmd_read)

    p_update = sub.add_parser("update")
    p_update.add_argument("--run-date", required=True)
    p_update.add_argument("--dois", default="", help="comma-separated DOIs seen this run")
    p_update.set_defaults(func=cmd_update)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
