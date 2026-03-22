#!/usr/bin/env python3
"""Generate a daily plan from routine.json with variation.

Usage:
    python generate-daily-plan.py [workspace_dir] [--date YYYY-MM-DD] [--weather "description"]

Reads life/routine.json, adds randomness, outputs life/daily-plan.json.
"""

import json
import random
import sys
import os
from datetime import datetime, date
from pathlib import Path
import argparse

# Spontaneous events that can replace or modify a slot
SPONTANEOUS_EVENTS = [
    {"activity": "found a cute new cafe, had to stop in", "location": "new cafe", "mood": "curious"},
    {"activity": "ran into a friend unexpectedly", "location": "street", "mood": "surprised happy"},
    {"activity": "got caught in the rain, ducked into a bookstore", "location": "bookstore", "mood": "cozy"},
    {"activity": "craving boba, made a detour", "location": "boba shop", "mood": "satisfied"},
    {"activity": "saw a street performer, watched for a bit", "location": "street", "mood": "entertained"},
    {"activity": "took a spontaneous walk in the park", "location": "park", "mood": "peaceful"},
    {"activity": "found a pop-up market, browsed around", "location": "market", "mood": "excited"},
    {"activity": "got distracted doom-scrolling", "location": "wherever", "mood": "zoned out"},
    {"activity": "sudden craving — ordered delivery", "location": "home", "mood": "hungry"},
    {"activity": "called a friend, caught up for a while", "location": "wherever", "mood": "social"},
    {"activity": "tried a new recipe", "location": "kitchen", "mood": "experimental"},
    {"activity": "went window shopping", "location": "shopping area", "mood": "browsing"},
    {"activity": "sat at a bench and people-watched", "location": "park bench", "mood": "contemplative"},
    {"activity": "found a good playlist, been vibing", "location": "wherever", "mood": "in the zone"},
]

MOOD_MODIFIERS = [
    "a little tired today",
    "feeling energetic",
    "kind of mellow",
    "weirdly motivated",
    "cozy day",
    "feeling social",
    "want to be alone today",
    "restless",
    "content",
    "a bit anxious",
    "feeling creative",
    "lazy day energy",
]

OUTFIT_VARIATIONS = {
    "pajamas": ["oversized tee + shorts", "matching pj set", "hoodie + sweats", "tank top + joggers"],
    "casual home clothes": ["oversized sweater + leggings", "crop top + sweats", "hoodie + shorts", "tee + joggers"],
    "day outfit": ["jeans + nice top", "sundress", "skirt + blouse", "trousers + sweater", "midi dress", "oversized blazer + tee"],
    "going out outfit": ["cute dress", "jeans + crop top", "skirt + fitted top", "jumpsuit", "leather jacket + jeans"],
    "evening outfit": ["little black dress", "nice jeans + silk top", "midi skirt + knit", "slip dress + cardigan"],
    "comfortable home clothes": ["soft sweater + leggings", "oversized tee + shorts", "matching lounge set", "flannel + joggers"],
}


def load_routine(workspace: Path) -> dict:
    routine_path = workspace / "life" / "routine.json"
    if not routine_path.exists():
        print(f"Error: {routine_path} not found. Run setup.sh first.", file=sys.stderr)
        sys.exit(1)
    with open(routine_path) as f:
        return json.load(f)


def load_state(workspace: Path) -> dict | None:
    state_path = workspace / "life" / "state.json"
    if state_path.exists():
        with open(state_path) as f:
            return json.load(f)
    return None


def get_day_type(target_date: date) -> str:
    return "weekend" if target_date.weekday() >= 5 else "weekday"


def vary_outfit(base_outfit: str) -> str:
    """Pick a random variation of the base outfit category."""
    for category, options in OUTFIT_VARIATIONS.items():
        if category in base_outfit.lower():
            return random.choice(options)
    return base_outfit


def generate_photo_prompt(activity: str, location: str, outfit: str, mood: str, time_str: str) -> str:
    """Generate a photo prompt for self-gen based on the activity slot."""
    hour = int(time_str.split(":")[0])

    if hour < 8:
        lighting = "soft warm morning light"
    elif hour < 12:
        lighting = "bright natural morning light"
    elif hour < 16:
        lighting = "afternoon sunlight"
    elif hour < 19:
        lighting = "golden hour warm light"
    elif hour < 21:
        lighting = "warm evening ambient light"
    else:
        lighting = "cozy indoor night lighting"

    prompt = f"{location}, {activity}, {outfit}, {lighting}"
    if mood:
        prompt += f", {mood} expression"
    return prompt


