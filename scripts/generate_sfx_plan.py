import re
import json
import os
from datetime import datetime

# SRT content from the user provided file
srt_content = """
1
00:00:00,183 --> 00:00:00,883
<b>ผมบักอ่ะ</b>

2
00:00:01,316 --> 00:00:02,316
<b>จริงจังมาเนี่ย</b>

3
00:00:02,883 --> 00:00:03,299
<b>ผมบัก</b>

4
00:00:03,299 --> 00:00:03,850
<b>ผมบักเข้ามา</b>

5
00:00:03,850 --> 00:00:04,566
<b>ในห้องเลยอ่ะ</b>

6
00:00:04,683 --> 00:00:04,983
<b>ในห้องเลยอ่ะทุกคน</b>

7
00:00:05,816 --> 00:00:06,583
<b>ชิบคายแล้ว</b>

8
00:00:07,083 --> 00:00:08,533
<b>ผมบักเข้ามาในห้องเลยอ่ะ</b>

9
00:00:09,333 --> 00:00:11,683
<b>เอ็กซิสอรีเต็มเลยอ่ะ</b>

10
00:00:12,216 --> 00:00:13,133
<b>ผมโดนขังห้องเลย</b>

11
00:00:13,599 --> 00:00:15,216
<b>ใช่ลง ลงไปในเร็วโฮชิ</b>

12
00:00:15,266 --> 00:00:16,516
<b>ถ้าเจอแสงสีแดง</b>
<b>ให้เดินไปเลย</b>

13
00:00:16,566 --> 00:00:17,383
<b>มันจะไปที่ทำพิธี</b>

14
00:00:17,566 --> 00:00:19,366
<b>ผมบักเข้ามาในห้องอ่ะ</b>

15
00:00:19,633 --> 00:00:21,216
<b>ลงมาทาง</b>

16
00:00:21,366 --> 00:00:22,516
<b>คุณโอโมริอยู่ไหน</b>

17
00:00:22,516 --> 00:00:23,500
<b>เดินไปล่างๆนี้ไหม</b>

18
00:00:23,666 --> 00:00:24,183
<b>เผื่อเจอกะโหลก</b>

19
00:00:24,366 --> 00:00:25,483
<b>ผมมาอยู่อะไรกับใครนี้</b>
"""

SFX_DIR = "C:\\Users\\warit\\Desktop\\davinci-katy-mcp\\SFX"

# Define SFX categories and family mappings (simplified from LLM_WIKI/Wiki/core/data-models.md and adding-sfx skill)
SFX_FAMILY_MAP = {
    "comedy": ["pop", "blip", "plink", "honk", "marimba", "awkward"],
    "reaction": ["awkward", "huh", "awww"],
    "impact": ["impact", "scream", "glass", "pop"],
    "emphasis": ["ding", "pop", "collect"],
    "fail": ["wrong", "scratch", "bleep"],
    "transition": ["whoosh", "rise"],
    "success": ["collect", "kaching", "ding", "sparkle"],
    "dramatic": ["rise", "gong", "metal", "glitch"],
    "action": ["impact", "whoosh", "explosion", "stomp"],
    "ui": ["click", "digital", "keyboard"],
}

# Reverse map for easy lookup: sfx_file -> family
SFX_FILE_TO_FAMILY = {}
for family, files in SFX_FAMILY_MAP.items():
    for f in files:
        SFX_FILE_TO_FAMILY[f] = family

class EventType:
    JOKE = "joke"
    REACTION = "reaction"
    SURPRISE = "surprise"
    EMPHASIS = "emphasis"
    FAIL = "fail"
    TRANSITION = "transition"
    SUCCESS = "success"
    DRAMATIC = "dramatic"
    ACTION = "action"
    UI_NOTIFICATION = "ui_notification"
    INTRO = "intro"
    OUTRO = "outro"

