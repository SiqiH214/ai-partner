# Prerequisites Check

This skill works on **any agent platform** — Pika, OpenClaw, or standalone. The pre-flight check detects what's available and guides setup for anything missing.

## Capabilities Needed

| Capability | What For | Required? |
|---|---|---|
| **Image generation** | Daily photos, scene generation | Yes |
| **Voice cloning** | Clone partner voice from audio sample | Recommended |
| **TTS (text-to-speech)** | Generate voice notes | Recommended |

## Pre-Flight Check

When the skill activates, detect the agent's platform and available APIs:

```
1. Check platform:
   a. PIKA_API_BASE_URL + PIKA_AGENT_API_KEY exist → Pika agent (all capabilities built in)
   b. GEMINI_API_KEY exists → standalone/OpenClaw agent (partial setup)
   c. Neither → needs full manual setup

2. For each missing capability, guide the user through setup (see below)
```

## Platform A: Pika Agents

Everything is built in via Pika Proxy — no additional API keys needed.

| Capability | Powered By |
|---|---|
| Image generation | Gemini / nano-banana-pro via Pika Proxy |
| Voice cloning + TTS | MiniMax via Pika Proxy |

→ Skip straight to onboarding. Don't mention APIs.

## Platform B: OpenClaw / Standalone Agents

These agents need their own API keys. Detect what's available and guide through missing ones.

### 1. Image Generation (required)

| Provider | Env Var | How to Get |
|---|---|---|
| **Gemini** (recommended) | `GEMINI_API_KEY` | [ai.google.dev](https://ai.google.dev) → Get API Key. Free tier: 15 req/min. |

**Gemini setup guide:**
```
1. Go to ai.google.dev
2. Click "Get API Key" → Create key in new project
3. Copy the key
4. Save it:
   - Pika: write to .secrets/gemini-api-key
   - OpenClaw: add to .env as GEMINI_API_KEY=your_key
   - Standalone: export GEMINI_API_KEY=your_key
```

### 2. Voice Cloning + TTS (recommended)

| Provider | Env Var | How to Get |
|---|---|---|
| **MiniMax** (recommended) | `MINIMAX_API_KEY` | [minimax.chat](https://www.minimax.chat) → Sign up → API Keys. Free tier available. |

**MiniMax setup guide:**
```
1. Go to minimax.chat
2. Sign up (free)
3. Go to API Keys section
4. Create and copy your key
5. Save it:
   - Pika: write to .secrets/minimax-api-key
   - OpenClaw: add to .env as MINIMAX_API_KEY=your_key
   - Standalone: export MINIMAX_API_KEY=your_key
```

**If user skips voice:** All voice features disabled. Text-only mode — still works fine.

## How to Guide the User

Keep it casual. Check as you go:

**Pika agent:** Skip straight to onboarding.

**OpenClaw/standalone — missing image gen:**
> "quick thing — i need image generation to send you photos of my day. grab a free Gemini API key from ai.google.dev. takes 2 minutes."

**OpenClaw/standalone — missing voice:**
> "want me to send you voice notes? i'll need a MiniMax API key — it's free. or we can do text-only."

**Everything ready:** Don't mention APIs. Start the fun part.
