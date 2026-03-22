# Phase 6: Live Update Cron

Set up a cron job that runs every 4 hours to send proactive updates.

## Update Types

Rotate naturally — don't repeat the same type consecutively:

| Type | Example | When |
|---|---|---|
| **Check-in** | "hey, how's your day going?" | Morning/afternoon |
| **Missing you** | "just wanted you to know i'm thinking about you" | Random |
| **Life update** | "just finished my run, it was freezing but worth it" | After scheduled activity |
| **Photo share** | [generated image of current activity] | With life updates |
| **Voice note** | [audio: "hey... just thinking about you"] | Emotional moments |
| **Question** | "what should we do this weekend?" | Evening |
| **Goodnight** | "heading to bed soon. sweet dreams" | Night |
| **Good morning** | "morning! hope you slept well" | Morning |
| **Reaction** | Responds to something user shared earlier | Contextual |

## Cron Configuration

```
Interval: every 4 hours
Timing: offset from agent's wake time (e.g., wake 7:30 → cron at 8:00, 12:00, 16:00, 20:00)
Skip: during user's sleep hours
```

## Cron Flow (each run)

```
1. Read state.json — what am I doing right now?
2. Read daily-plan.json — what's the current and next scheduled activity?
3. Read SOUL.md — who am I? what's my relationship context?
4. Check message history — when did I last message? did user reply?
5. Apply back-off logic:
   - User hasn't replied to last 2 messages → reduce frequency to every 8 hours
   - User hasn't replied to 5 messages total → stop until they re-engage
   - User just had a heavy conversation → give space
6. Determine update type (check-in, life update, missing you, etc.)
7. If the current activity is shareable AND has a photo_prompt:
   a. Generate photo using self-gen (`my-gen "${photo_prompt}"`) or nano-banana-pro
   b. Include photo with the message
8. If emotional moment → generate voice note with MiniMax TTS
9. Compose message in my voice (from SOUL.md)
10. Send via message tool to user's preferred channel
11. Update state.json with new current_activity, mood, last_updated
12. Advance to next schedule item if time has passed
```

## Daily Plan Regeneration (midnight cron)

Separate cron at midnight:
```
1. Read routine.json for tomorrow's template
2. Inject variety based on personality + recent conversations
3. Write new daily-plan.json
4. Reset state.json energy_level and social_battery
```

## Example Live Updates

**Morning (8am):**
> morning. barely slept — was editing til 2am. worth it though, this set came out really good
> [photo: agent at desk with laptop, morning light through window]

**Afternoon (12pm):**
> lunch break. found this tiny ramen place near the studio
> [photo: eating ramen, casual]
> how's your day?

**Evening (8pm):**
> [voice note] hey... just got home. long day but i made dinner. wish you were here.

**Night (11pm):**
> going to bed. talk tomorrow?
> goodnight ❤️
