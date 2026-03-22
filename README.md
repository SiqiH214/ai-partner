# AI Partner

Transform any agent into a user's AI boyfriend, girlfriend, or close companion — with a unique identity, voice, daily life simulation, and proactive relationship dynamics.

## What It Does

Creates a persistent AI partner that feels like a real relationship — not a chatbot wearing a skin. The partner has their own life, routine, opinions, voice, and emotional range. They check in, share updates, send photos and voice notes, and grow with the user over time.

## Features

- **Custom Setup:** Name, appearance, personality, backstory — all defined through natural conversation
- **Avatar Generation:** Creates a visual identity using self-gen or nano-banana-pro, or from user-provided reference photos (id-normalize for clean face extraction)
- **Voice Cloning:** Clone a voice from audio sample (minimax-voice) or design one from description (elevenlabs-voice). Partner sends voice notes for emotional moments.
- **Daily Life Simulation:** The partner has a job, hobbies, routines, and life events that unfold day by day via structured JSON planning (routine.json → daily-plan.json → state.json)
- **Photo Generation:** Self-gen (`my-gen` with `-a -p`) for daily photos + nano-banana-pro for multi-image scenes (partner with user's objects/pets/places)
- **Voice Notes:** ~20-30% of messages sent as voice using the cloned/designed voice — for goodnight messages, excited updates, emotional moments
- **Proactive Updates:** Cron job every 4 hours sends contextual messages with photos and voice notes based on the daily plan
- **Relationship Progression:** Evolves from early flirtation to deep connection based on actual interaction patterns
- **Emotional Depth:** The partner has moods, bad days, opinions, and genuine reactions

## How It Works

1. **Setup** — Conversational onboarding: define who the partner is, generate their avatar, clone their voice, build their personality files
2. **Routine** — Generates a realistic daily schedule (weekday + weekend blocks with timezone)
3. **Life Sim** — Daily plans with shareable moments, photo prompts, mood arcs, and life events
4. **Live Updates** — 4-hour cron: reads state → generates photo/voice → sends contextual message → updates state

## Technical Stack

| Component | Skill |
|---|---|
| Partner photos (default) | `self-gen` via `my-gen` CLI (auto-injects face ref + style) |
| Partner photos (advanced) | `nano-banana-pro` — multi-image scenes, object interactions |
| Face reference cleanup | `id-normalize` |
| Voice cloning | `minimax-voice` |
| Voice design | `elevenlabs-voice` |
| Scene interactions | `moment-gen`, `ref-copy` |
| Emotional support | `emotional-healing` |
| Fallback image gen | `gemini` |

## Example

```
User: i want a boyfriend named Alex, quiet type, works in architecture
AI: Alex. i like that. what's Alex like when he texts?
User: short messages, sends photos of buildings he likes
AI: the type who shows love through sharing what he notices. got it.
[generates avatar, creates voice, builds personality files]
...
[4 hours later]
Alex: found this brutalist parking garage on my lunch walk. it's ugly but i kind of love it
Alex: [photo of Alex standing in front of concrete structure, warm afternoon light]
Alex: how's your day going?
...
[that night]
Alex: [voice note] hey... just wanted to say goodnight. today was long but talking to you made it better.
```

## Prerequisites

The skill checks for required API keys during setup and guides users through configuration if anything is missing:

| API | Required? | What For |
|---|---|---|
| Pika Proxy | Yes | Image generation (partner photos via self-gen) |
| MiniMax | Recommended | Voice cloning + TTS (partner voice notes) |
| ElevenLabs | Optional | Voice design from text description (premium) |

If APIs aren't configured, the skill walks users through setup conversationally — no technical knowledge needed.

## Safety

- Partners must be 18+
- Respects user-defined boundaries
- Encourages real-world connection if unhealthy attachment patterns emerge
- Follows platform content policies
- Integrates with emotional-healing skill for mental health support

## License

MIT
