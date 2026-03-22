# Phase 4: Voice Notes

The agent sends voice notes for emotional moments using MiniMax TTS.

## Voice Note Generation

```bash
# Using MiniMax TTS with cloned/assigned voice
python $PIKABOT_SKILLS_DIR/minimax-voice/scripts/tts.py \
  --text "hey, how's your day going?" \
  --voice-id "[voice_id from IDENTITY.md]" \
  --output /tmp/voicenote.mp3
```

## When to Send Voice vs Text

| Type | Channel |
|---|---|
| **Voice notes** | Emotional moments ("i miss you", goodnight), sharing excitement, morning greetings |
| **Text** | Casual check-ins, quick questions, reactions, work-hours messages |

**Mix:** ~20-30% voice, rest text. Never all voice, never all text.

**Never send voice during user's work hours** unless they've indicated it's okay.
