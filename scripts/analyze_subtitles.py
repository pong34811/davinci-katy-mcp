#!/usr/bin/env python3
"""Read and analyze subtitle track 1 from DaVinci Resolve.

Usage:
    python scripts/analyze_subtitles.py --action read [--output subtitles.json]
    python scripts/analyze_subtitles.py --action analyze [--input subtitles.json]
    python scripts/analyze_subtitles.py --action both [--output subtitles.json]
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
MCP_DIR = os.path.join(REPO_ROOT, "davinci-resolve-mcp")
for _p in (REPO_ROOT, MCP_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# ── Emotion/Beat Keywords ───────────────────────────────────────────────────

EMOTION_KEYWORDS = {
    "surprise": {
        "th": ["มาจากไหน", "ตกใจ", "โอ้โห", "ไม่น่าเชื่อ", "เซอร์ไพรส์", "ทำไม", "จริงหรอ", "เฮ้ย"],
        "en": ["wow", "omg", "surprise", "really", "no way", "holy", "what"],
    },
    "excitement": {
        "th": ["เย้", "สุดยอด", "เจ๋ง", "เทพ", "โคตร", "เริ่ด", "ปัง", "ยินดี"],
        "en": ["yay", "awesome", "amazing", "great", "cool", "love", "best"],
    },
    "success": {
        "th": ["สำเร็จ", "ได้แล้ว", "ชนะ", "ผ่าน", "ถูกต้อง", "เยี่ยม", "สมหวัง"],
        "en": ["success", "win", "pass", "correct", "done", "complete"],
    },
    "fail": {
        "th": ["ล้มเหลว", "ผิด", "ไม่ได้", "พัง", "เจ๊ง", "พลาด", "ตาย"],
        "en": ["fail", "wrong", "lose", "die", "dead", "broken", "error"],
    },
    "emphasis": {
        "th": ["ตัวเลข", "สถิติ", "จำนวน", "เปอร์เซ็นต์", "ล้าน", "พัน", "ร้อย", "บาท"],
        "en": ["first", "second", "third", "most", "only", "every", "always", "never"],
    },
    "question": {
        "th": ["ทำไม", "ยังไง", "อะไร", "ที่ไหน", "เมื่อไหร่", "ใคร"],
        "en": ["why", "how", "what", "where", "when", "who"],
    },
    "transition": {
        "th": ["ต่อไป", "แล้วก็", "นอกจากนี้", "มาดู", "ไปดู", "สำหรับ"],
        "en": ["next", "then", "also", "now", "let's", "moving on"],
    },
    "closing": {
        "th": ["ลาก่อน", "บาย", "เจอกัน", "ขอบคุณ", "ฝากกด", "ติดตาม"],
        "en": ["bye", "see you", "thanks", "subscribe", "follow", "end"],
    },
}

# ── Subtitle Reader ─────────────────────────────────────────────────────────

def read_subtitles_from_resolve() -> List[Dict[str, Any]]:
    """Read subtitle track 1 from the current DaVinci Resolve timeline."""
    try:
        from src.utils.platform import get_resolve_paths
        paths = get_resolve_paths()
        os.environ.setdefault("RESOLVE_SCRIPT_API", paths["api_path"])
        os.environ.setdefault("RESOLVE_SCRIPT_LIB", paths["lib_path"])
        modules = paths["modules_path"]
        if modules not in sys.path:
            sys.path.append(modules)

        import DaVinciResolveScript as dvr
        resolve = dvr.scriptapp("Resolve")
        if resolve is None:
            print("ERROR: Cannot connect to Resolve. Is it running?", file=sys.stderr)
            return []

        project = resolve.GetProjectManager().GetCurrentProject()
        if project is None:
            print("ERROR: No project open.", file=sys.stderr)
            return []

        timeline = project.GetCurrentTimeline()
        if timeline is None:
            print("ERROR: No timeline open.", file=sys.stderr)
            return []

        fps = float(timeline.GetSetting("timelineFrameRate") or 30.0)
        subs = timeline.GetItemListInTrack("subtitle", 1)
        if not subs:
            print("WARNING: No subtitles found in track 1.", file=sys.stderr)
            return []

        subs.sort(key=lambda x: x.GetStart())
        result = []
        for i, s in enumerate(subs):
            start_frame = s.GetStart()
            end_frame = s.GetEnd()
            text = s.GetName() or ""
            result.append({
                "index": i + 1,
                "start_frame": start_frame,
                "end_frame": end_frame,
                "start_seconds": round(start_frame / fps, 3),
                "end_seconds": round(end_frame / fps, 3),
                "duration_seconds": round((end_frame - start_frame) / fps, 3),
                "text": text.strip(),
                "fps": fps,
            })

        print(f"Read {len(result)} subtitles from track 1 (fps={fps})")
        return result

    except ImportError:
        print("ERROR: Cannot import DaVinciResolveScript.", file=sys.stderr)
        return []
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return []


def read_subtitles_from_srt(path: str) -> List[Dict[str, Any]]:
    """Parse an SRT file into subtitle entries."""
    if not os.path.isfile(path):
        print(f"ERROR: File not found: {path}", file=sys.stderr)
        return []

    with open(path, "r", encoding="utf-8-sig") as f:
        content = f.read()

    entries = []
    blocks = re.split(r"\n\s*\n", content.strip())
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue
        try:
            index = int(lines[0].strip())
        except ValueError:
            continue
        time_match = re.match(
            r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2})[,.](\d{3})",
            lines[1].strip(),
        )
        if not time_match:
            continue
        g = [int(x) for x in time_match.groups()]
        start = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        end = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        text = " ".join(lines[2:]).strip()
        entries.append({
            "index": index,
            "start_seconds": round(start, 3),
            "end_seconds": round(end, 3),
            "duration_seconds": round(end - start, 3),
            "text": text,
        })

    print(f"Parsed {len(entries)} subtitles from {path}")
    return entries


# ── Subtitle Analyzer ───────────────────────────────────────────────────────

def detect_emotion(text: str) -> List[str]:
    """Detect emotions from subtitle text using keyword matching."""
    text_lower = text.lower()
    detected = []
    for emotion, keywords in EMOTION_KEYWORDS.items():
        for lang_keywords in keywords.values():
            for kw in lang_keywords:
                if kw.lower() in text_lower:
                    detected.append(emotion)
                    break
            if emotion in detected:
                break
    return detected if detected else ["neutral"]


def detect_numbers(text: str) -> List[str]:
    """Extract numbers from text (for emphasis detection)."""
    numbers = re.findall(r"[\d,]+\.?\d*", text)
    return [n.replace(",", "") for n in numbers]


def analyze_subtitles(subtitles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Analyze each subtitle for emotions, beats, and SFX opportunities."""
    beats = []
    for sub in subtitles:
        text = sub["text"]
        emotions = detect_emotion(text)
        numbers = detect_numbers(text)

        # Determine beat type
        beat_type = "neutral"
        sfx_suggestion = None
        priority = 0  # 0=low, 1=medium, 2=high

        if "surprise" in emotions:
            beat_type = "surprise"
            sfx_suggestion = "pop"
            priority = 2
        elif "excitement" in emotions:
            beat_type = "excitement"
            sfx_suggestion = "sparkle"
            priority = 2
        elif "success" in emotions:
            beat_type = "success"
            sfx_suggestion = "collect"
            priority = 2
        elif "fail" in emotions:
            beat_type = "fail"
            sfx_suggestion = "wrong"
            priority = 2
        elif "emphasis" in emotions or numbers:
            beat_type = "emphasis"
            sfx_suggestion = "ding"
            priority = 1
        elif "question" in emotions:
            beat_type = "question"
            sfx_suggestion = "pop"
            priority = 1
        elif "transition" in emotions:
            beat_type = "transition"
            sfx_suggestion = "whoosh-clean"
            priority = 1
        elif "closing" in emotions:
            beat_type = "closing"
            sfx_suggestion = "sparkle"
            priority = 1

        beats.append({
            **sub,
            "emotions": emotions,
            "beat_type": beat_type,
            "sfx_suggestion": sfx_suggestion,
            "priority": priority,
            "numbers": numbers,
        })

    return beats


