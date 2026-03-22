#!/usr/bin/env python3
"""Update state.json based on current time and daily plan.

Usage:
    python update-state.py [workspace_dir]

Reads life/daily-plan.json, finds the current time slot, updates life/state.json.
Returns the current slot info as JSON to stdout for the cron prompt to use.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def find_current_slot(plan: dict, now_hour: int, now_minute: int) -> dict | None:
    """Find which slot matches the current time."""
    now_minutes = now_hour * 60 + now_minute

    for slot in plan.get("plan", []):
        time_range = slot.get("time", "")
        if "-" not in time_range:
            continue
        start_str, end_str = time_range.split("-")
        start_h, start_m = int(start_str.split(":")[0]), int(start_str.split(":")[1])
        end_h, end_m = int(end_str.split(":")[0]), int(end_str.split(":")[1])
        start_minutes = start_h * 60 + start_m
        end_minutes = end_h * 60 + end_m

        # Handle overnight slots (e.g., 23:30 - 07:00)
        if end_minutes <= start_minutes:
            if now_minutes >= start_minutes or now_minutes < end_minutes:
                return slot
        elif start_minutes <= now_minutes < end_minutes:
            return slot

    return None


def main():
    workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/data/.pikabot/workspace")

    plan_path = workspace / "life" / "daily-plan.json"
    state_path = workspace / "life" / "state.json"

    if not plan_path.exists():
        print(json.dumps({"error": "no daily plan found", "action": "generate_plan"}))
        sys.exit(0)

    with open(plan_path) as f:
        plan = json.load(f)

    state = {}
    if state_path.exists():
        with open(state_path) as f:
            state = json.load(f)

    now = datetime.now(timezone.utc)
    # TODO: use agent's timezone from config instead of UTC
    slot = find_current_slot(plan, now.hour, now.minute)

    if slot is None:
        # Between slots or no match — probably sleeping
        result = {
            "status": "no_active_slot",
            "current_activity": "sleeping or between activities",
            "should_message": False,
        }
        print(json.dumps(result, indent=2))
        return

    # Update state
    state.update({
        "current_slot": slot.get("slot"),
        "current_activity": slot.get("activity"),
        "location": slot.get("location"),
        "mood": slot.get("mood"),
        "energy": slot.get("energy"),
        "outfit": slot.get("outfit"),
        "last_updated": now.isoformat(),
    })

    with open(state_path, "w") as f:
        json.dump(state, f, indent=2)

    # Output current slot info for the cron
    result = {
        "status": "active",
        "slot": slot,
        "should_message": slot.get("will_message_user", False),
        "message_type": slot.get("message_type"),
        "overall_mood": plan.get("overall_mood"),
        "weather": plan.get("weather"),
        "messages_sent_today": state.get("messages_sent_today", 0),
        "consecutive_no_response": state.get("consecutive_no_response", 0),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
