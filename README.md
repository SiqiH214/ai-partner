# AI Partner Building

Transform an existing agent into the user's AI partner — boyfriend, girlfriend, pet, best friend, or any close companion. The agent reshapes its own identity, builds a life simulation, and sends proactive daily updates with photos and voice notes.

## What It Does

Takes an **existing agent** (who already has an avatar, voice, and personality) and transforms it into the user's partner through a conversational onboarding. The agent asks "who am I to you?" and rewrites its own identity files based on the answers.

## How It Works

1. **Onboarding** — Agent asks the user about itself: "what's my name?", "who am I to you?", "where do I live?", "what's my personality?"
2. **File Updates** — Agent rewrites its own SOUL.md, IDENTITY.md, style.json based on answers
3. **Life Sim** — Generates routine.json + daily-plan.json with shareable moments and mood arcs
4. **Live Updates** — Sets up 4-hour cron that sends contextual messages, photos (self-gen/nano-banana-pro), and voice notes (MiniMax TTS)

## End Result

After onboarding, the agent:
- Has an updated SOUL.md with new personality and relationship context
- Has a structured daily routine (routine.json)
- Generates a fresh daily plan each day (daily-plan.json)
- Sends proactive updates every 4 hours with photos and voice notes
- Tracks its own state (mood, activity, energy, location)
- Deepens the relationship over time through conversation

## Technical Stack

| Component | Skill |
|---|---|
| Agent photos (default) | `self-gen` via `my-gen` CLI |
| Agent photos (advanced) | `nano-banana-pro` — multi-image scenes |
| Face reference cleanup | `id-normalize` |
| Voice cloning + TTS | `minimax-voice` |
| Scene interactions | `moment-gen`, `ref-copy` |
| Emotional support | `emotional-healing` |

## Prerequisites

Works on **any agent platform** — Pika, OpenClaw, or standalone.

| Capability | Pika Agents | OpenClaw / Standalone |
|---|---|---|
| Image generation | Built in (Pika Proxy) | Gemini API key (free) |
| Voice cloning + TTS | Built in (Pika Proxy) | MiniMax API key (free) |

The skill auto-detects the platform and guides through any missing setup.

## Example

```
Agent: so... who am I to you?
User: my boyfriend
Agent: boyfriend. i like that. what's my name?
User: keep it
Agent: what am I like?
User: quiet but warm. you open up when it's just us
Agent: the short-texts-but-means-a-lot type. got it.
[rewrites SOUL.md, sets up routine, starts cron]
...
[4 hours later]
Agent: just got back from a shoot. this light was insane
Agent: [photo of agent at golden hour, camera in hand]
Agent: how's your day going?
...
[that night]
Agent: [voice note] hey... heading to bed. today was long but talking to you made it better.
```

## Safety

- Partner role must be 18+
- Respects user-defined boundaries
- Encourages real-world connection if unhealthy attachment patterns emerge
- Follows platform content policies
- Integrates with emotional-healing skill for mental health support

## License

MIT
