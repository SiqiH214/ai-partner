#!/usr/bin/env bash
# install-crons.sh — Register ai-partner crons with pikabot
# Usage: bash scripts/install-crons.sh [agent_timezone]
#
# This creates two crons:
#   1. ai-partner-daily-plan — regenerates daily plan at 6am
#   2. ai-partner-life-update — sends proactive updates every 4 hours

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
WORKSPACE="${PIKABOT_WORKSPACE:-/data/.pikabot/workspace}"
TZ="${1:-America/Los_Angeles}"

echo "[ai-partner] Installing crons (timezone: $TZ)"
echo "[ai-partner] Skill dir: $SKILL_DIR"
echo "[ai-partner] Workspace: $WORKSPACE"

cat <<EOF

=== CRON COMMANDS ===

Run these pikabot commands to register the crons:

--- Daily Plan (6am) ---
pikabot cron create --label ai-partner-daily-plan --schedule '0 6 * * *' --timezone $TZ --prompt 'Regenerate your daily plan for today.
1. Run: python $SKILL_DIR/scripts/generate-daily-plan.py $WORKSPACE --timezone $TZ
2. Read the generated life/daily-plan.json.
3. If something specific is happening today, adjust the plan.
4. If good morning slot AND consecutive_no_response < 3, send morning selfie + message. Then run: python $SKILL_DIR/scripts/record-message-sent.py $WORKSPACE
5. If no response in 48h+ → skip morning message, just generate silently.
Reply HEARTBEAT_OK when done.'

--- Life Update (every 4h) ---
pikabot cron create --label ai-partner-life-update --schedule '0 */4 * * *' --timezone $TZ --prompt 'Send a proactive life update.
1. Run: python $SKILL_DIR/scripts/update-state.py $WORKSPACE --timezone $TZ
2. If no_active_slot → HEARTBEAT_OK.
3. Run: python $SKILL_DIR/scripts/check-backoff.py $WORKSPACE — if exit 1, HEARTBEAT_OK.
4. If will_message_user=false → HEARTBEAT_OK.
5. Generate selfie via my-gen with photo_prompt, archive to media/images/.
6. Send photo + short message matching mood. Then run: python $SKILL_DIR/scripts/record-message-sent.py $WORKSPACE
Reply HEARTBEAT_OK when done.'

[ai-partner] Copy and run these commands to activate the crons.
EOF