class ContentFormat:
    TALKING_HEAD = "talking_head"
    PODCAST = "podcast"
    GAME = "game"
    MEME = "meme"
    LIVESTREAM = "livestream"

class SubtitleCue:
    def __init__(self, index, start_time, end_time, text):
        self.index = index
        self.start_time = self.parse_time_to_seconds(start_time)
        self.end_time = self.parse_time_to_seconds(end_time)
        self.text = text.replace('<b>', '').replace('</b>', '').strip()

    def parse_time_to_seconds(self, time_str):
        h, m, s_ms = time_str.split(':')
        s, ms = s_ms.split(',')
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

    @property
    def duration(self):
        return self.end_time - self.start_time

def parse_srt(srt_content):
    cues = []
    blocks = srt_content.strip().split('\n\n')
    for block in blocks:
        lines = block.split('\n')
        if len(lines) >= 3:
            index = int(lines[0])
            time_str = lines[1]
            text = ' '.join(lines[2:]).strip()
            start_time, end_time = time_str.split(' --> ')
            cues.append(SubtitleCue(index, start_time, end_time, text))
    return cues

def get_available_sfx_files(sfx_dir):
    available_files = []
    for root, _, files in os.walk(sfx_dir):
        for f in files:
            if f.endswith((".mp3", ".wav")):
                file_basename = os.path.splitext(f)[0].lower() # filename without extension, lowercased
                # Try to map to a family based on substrings, simplified
                assigned_family = "other"
                for family_name, keywords in SFX_FAMILY_MAP.items():
                    for keyword in keywords:
                        if keyword in file_basename:
                            assigned_family = family_name
                            break
                    if assigned_family != "other":
                        break
                available_files.append({
                    "filename": f,
                    "basename": os.path.splitext(f)[0],
                    "family": assigned_family,
                    "path": os.path.join(root, f) # Full path might not be needed for plan, but useful for context
                })
    return available_files

class BeatPoint:
    def __init__(self, timestamp, event_type, impact_score, description, sfx_family=None, sfx_file=None):
        self.timestamp = timestamp
        self.event_type = event_type
        self.impact_score = impact_score
        self.description = description
        self.sfx_family = sfx_family
        self.sfx_file = sfx_file

    def to_dict(self):
        return {
            "timestamp_seconds": self.timestamp,
            "event_type": self.event_type,
            "impact_score": self.impact_score,
            "description": self.description,
            "sfx_family": self.sfx_family,
            "sfx_file": self.sfx_file
        }

def round2_beat_harvesting(cues):
    candidates = []
    for i, cue in enumerate(cues):
        text = cue.text.lower()

        # Rule-based detection (simplified for this example)
        # JOKE/PUNCHLINE
        if "บัก" in text or "จริงจัง" in text or "ชิบคาย" in text or "กะโหลก" in text or "ใครนี้" in text:
            candidates.append(BeatPoint(cue.start_time, EventType.JOKE, 0.8, f"Punchline/Joke: '{cue.text}'", sfx_family="comedy"))
        
        # REACTION
        if "เต็มเลย" in text or "โดนขัง" in text:
            candidates.append(BeatPoint(cue.start_time, EventType.REACTION, 0.7, f"Reaction: '{cue.text}'", sfx_family="reaction"))

        # EMPHASIS
        if "แสงสีแดง" in text or "ทำพิธี" in text or "ห้อง" in text:
            candidates.append(BeatPoint(cue.start_time, EventType.EMPHASIS, 0.6, f"Emphasis: '{cue.text}'", sfx_family="emphasis"))

    return candidates

