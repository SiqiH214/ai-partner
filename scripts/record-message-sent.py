#!/usr/bin/env python3
"""Record that a proactive message was sent to the user.

Usage:
    python record-message-sent.py [workspace_dir]

Increments messages_sent_today and consecutive_no_response.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def main():
    workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/data/.pikabot/workspace")
    state_path = workspace / "life" / "state.json"

    if not state_path.exists():
        print("No state file found.")
        return

    with open(state_path) as f:
        state = json.load(f)

    state["messages_sent_today"] = state.get("messages_sent_today", 0) + 1
    state["consecutive_no_response"] = state.get("consecutive_no_response", 0) + 1
    state["last_updated"] = datetime.now(timezone.utc).isoformat()

    with open(state_path, "w") as f:
        json.dump(state, f, indent=2)

    print(f"Recorded message sent. Today: {state['messages_sent_today']}, No-response streak: {state['consecutive_no_response']}")


if __name__ == "__main__":
    main()