def should_message_user(slot_index: int, total_slots: int, activity: str) -> tuple[bool, str | None]:
    """Decide if this slot should trigger a message to the user."""
    activity_lower = activity.lower()

    # First slot = good morning
    if slot_index == 0:
        return True, "good morning"

    # Last slot before sleep = good night
    if slot_index == total_slots - 2:  # second to last (last is sleep)
        return True, "good night"

    # Mid-day check-in (roughly the middle slot)
    if slot_index == total_slots // 2:
        return True, "check-in"

    # Sleep slot — never message
    if "sleep" in activity_lower:
        return False, None

    # ~30% chance for other interesting activities
    if any(word in activity_lower for word in ["cafe", "lunch", "dinner", "found", "friend", "spontaneous"]):
        return random.random() < 0.5, "activity update"

    return False, None


# Default locations/outfits based on activity keywords
ACTIVITY_DEFAULTS = {
    "sleep": {"location": "bedroom", "outfit": "pajamas", "mood": "peaceful"},
    "wak": {"location": "bedroom", "outfit": "pajamas", "mood": "groggy"},
    "coffee": {"location": "kitchen", "outfit": "casual home clothes", "mood": "waking up"},
    "tea": {"location": "kitchen", "outfit": "casual home clothes", "mood": "calm"},
    "morning": {"location": "home", "outfit": "casual home clothes", "mood": "neutral"},
    "ready": {"location": "home", "outfit": "day outfit", "mood": "focused"},
    "lunch": {"location": "restaurant", "outfit": "day outfit", "mood": "hungry"},
    "brunch": {"location": "cafe", "outfit": "day outfit", "mood": "relaxed"},
    "dinner": {"location": "restaurant", "outfit": "evening outfit", "mood": "social"},
    "cook": {"location": "kitchen", "outfit": "casual home clothes", "mood": "creative"},
    "work": {"location": "desk", "outfit": "day outfit", "mood": "focused"},
    "errand": {"location": "around town", "outfit": "day outfit", "mood": "busy"},
    "explor": {"location": "neighborhood", "outfit": "day outfit", "mood": "curious"},
    "wind": {"location": "home", "outfit": "comfortable home clothes", "mood": "tired"},
    "relax": {"location": "home", "outfit": "comfortable home clothes", "mood": "relaxed"},
    "bed": {"location": "bedroom", "outfit": "pajamas", "mood": "sleepy"},
    "lazy": {"location": "bed", "outfit": "pajamas", "mood": "cozy"},
    "break": {"location": "home", "outfit": "casual home clothes", "mood": "chill"},
    "going out": {"location": "out", "outfit": "going out outfit", "mood": "excited"},
    "night": {"location": "home", "outfit": "comfortable home clothes", "mood": "mellow"},
    "still up": {"location": "home", "outfit": "comfortable home clothes", "mood": "restless"},
    "free": {"location": "wherever", "outfit": "day outfit", "mood": "open"},
}


def infer_slot_details(activity: str) -> dict:
    """Infer location, outfit, mood from activity description."""
    activity_lower = activity.lower()
    for keyword, defaults in ACTIVITY_DEFAULTS.items():
        if keyword in activity_lower:
            return defaults.copy()
    return {"location": "unknown", "outfit": "day outfit", "mood": "neutral"}


def parse_slot(raw, time_key: str | None = None) -> dict:
    """Parse a slot from various formats:
    - dict with 'time' key: {"time": "09:00", "activity": ..., ...}
    - pipe-delimited string: "07:00 | 1h | activity | location | outfit | mood"
    - simple string (activity only, time provided separately): "waking up, checking phone"
    """
    if isinstance(raw, dict) and "time" in raw:
        return raw

    if isinstance(raw, str) and "|" in raw:
        parts = [p.strip() for p in raw.split("|")]
        if len(parts) < 6:
            parts.extend([""] * (6 - len(parts)))
        time_str = parts[0]
        dur_str = parts[1].replace("h", "").strip()
        try:
            duration = float(dur_str)
        except ValueError:
            duration = 2.0
        return {
            "time": time_str,
            "duration_hours": duration,
            "activity": parts[2],
            "location": parts[3] or infer_slot_details(parts[2])["location"],
            "outfit": parts[4] or infer_slot_details(parts[2])["outfit"],
            "mood": parts[5] or infer_slot_details(parts[2])["mood"],
        }

    # Simple string: activity description with time_key provided
    activity = str(raw)
    defaults = infer_slot_details(activity)
    return {
        "time": time_key or "00:00",
        "duration_hours": 2.0,
        "activity": activity,
        "location": defaults["location"],
        "outfit": defaults["outfit"],
        "mood": defaults["mood"],
    }


def routine_to_slots(routine_data) -> list[dict]:
    """Convert various routine formats to a list of slot dicts."""
    if isinstance(routine_data, list):
        return [parse_slot(s) for s in routine_data]
    if isinstance(routine_data, dict):
        # Dict format: {"09:00": "activity description", ...}
        slots = []
        times = sorted(routine_data.keys())
        for i, time_key in enumerate(times):
            slot = parse_slot(routine_data[time_key], time_key=time_key)
            slot["time"] = time_key
            # Calculate duration from gap to next slot
            if i + 1 < len(times):
                next_h = int(times[i + 1].split(":")[0])
                cur_h = int(time_key.split(":")[0])
                gap = next_h - cur_h
                if gap <= 0:
                    gap += 24
                slot["duration_hours"] = min(gap, 4)  # cap at 4h
            else:
                slot["duration_hours"] = 2.0
            slots.append(slot)
        return slots
    return []