def round3_curation_selection(candidates, duration_seconds, sfx_files, content_format=ContentFormat.TALKING_HEAD):
    final_placements = []
    warnings = []
    
    # Sort by impact score (descending)
    candidates.sort(key=lambda x: x.impact_score, reverse=True)

    # Format-specific rules
    if content_format == ContentFormat.TALKING_HEAD:
        max_sfx_per_minute = 5 # Max 5 SFX/min for talking head
        min_spacing = 1.0 # Min 1 second spacing
    else:
        max_sfx_per_minute = 10 # Placeholder for other formats
        min_spacing = 0.5

    # Filter 1: Density Check
    density_cap = int((duration_seconds / 60) * max_sfx_per_minute)
    if len(candidates) > density_cap:
        warnings.append(f"Too many candidates ({len(candidates)}) for density cap ({density_cap}). Trimming.")
        candidates = candidates[:density_cap]
    
    # Filter 2 & 3: Spacing and Family Variety
    placed_timestamps = []
    placed_families = {}

    for beat in candidates:
        # Find best matching SFX file
        best_sfx_file = None
        for sfx_f in sfx_files:
            if sfx_f["family"] == beat.sfx_family:
                # Prioritize processed files if available, or just take first match
                best_sfx_file = sfx_f["filename"]
                break
        
        if not best_sfx_file:
            warnings.append(f"No matching SFX file found for family '{beat.sfx_family}' for beat at {beat.timestamp:.2f}s")
            continue

        # Spacing check
        can_place = True
        for placed_ts in placed_timestamps:
            if abs(beat.timestamp - placed_ts) < min_spacing:
                can_place = False
                warnings.append(f"SFX at {beat.timestamp:.2f}s is too close to another SFX at {placed_ts:.2f}s. Skipping {beat.description}")
                break
        
        if not can_place:
            continue

        # Family Variety Check (simple: avoid same family too close)
        # More robust check needed for production, this is a basic one
        if beat.sfx_family in placed_families:
            last_placed_time_for_family = placed_families[beat.sfx_family]
            if (beat.timestamp - last_placed_time_for_family) < (min_spacing * 2): # Avoid same family within 2x min_spacing
                warnings.append(f"Skipping SFX at {beat.timestamp:.2f}s due to recent placement of same family ('{beat.sfx_family}').")
                continue

        beat.sfx_file = best_sfx_file # Assign the chosen SFX file
        final_placements.append(beat)
        placed_timestamps.append(beat.timestamp)
        placed_families[beat.sfx_family] = beat.timestamp

    return final_placements, warnings

# --- Main Workflow ---

# Step 0: Setup
cues = parse_srt(srt_content)
duration_seconds = cues[-1].end_time if cues else 0
content_format = ContentFormat.TALKING_HEAD # Assuming talking-head for this content
available_sfx_files = get_available_sfx_files(SFX_DIR)

# Round 1: Structural Scan (Implicit for this short script)
# Duration and format are set.

# Round 2: Beat Harvesting
beat_candidates = round2_beat_harvesting(cues)

# Round 3: Curation & Selection
final_beats, curation_warnings = round3_curation_selection(beat_candidates, duration_seconds, available_sfx_files, content_format)

# Finalize: Create plan JSON
sfx_placements = []
for beat in final_beats:
    sfx_placements.append({
        "sfx_file": beat.sfx_file,
        "timestamp_seconds": round(beat.timestamp, 3),
        "duration": 0.5, # Default sting duration
        "reason": beat.description # Use beat description as reason
    })

plan_json = {
    "timeline_name": "Auto SFX Placement",
    "sfx": sfx_placements,
    "format": content_format,
    "timeline_duration_seconds": round(duration_seconds, 3),
    "fps": 60.0,
    "density_per_minute": round(len(sfx_placements) / (duration_seconds / 60) if duration_seconds > 0 else 0, 2),
    "warnings": curation_warnings
}

# Save plan to a JSON file
plan_path = "C:\\Users\\warit\\Desktop\\davinci-katy-mcp\\scripts\\plan.json"
with open(plan_path, 'w', encoding='utf-8') as f:
    json.dump(plan_json, f, indent=2, ensure_ascii=False)

print(f"SFX plan generated at: {plan_path}")
print(json.dumps(plan_json, indent=2, ensure_ascii=False))