#!/usr/bin/env bash
# setup.sh — Install ai-partner skill into the agent's workspace
# Usage: bash scripts/setup.sh [workspace_dir]

set -euo pipefail

WORKSPACE="${1:-/data/.pikabot/workspace}"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "[ai-partner] Installing into $WORKSPACE"

# Create life directory
mkdir -p "$WORKSPACE/life"

# Copy routine template if no routine exists yet
if [ ! -f "$WORKSPACE/life/routine.json" ]; then
  cp "$SKILL_DIR/templates/life-routine.json.template" "$WORKSPACE/life/routine.json"
  echo "[ai-partner] Created life/routine.json from template"
else
  echo "[ai-partner] life/routine.json already exists, skipping"
fi

# Initialize state.json if it doesn't exist
if [ ! -f "$WORKSPACE/life/state.json" ]; then
  cat > "$WORKSPACE/life/state.json" << 'EOF'
{
  "current_slot": null,
  "current_activity": "just set up",
  "location": "home",
  "mood": "excited",
  "energy": 0.8,
  "outfit": null,
  "last_meal": null,
  "with": null,
  "thinking_about": null,
  "last_updated": null,
  "last_user_contact": null,
  "messages_sent_today": 0,
  "consecutive_no_response": 0
}
EOF
  echo "[ai-partner] Created life/state.json"
else
  echo "[ai-partner] life/state.json already exists, skipping"
fi

# Create today-plan.md placeholder
if [ ! -f "$WORKSPACE/life/today-plan.md" ]; then
  echo "# Today's Plan\n\n_Not yet generated. Run generate-daily-plan.py to create._" > "$WORKSPACE/life/today-plan.md"
  echo "[ai-partner] Created life/today-plan.md placeholder"
fi

echo "[ai-partner] Setup complete. Next steps:"
echo "  1. Customize life/routine.json for the agent's personality"
echo "  2. Run: python $SKILL_DIR/scripts/generate-daily-plan.py $WORKSPACE"
echo "  3. Run: bash $SKILL_DIR/scripts/install-crons.sh"
