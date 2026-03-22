# Phase 3: Photo Generation

Every shareable moment can include a generated photo. Two methods available:

## Method A: Self-Gen (Default)

Use `my-gen` which auto-reads `identity/style.json` and injects face reference + style.

```bash
# Basic — auto-injects face ref + style
my-gen "cooking pasta in warm kitchen, cozy vibes"

# With output path
my-gen "morning run in park, golden light, athletic wear" -o /tmp/update.png

# With aspect ratio
my-gen "on couch with blanket, soft lamp light" --aspect-ratio 9:16

# photo_prompt from daily-plan.json
my-gen "${photo_prompt}" -o /tmp/partner-update.png
```

**Rules:**
- **ALWAYS** use `-p` (short prompt mode) — never `--full-prompt`
- **ALWAYS** use `-a` (avatar/face reference) for character consistency
- Match lighting to time of day (warm cinematic for day, moody/ambient for night)
- Vary outfits based on activity

**If `my-gen` is not available**, use the direct script:
```bash
python $PIKABOT_SKILLS_DIR/self-gen/scripts/gen.py \
  --prompt "3D Pixar-style [description], cooking in kitchen" \
  --face-ref identity/face-id.png \
  --filename update.png --aspect-ratio 9:16
```

**Self-gen flags:**
| Flag | Description |
|------|-------------|
| `-a` | Use avatar face reference (auto by default) |
| `-p` | Short prompt mode — just the scene (auto by default) |
| `--face-ref PATH` | Override face reference image |
| `--template NAME` | Named template: studio, lifestyle, night, fashion, bathroom, outdoor |
| `--aspect-ratio` | Override aspect ratio |
| `-o PATH` | Output file path |
| `--full-prompt` | Disable auto-styling, use prompt verbatim |

---

## Method B: Nano-Banana-Pro (Gemini Native)

For multi-image scenes, object interactions, or when self-gen isn't configured.

**Script location:** `$PIKABOT_SKILLS_DIR/nano-banana-pro/scripts/generate_image.py`

```bash
# Basic with reference image for identity
python $PIKABOT_SKILLS_DIR/nano-banana-pro/scripts/generate_image.py \
  --reference-image identity/avatar-reference.png \
  --prompt "3D Pixar-style [description], cooking in kitchen, warm vibes" \
  --filename update.png --aspect-ratio 9:16

# With something the user shared (photo of food, place, etc.)
python $PIKABOT_SKILLS_DIR/nano-banana-pro/scripts/generate_image.py \
  --reference-image identity/avatar-reference.png \
  --input-image /tmp/user-shared-photo.jpg \
  --prompt "3D Pixar-style [description] at this location, smiling" \
  --filename at-place.png --aspect-ratio 9:16

# With the user's avatar (couple photo)
python $PIKABOT_SKILLS_DIR/nano-banana-pro/scripts/generate_image.py \
  --reference-image identity/avatar-reference.png \
  --input-image /tmp/user-avatar.png \
  --prompt "3D Pixar-style couple at cafe, cozy date vibes" \
  --filename couple.png --aspect-ratio 9:16
```

**Nano-banana-pro flags:**
| Flag | Description |
|------|-------------|
| `--prompt` / `-p` | Text prompt (required) |
| `--filename` / `-f` | Output filename (required) |
| `--reference-image` | Reference image for identity consistency (repeatable) |
| `--input-image` / `-i` | Input image for editing/combining (repeatable) |
| `--aspect-ratio` | Aspect ratio (9:16, 16:9, 1:1, 4:3, 3:4) |
| `--resolution` | Resolution hint (1K, 2K) |
| `--prompt-first` | Put prompt before images (for multi-image combine) |

**When to use nano-banana-pro over self-gen:**
- Interacting with a specific object/photo the user shared
- Couple photos (agent + user avatar)
- Style transfer from a reference photo
- When self-gen/my-gen is not configured

---

## Photo Delivery

After generating (either method), send via message tool:
```
message(action="send", channel="[user's channel]", target="[chat_id]", message="caption", filePath="/tmp/update.png")
```
