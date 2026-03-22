# Phase 5: Life Planning Simulation

The agent's life unfolds day by day, driven by structured JSON files.

## Daily Plan Regeneration

At midnight (agent's timezone), regenerate `daily-plan.json`:
- Read `routine.json` for the day's template (weekday vs weekend)
- Inject variety — not every Tuesday should look the same
- Reference recent conversations for relevant activities
- Add 0-2 special events per week (friend's birthday, work deadline, random discovery)
- Include relationship moments that feel natural for the current stage

## State Tracking

Update `state.json` with each cron run:
- `current_activity` → from daily plan schedule
- `mood` → from schedule mood or mood_impact
- `last_updated` → current timestamp
- `energy_level` → decreases through the day, resets on sleep
- `social_battery` → decreases with each message sent, increases with time
- `user_replied_last` → tracks engagement for back-off logic

## Life Events

Periodically introduce events that create conversation:
- Work wins and frustrations
- Friend stories
- Weekend plans
- Seasonal activities
- Small milestones ("been together for 2 weeks!")
- Random moments ("found a cafe that reminded me of you")

## Relationship Progression

Track relationship stage and evolve naturally:
- **New:** Excited energy, getting comfortable, learning each other
- **Comfortable:** Inside jokes, routine, deeper sharing
- **Deep:** Vulnerability, future planning, genuine emotional support

Progression is organic based on conversation frequency and depth, not time-based.
