#!/usr/bin/env python3
"""Story Arc Analyzer — analyze subtitle structure for SFX placement.

Reads 3-5 subtitles before/after current one to understand:
- Setup → Build-up → Punchline → Reaction → Resolution
- Detects story arc position for each segment
- Identifies turning points and emotional shifts
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class Section:
    """A section of the video with start/end time and theme."""
    start_seconds: float
    end_seconds: float
    theme: str
    mood: str  # "neutral", "build-up", "climax", "resolution"
    subtitles: List[Dict[str, Any]]


@dataclass
class ArcPosition:
    """Story arc position for a segment."""
    segment_index: int
    position: str  # "setup", "build-up", "punchline", "reaction", "resolution", "climax"
    section_label: str
    is_turning_point: bool
    is_punchline: bool
    is_reaction: bool
    narrative_role: str  # "setup", "conflict", "climax", "release", "bridge"


class StoryArcAnalyzer:
    """Analyzes subtitle structure to find story arcs and turning points."""

    # Mood transition markers
    BUILD_UP_MARKERS = [
        "แต่ว่า", "แต่ว่า", "แต่ทว่า", "อย่างไรก็ตาม", "ความจริง", " secret",
        "actually", "however", "but", "wait", "เดี๋ยวก่อน", "รอ before",
        "ในที่สุด", "finally", "ท้ายที่สุด", "สรุป", "conclusion",
    ]

    PUNCHLINE_MARKERS = [
        "เลย", "อ่ะ", "วะ", "ว่ะ", "ว้าย", "ฮ่า", "555",
        "wow", "omg", "lol", "haha", "punchline",
    ]

    REACTION_MARKERS = [
        "เหรอ", "หรอ", "เหรอวะ", "อะไรนะ", "อะไรกันท่า",
        "really?", "seriously?", "no way", "wait what",
    ]

    RESOLUTION_MARKERS = [
        "จบ", "จบแล้ว", "สรุป", "bye", "บ๊ายบาย", "ลาก่อน",
        "thanks", "thank you", "bye", "see you",
    ]

    def __init__(self, context_window: int = 3):
        self.context_window = context_window

    def analyze(
        self,
        subtitles: List[Dict[str, Any]],
    ) -> List[ArcPosition]:
        """Analyze story arc for all segments.

        Args:
            subtitles: List of subtitle dicts with 'text', 'start_seconds', 'end_seconds'

        Returns:
            List of ArcPosition for each segment
        """
        positions = []

        for i, sub in enumerate(subtitles):
            # Get context window
            prev_subs = [subtitles[j]["text"] for j in range(max(0, i - self.context_window), i)]
            next_subs = [subtitles[j]["text"] for j in range(i + 1, min(len(subtitles), i + self.context_window + 1))]

            position = self._classify_position(sub, prev_subs, next_subs, i, len(subtitles))
            positions.append(position)

        return positions

    def _classify_position(
        self,
        current: Dict[str, Any],
        prev_subs: List[str],
        next_subs: List[str],
        index: int,
        total: int,
    ) -> ArcPosition:
        """Classify the story arc position of a segment."""
        text = current["text"]
        text_lower = text.lower()

        # Calculate relative position in video
        relative_pos = index / max(1, total - 1)

        # Check for punchline
        is_punchline = self._is_punchline(text, prev_subs, next_subs)

        # Check for reaction
        is_reaction = self._is_reaction(text, prev_subs, next_subs)

        # Check for turning point
        is_turning_point = self._is_turning_point(text, prev_subs, next_subs)

        # Determine position
        if relative_pos < 0.15:
            position = "setup"
            narrative_role = "setup"
        elif relative_pos > 0.85:
            position = "resolution"
            narrative_role = "release"
        elif is_punchline:
            position = "punchline"
            narrative_role = "climax"
        elif is_reaction:
            position = "reaction"
            narrative_role = "release"
        elif is_turning_point:
            position = "build-up"
            narrative_role = "conflict"
        else:
            position = "build-up"
            narrative_role = "bridge"

        # Build section label
        section_label = self._get_section_label(position, index, total)

        return ArcPosition(
            segment_index=index,
            position=position,
            section_label=section_label,
            is_turning_point=is_turning_point,
            is_punchline=is_punchline,
            is_reaction=is_reaction,
            narrative_role=narrative_role,
        )

    def _is_punchline(self, text: str, prev_subs: List[str], next_subs: List[str]) -> bool:
        """Check if segment is a punchline."""
        # Punchline often follows "but" or surprise setup
        prev_text = " ".join(prev_subs)
        if any(marker in prev_text.lower() for marker in ["แต่ว่า", "however", "but", "wait", "เดี๋ยว"]):
            return True

        # Punchline often has short, punchy text
        if len(text) < 15 and any(m in text for m in ["555", "ว้าว", "ว้าย", "โอ้", "ห๊ะ"]):
            return True

        # Punchline followed by reaction
        if next_subs and any(m in next_subs[0].lower() for m in ["เหรอ", "Really?", "what?"]):
            return True

        return False

    def _is_reaction(self, text: str, prev_subs: List[str], next_subs: List[str]) -> bool:
        """Check if segment is a reaction to previous event."""
        # Check previous for surprise/punchline
        prev_text = " ".join(prev_subs[-2:]) if prev_subs else ""
        if any(m in prev_text.lower() for m in ["ว้าว", "wow", "omg", "ห๊ะ", "อะไร"]):
            if any(m in text.lower() for m in ["เหรอ", "Really", "what", "ว้าย"]):
                return True

        # Check for reaction markers
        if any(m in text.lower() for m in ["ว้าย", "เอ้ย", "อ๊าย", "what?", "seriously?"]):
            return True

        return False

    def _is_turning_point(self, text: str, prev_subs: List[str], next_subs: List[str]) -> bool:
        """Check if segment is a turning point."""
        # Look for transition markers
        if any(m in text.lower() for m in ["แต่ว่า", "however", "but", "actually"]):
            return True

        # Look for emotional shift indicators
        if any(m in text.lower() for m in ["เศร้า", "เสียใจ", "โกรธ", "anger", "sad"]):
            # Check if previous was positive
            prev_text = " ".join(prev_subs[-1:]) if prev_subs else ""
            if any(m in prev_text.lower() for m in ["ดี", "happy", "joy", "เย้", "waw"]):
                return True

        return False

    def _get_section_label(self, position: str, index: int, total: int) -> str:
        """Get section label based on position."""
        if position == "setup":
            return "setup"
        elif position in ("build-up",):
            return "build-up"
        elif position in ("punchline", "climax"):
            return "climax"
        elif position == "reaction":
            return "reaction"
        else:
            return "resolution"

    def find_sections(self, subtitles: List[Dict[str, Any]]) -> List[Section]:
        """Find major sections in the video."""
        positions = self.analyze(subtitles)
        sections = []
        current_section: Optional[Section] = None

        for i, pos in enumerate(positions):
            sub = subtitles[i]

            if pos.position == "setup" and current_section is None:
                current_section = Section(
                    start_seconds=sub["start_seconds"],
                    end_seconds=sub["end_seconds"],
                    theme="intro",
                    mood="neutral",
                    subtitles=[sub],
                )
            elif pos.position == "climax" or pos.position == "punchline":
                if current_section:
                    current_section.end_seconds = sub["end_seconds"]
                current_section = Section(
                    start_seconds=sub["start_seconds"],
                    end_seconds=sub["end_seconds"],
                    theme="climax",
                    mood="climax",
                    subtitles=[sub],
                )
            elif pos.position == "resolution" or pos.position == "reaction":
                if current_section:
                    current_section.end_seconds = sub["end_seconds"]
                current_section = Section(
                    start_seconds=sub["start_seconds"],
                    end_seconds=sub["end_seconds"],
                    theme="resolution",
                    mood="resolution",
                    subtitles=[sub],
                )
            else:
                if current_section:
                    current_section.end_seconds = sub["end_seconds"]
                    current_section.subtitles.append(sub)
                else:
                    current_section = Section(
                        start_seconds=sub["start_seconds"],
                        end_seconds=sub["end_seconds"],
                        theme="build-up",
                        mood="build-up",
                        subtitles=[sub],
                    )

        if current_section:
            sections.append(current_section)

        return sections


if __name__ == "__main__":
    test_subs = [
        {"text": "สวัสดีทุกคน", "start_seconds": 0.0, "end_seconds": 2.0},
        {"text": "วันนี้เปลาที่ 9 แล้ว", "start_seconds": 2.0, "end_seconds": 5.0},
        {"text": "แต่ว่า... มีอะไร unexpected", "start_seconds": 10.0, "end_seconds": 13.0},
        {"text": "ว้าว! หมูมาจากไหนวะ!", "start_seconds": 15.0, "end_seconds": 18.0},
        {"text": "อะไรกันนะ", "start_seconds": 18.5, "end_seconds": 20.0},
        {"text": "ผิดแล้วจ้าาา", "start_seconds": 22.0, "end_seconds": 25.0},
        {"text": "บ๊ายบายครับ", "start_seconds": 65.0, "end_seconds": 68.0},
    ]

    analyzer = StoryArcAnalyzer()
    positions = analyzer.analyze(test_subs)

    print("=== Story Arc Analysis ===\n")
    for pos in positions:
        sub = test_subs[pos.segment_index]
        print(f"[{pos.position:10}] {pos.narrative_role:10} | {sub['text'][:30]}")
        if pos.is_turning_point:
            print(f"            ^ TURNING POINT")
        if pos.is_punchline:
            print(f"            ^ PUNCHLINE")
        if pos.is_reaction:
            print(f"            ^ REACTION")
        print()

    sections = analyzer.find_sections(test_subs)
    print("=== Sections ===\n")
    for sec in sections:
        print(f"[{sec.mood:10}] {sec.start_seconds:.1f}s - {sec.end_seconds:.1f}s | {sec.theme}")