def format_beats_table(beats: List[Dict[str, Any]]) -> str:
    """Format beats as a readable table."""
    lines = [
        f"{'#':>3} | {'Start':>8} | {'End':>8} | {'Dur':>5} | {'Beat':<12} | {'SFX':<16} | {'Text':<30}",
        "-" * 100,
    ]
    for b in beats:
        start = f"{b['start_seconds']:.2f}s"
        end = f"{b['end_seconds']:.2f}s"
        dur = f"{b['duration_seconds']:.1f}s"
        text = b["text"][:30] + ("..." if len(b["text"]) > 30 else "")
        lines.append(
            f"{b['index']:>3} | {start:>8} | {end:>8} | {dur:>5} | {b['beat_type']:<12} | "
            f"{(b['sfx_suggestion'] or ''):<16} | {text}"
        )
    return "\n".join(lines)


# ── Main ────────────────────────────────────────────────────────────────────

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Read and analyze subtitle track 1 from DaVinci Resolve."
    )
    parser.add_argument(
        "--action",
        choices=["read", "analyze", "both"],
        default="both",
        help="read = read subtitles, analyze = analyze beats, both = do both",
    )
    parser.add_argument(
        "--input",
        help="path to SRT file or JSON subtitle file (for analyze action)",
    )
    parser.add_argument(
        "--output",
        default="subtitles.json",
        help="output JSON path (default: subtitles.json)",
    )
    args = parser.parse_args(argv)

    subtitles = []
    beats = []

    if args.action in ("read", "both"):
        if args.input and args.input.endswith(".srt"):
            subtitles = read_subtitles_from_srt(args.input)
        elif args.input and args.input.endswith(".json"):
            with open(args.input, "r", encoding="utf-8") as f:
                subtitles = json.load(f)
        else:
            subtitles = read_subtitles_from_resolve()

        if subtitles:
            out_path = args.output
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(subtitles, f, ensure_ascii=False, indent=2)
            print(f"Saved {len(subtitles)} subtitles to {out_path}")

    if args.action in ("analyze", "both"):
        if not subtitles and args.input:
            if args.input.endswith(".json"):
                with open(args.input, "r", encoding="utf-8") as f:
                    subtitles = json.load(f)
            elif args.input.endswith(".srt"):
                subtitles = read_subtitles_from_srt(args.input)

        if not subtitles:
            print("ERROR: No subtitles to analyze. Run 'read' first or provide --input.", file=sys.stderr)
            return 1

        beats = analyze_subtitles(subtitles)
        print(f"\n=== Beat Analysis ({len(beats)} segments) ===\n")
        print(format_beats_table(beats))

        # Save beats
        beats_path = args.output.replace(".json", "_beats.json") if args.output.endswith(".json") else "beats.json"
        with open(beats_path, "w", encoding="utf-8") as f:
            json.dump(beats, f, ensure_ascii=False, indent=2)
        print(f"\nSaved {len(beats)} beats to {beats_path}")

        # Summary
        non_neutral = [b for b in beats if b["beat_type"] != "neutral"]
        high_priority = [b for b in beats if b["priority"] >= 2]
        print(f"\n=== Summary ===")
        print(f"Total segments: {len(beats)}")
        print(f"Segments with beats: {len(non_neutral)}")
        print(f"High priority (SFX suggested): {len(high_priority)}")
        if non_neutral:
            print(f"\nSFX candidates:")
            for b in non_neutral:
                print(f"  {b['start_seconds']:.2f}s: {b['beat_type']} -> {b['sfx_suggestion']} ({b['text'][:50]})")

    return 0


if __name__ == "__main__":
    sys.exit(main())
