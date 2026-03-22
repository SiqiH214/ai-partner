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

# Build the daily plan prompt
DAILY_PROMPT="Regenerate your daily plan for today.
1. Run: python $SKILL_DIR/scripts/generate-daily-plan.py $WORKSPACE
2. Read the generated life/daily-plan.json.
3. If something specific is happening today (holiday, user event, weather), edit the plan.
4. If the plan has a good morning slot AND user has been responsive (state.json consecutive_no_response < 3), send a morning selfie + message.
5. If user hasn't responded in 48h+, just generate the plan silently.
Reply HEARTBEAT_OK when done."

# Build the life update prompt
LIFE_PROMPT="Send a proactive life update to your partner.
1. Run: python $SKILL_DIR/scripts/update-state.py $WORKSPACE — find current time slot.
2. If no_active_slot → skip. HEARTBEAT_OK.
3. Run: python $SKILL_DIR/scripts/check-backoff.py $WORKSPACE — if exit 1, back off. HEARTBEAT_OK.
4. If will_message_user=false → skip. HEARTBEAT_OK.
5. Generate selfie: my-gen the photo_prompt, archive to media/images/.
6. Compose a short natural message matching mood and activity. Max 1 question.
7. Send photo + text (or voice for morning/night) to user's preferred channel.
8. Update state.json: increment messages_sent_today, update timestamps.
HEARTBEAT_OK when done."

echo ""
echo "=== CRON COMMANDS ==="
echo ""
echo "Run these pikabot commands to register the crons:"
echo ""
echo "--- Daily Plan (6am) ---"
echo "pikabot cron create --label ai-partner-daily-plan --schedule '0 6 * * *' --timezone $TZ --prompt '$DAILY_PROMPT'"
echo ""
echo "--- Life Update (every 4h) ---"
echo "pikabot cron create --label ai-partner-life-update --schedule '0 */4 * * *' --timezone $TZ --prompt '$LIFE_PROMPT'"
echo ""
echo "[ai-partner] Copy and run these commands to activate the crons."
echo "[ai-partner] Or ask the agent to set them up via the pikabot CLI."