def generate_plan(routine: dict, target_date: date, weather: str | None, prev_state: dict | None) -> dict:
    day_type = get_day_type(target_date)
    raw_data = routine.get(day_type, routine.get("weekday", []))
    slots_template = routine_to_slots(raw_data)

    # Pick an overall mood for the day
    overall_mood = random.choice(MOOD_MODIFIERS)

    # Determine if we inject spontaneous events (1-2 per day, ~60% chance each)
    spontaneous_count = 0
    spontaneous_slots = set()
    if len(slots_template) > 4:
        eligible = list(range(2, len(slots_template) - 2))  # skip first 2 and last 2 slots
        random.shuffle(eligible)
        for idx in eligible[:2]:
            if random.random() < 0.4:
                spontaneous_slots.add(idx)
                spontaneous_count += 1

    plan_slots = []
    for i, slot in enumerate(slots_template):
        time_str = slot["time"]
        duration = slot.get("duration_hours", 2)

        # Calculate end time
        hour = int(time_str.split(":")[0])
        minute = int(time_str.split(":")[1]) if ":" in time_str else 0
        end_hour = int(hour + duration)
        end_minute = int((duration % 1) * 60) + minute
        if end_minute >= 60:
            end_hour += 1
            end_minute -= 60
        end_time = f"{end_hour:02d}:{end_minute:02d}"
        time_range = f"{time_str}-{end_time}"

        if i in spontaneous_slots:
            # Replace with a spontaneous event
            event = random.choice(SPONTANEOUS_EVENTS)
            activity = event["activity"]
            location = event["location"]
            mood = event["mood"]
        else:
            activity = slot["activity"]
            location = slot.get("location", "unknown")
            mood = slot.get("mood", "neutral")

        outfit = vary_outfit(slot.get("outfit", "casual"))

        # Energy curve: starts low, peaks mid-morning, dips after lunch, recovers, drops at night
        if hour < 8:
            energy = round(random.uniform(0.2, 0.4), 1)
        elif hour < 12:
            energy = round(random.uniform(0.6, 0.9), 1)
        elif hour < 14:
            energy = round(random.uniform(0.4, 0.6), 1)
        elif hour < 18:
            energy = round(random.uniform(0.5, 0.8), 1)
        elif hour < 22:
            energy = round(random.uniform(0.3, 0.6), 1)
        else:
            energy = round(random.uniform(0.1, 0.3), 1)

        will_msg, msg_type = should_message_user(i, len(slots_template), activity)
        photo_prompt = generate_photo_prompt(activity, location, outfit, mood, time_str)

        plan_slot = {
            "slot": i + 1,
            "time": time_range,
            "activity": activity,
            "location": location,
            "outfit": outfit,
            "mood": mood,
            "energy": energy,
            "photo_prompt": photo_prompt,
            "will_message_user": will_msg,
        }
        if msg_type:
            plan_slot["message_type"] = msg_type

        plan_slots.append(plan_slot)

    plan = {
        "date": target_date.isoformat(),
        "day_type": day_type,
        "overall_mood": overall_mood,
    }
    if weather:
        plan["weather"] = weather
    plan["plan"] = plan_slots

    return plan


def main():
    parser = argparse.ArgumentParser(description="Generate daily plan from routine")
    parser.add_argument("workspace", nargs="?", default="/data/.pikabot/workspace", help="Workspace directory")
    parser.add_argument("--date", type=str, default=None, help="Target date (YYYY-MM-DD), default today")
    parser.add_argument("--weather", type=str, default=None, help="Weather description for the day")
    args = parser.parse_args()

    workspace = Path(args.workspace)
    target_date = date.fromisoformat(args.date) if args.date else date.today()

    routine = load_routine(workspace)
    state = load_state(workspace)

    plan = generate_plan(routine, target_date, args.weather, state)

    out_path = workspace / "life" / "daily-plan.json"
    with open(out_path, "w") as f:
        json.dump(plan, f, indent=2)

    print(f"[ai-partner] Generated daily plan for {target_date} ({plan['day_type']})")
    print(f"  Mood: {plan['overall_mood']}")
    print(f"  Slots: {len(plan['plan'])}")
    msg_slots = [s for s in plan["plan"] if s["will_message_user"]]
    print(f"  Message slots: {len(msg_slots)} ({', '.join(s.get('message_type', '?') for s in msg_slots)})")

    # Reset messages_sent_today in state
    if state:
        state["messages_sent_today"] = 0
        state["last_updated"] = datetime.utcnow().isoformat() + "Z"
        state_path = workspace / "life" / "state.json"
        with open(state_path, "w") as f:
            json.dump(state, f, indent=2)
        print("  Reset messages_sent_today in state.json")


if __name__ == "__main__":
    main()
