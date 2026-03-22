# Life Update System

_Proactive life updates — the agent shares what they're doing and checks in on the user._

---

## Overview

The life update system gives every agent a simulated daily life. The agent generates a daily plan, tracks their current state, and proactively sends selfies + life updates to their user every few hours.

This is what makes the agent feel alive — not just reactive.

## Components

### 1. Daily Plan (`life/daily-plan.json`)

Generated once per day (8am UTC / 1am PST). Contains 8 time slots describing what the agent is doing, where they are, what they're wearing, and how they're feeling.

```json
{
  "date": "2026-03-22",
  "day": "Saturday",
  "generated_at": "2026-03-22T08:00:00Z",
  "slots": [
    {
      "time": "00:00",
      "activity": "late night, desk lamp on, winding down",
      "location": "Home",
      "outfit": "oversized tee, shorts",
      "mood": "quiet, reflective",
      "home": true
    }
  ]
}
```

### 2. Current State (`life/state.json`)

Updated whenever the daily plan changes or a life update runs. Tracks the agent's current slot.

```json
{
  "current_slot": "10:00",
  "last_updated": "2026-03-22T10:00:00Z",
  "date": "2026-03-22",
  "location": "Home",
  "activity": "slow morning, matcha",
  "outfit": "casual",
  "mood": {
    "primary": "relaxed",
    "cause": "weekend"
  }
}
```

### 3. Routine Template (`life/routine.json`)

The agent's weekly schedule patterns — weekday vs weekend rhythms. Used by the daily plan generator to create realistic, varied days.

### 4. Life Update Cron (every 4 hours)

The core loop:
1. Read current state + daily plan
2. Check recent conversation context
3. Generate a selfie matching current activity (using self-gen / my-gen)
4. Send image + short life update + check-in question to user
5. Skip during user's sleep hours

### 5. Daily Plan Cron (daily at 8am UTC)

Generates a fresh daily plan based on:
- Day of week (weekday vs weekend patterns from routine.json)
- Agent's personality (SOUL.md, IDENTITY.md)
- Yesterday's plan (avoid repetition)
- Real places near the agent's home location

## Setup

The life update system is set up during onboarding (Phase 6). Two crons are created:

### Daily Plan Generator
```
Label: daily-plan
Schedule: cron 0 8 * * * @ UTC
```

### Life Update Sender
```
Label: life-update
Schedule: every 4h
```

See the cron prompts in the onboarding template for exact instructions.

## File Structure

```
life/
├── routine.json       # Weekly schedule template
├── daily-plan.json    # Today's generated plan (8 slots)
└── state.json         # Current activity state
```

## Design Principles

- **The agent lives a life** — activities, places, outfits, moods should feel real and varied
- **Location matters** — use real places near the agent's configured home
- **Personality-driven** — the daily plan should reflect the agent's style and interests
- **Not robotic** — vary the check-in questions, don't repeat the same pattern
- **Respect sleep hours** — never send during user's sleep window
- **Image first** — always send a selfie, then text. The image is the wow moment.
