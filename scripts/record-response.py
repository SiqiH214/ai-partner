#!/usr/bin/env python3
"""Record that the user responded — resets back-off counters.

Usage:
    python record-response.py [workspace_dir]

Call this when the user sends a message to the agent.
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

    state["consecutive_no_response"] = 0
    state["last_user_contact"] = datetime.now(timezone.utc).isoformat()

    with open(state_path, "w") as f:
        json.dump(state, f, indent=2)

    print("Recorded user response. Back-off counters reset.")


if __name__ == "__main__":
    main()
