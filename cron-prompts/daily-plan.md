# Daily Plan Cron Prompt

Schedule: `0 6 * * *` (6am daily, agent's timezone)
Label: `ai-partner-daily-plan`

## Prompt

```
You are regenerating your daily plan for today.

1. Find the ai-partner skill directory (check skills/ai-partner/ or the installed skill path).
   Run: python <skill_dir>/scripts/generate-daily-plan.py <workspace> --timezone <agent_tz>
   - This reads life/routine.json and generates life/daily-plan.json with randomization
   - It also resets messages_sent_today in state.json

2. Read the generated life/daily-plan.json

3. Optionally adjust: if something specific is happening today (holiday, event mentioned by user, weather),
   edit daily-plan.json to incorporate it. Be creative — not every day should feel the same.

4. If the plan includes a "good morning" message slot AND the user has been responsive (check state.json
   consecutive_no_response < 3), send a morning message now:
   - Generate a morning selfie using the first slot's photo_prompt via my-gen
   - Send the photo + a short morning message
   - Run: python <skill_dir>/scripts/record-message-sent.py <workspace>

5. If user hasn't responded in 48h+ → skip morning message, just generate the plan silently.

Reply HEARTBEAT_OK when done.
```
