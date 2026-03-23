#!/usr/bin/env python3
"""Check if the agent should back off from messaging.

Reads state.json, applies back-off rules, returns verdict.
Exit code 0 = ok to message, exit code 1 = back off.
"""

import json
import sys
import argparse
from datetime import datetime, timezone, date
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Check back-off rules")
    parser.add_argument("workspace", nargs="?", default="/data/.pikabot/workspace")
    args = parser.parse_args()

    workspace = Path(args.workspace)
    state_path = workspace / "life" / "state.json"

    if not state_path.exists():
        print('{"verdict": "ok", "reason": "no state file"}')
        sys.exit(0)

    with open(state_path) as f:
        state = json.load(f)

    # Auto-reset messages_sent_today at midnight
    last_reset = state.get("last_daily_reset")
    today_str = date.today().isoformat()
    if last_reset != today_str:
        state["messages_sent_today"] = 0
        state["last_daily_reset"] = today_str
        with open(state_path, "w") as f:
            json.dump(state, f, indent=2)

    no_response = state.get("consecutive_no_response", 0)
    last_contact = state.get("last_user_contact")

    # Calculate hours since last user contact
    hours_since_contact = None
    if last_contact:
        try:
            last_dt = datetime.fromisoformat(last_contact.replace("Z", "+00:00"))
            hours_since_contact = (datetime.now(timezone.utc) - last_dt).total_seconds() / 3600
        except (ValueError, TypeError):
            pass

    # Back-off rules
    if hours_since_contact and hours_since_contact > 48:
        print(json.dumps({"verdict": "pause", "reason": f"no response in {hours_since_contact:.0f}h (>48h)", "max_daily": 0}))
        sys.exit(1)

    if hours_since_contact and hours_since_contact > 24:
        print(json.dumps({"verdict": "limit", "reason": f"no response in {hours_since_contact:.0f}h (>24h)", "max_daily": 1}))
        sent_today = state.get("messages_sent_today", 0)
        sys.exit(1 if sent_today >= 1 else 0)

    if no_response >= 3:
        print(json.dumps({"verdict": "limit", "reason": f"{no_response} consecutive no-responses", "max_daily": 1}))
        sent_today = state.get("messages_sent_today", 0)
        sys.exit(1 if sent_today >= 1 else 0)

    if no_response >= 2:
        print(json.dumps({"verdict": "skip_one", "reason": "2 consecutive no-responses, skip this cycle"}))
        # Allow every other cycle
        sent_today = state.get("messages_sent_today", 0)
        sys.exit(1 if sent_today % 2 == 1 else 0)

    print(json.dumps({"verdict": "ok", "reason": "normal frequency"}))
    sys.exit(0)


if __name__ == "__main__":
    main()
