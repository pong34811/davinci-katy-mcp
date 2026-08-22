"""Video Event Analyzer.

Analyzes timeline transcripts, SRT subtitles, and timeline structure
to identify sound-effect worthy moments (punchlines, reactions, transitions, emphasis).
Automatically detects video content format (talking-head, podcast, game, meme, livestream).
"""

from __future__ import annotations

import logging
import re
from typing import Any, Dict, List, Optional, Tuple, Union

from src.sfx_engine.config import SFXConfig
from src.sfx_engine.models import BeatPoint, ContentFormat, EventType, TimelineEvent

logger = logging.getLogger(__name__)


# Thai and English Keyword Patterns for Event Identification
KEYWORD_PATTERNS: List[Tuple[EventType, float, re.Pattern]] = [
    # EventType, default impact score, regex pattern
    (
        EventType.EMPHASIS,
        0.75,
        re.compile(r"(?i)(ตัวเลข|จำนวน|สถิติ|เปอร์เซ็นต์|ล้าน|พัน|ร้อย|บาท|กิโล|เท่า|คะแนน|แสน|vtuber|pngtuber|วิทูเบอร์|วีทูปเบอร์|\b\d+[\d,.]*\b|percent|million|thousand|first|second)", re.UNICODE),
    ),
    (
        EventType.REACTION,
        0.8,
        re.compile(r"(?i)(เย้|ว้าว|โอ้|อ๊ะ|โห|ช็อก|เฮ็ด|งง|เหรอ|จริงดิ|เห้ย|อ้าว|อุ๊ย|ฮือ|ว๊าก|wow|omg|what|shock|surprise|yeah|hey)", re.UNICODE),
    ),
    (
        EventType.JOKE,
        0.85,
        re.compile(r"(?i)(555|ฮ่าๆ|ฮะฮะ|ตลก|มุก|ขำ|ปั่น|กวน|กาว|lol|lmao|haha|funny|joke|meme)", re.UNICODE),
    ),
    (
        EventType.FAIL,
        0.85,
        re.compile(r"(?i)(ผิด|พลาด|แตก|พัง|ดับ|ตาย|แพ้|แย่|ซวย|มั่ว|กรรม|oops|fail|wrong|died|dead|miss|lose|error|bug)", re.UNICODE),
    ),
    (
        EventType.SUCCESS,
        0.85,
        re.compile(r"(?i)(สำเร็จ|ชนะ|ได้แล้ว|ถูกต้อง|เยี่ยม|สุดยอด|เก่ง|ปัง|ผ่าน|เรียบร้อย|วิเศษ|win|success|correct|done|passed|cleared|perfect|level up)", re.UNICODE),
    ),
    (
        EventType.TRANSITION,
        0.7,
        re.compile(r"(?i)(ต่อไป|มาดูกัน|ขั้นตอน|ถัดไป|สรุป|เริ่ม|ตอนแรก|จบ|ถัดมา|next|then|now|after|finally|let's|step)", re.UNICODE),
    ),
    (
        EventType.DRAMATIC,
        0.8,
        re.compile(r"(?i)(แต่|แต่ว่า|ทว่า|อย่างไรก็ตาม|ความจริง|ลับ|อันตราย|ระวัง|ระเบิด|but|however|secret|danger|warning|shocking|dramatic)", re.UNICODE),
    ),
]


class EventAnalyzer:
    """Analyzes timeline text, subtitles, and structure for SFX beat placement."""

    def __init__(self, config: Optional[SFXConfig] = None):
        self.config = config or SFXConfig.load()

    def detect_format(
        self,
        timeline_info: Dict[str, Any],
        transcript_text: Optional[str] = None,
    ) -> ContentFormat:
        """Detect format classification of the current video timeline.

        Evaluates duration, track structure, timeline name, and speech density.
        """
        duration_sec = float(timeline_info.get("duration_seconds", 0.0))
        name = str(timeline_info.get("name", "")).lower()

        # Explicit name keywords
        if "meme" in name or "short" in name or "tiktok" in name or "reel" in name:
            return ContentFormat.MEME
        if "podcast" in name or "interview" in name:
            return ContentFormat.PODCAST
        if "game" in name or "play" in name or "stream" in name:
            return ContentFormat.GAME

        # Duration heuristics
        if 0 < duration_sec <= 45.0:
            return ContentFormat.MEME
        if duration_sec > 1800.0:  # > 30 minutes
            return ContentFormat.PODCAST

        # Default standard format
        return ContentFormat.TALKING_HEAD

    def analyze_subtitles(self, srt_content: str) -> List[TimelineEvent]:
        """Parse SubRip (.srt) content into timed TimelineEvents.

        Args:
            srt_content: Raw SRT file string.

        Returns:
            List of detected TimelineEvents with accurate timestamps.
        """
        blocks = re.split(r"\n\s*\n", srt_content.strip())
        events: List[TimelineEvent] = []

        for block in blocks:
            lines = [line.strip() for line in block.split("\n") if line.strip()]
            if len(lines) < 3:
                continue

            # Line 2 is timestamp
            time_line = lines[1]
            match = re.search(
                r"(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})",
                time_line,
            )
            if not match:
                continue

            h1, m1, s1, ms1, h2, m2, s2, ms2 = map(int, match.groups())
            start_sec = h1 * 3600 + m1 * 60 + s1 + ms1 / 1000.0
            end_sec = h2 * 3600 + m2 * 60 + s2 + ms2 / 1000.0
            text = " ".join(lines[2:])

            # Extract events from subtitle text
            detected = self._detect_events_in_text(text, start_sec, end_sec)
            events.extend(detected)

        # Sort chronologically
        events.sort(key=lambda e: e.timestamp)
        return events

    def analyze_transcript(
        self,
        transcript: Union[str, List[Dict[str, Any]]],
        format_type: ContentFormat = ContentFormat.TALKING_HEAD,
    ) -> List[TimelineEvent]:
        """Analyze word-level or text transcript into TimelineEvents."""
        events: List[TimelineEvent] = []

        if isinstance(transcript, str):
            # Plain string transcript without timestamps
            lines = transcript.split("\n")
            step = 3.0  # Estimate 3 sec per line
            for i, line in enumerate(lines):
                if line.strip():
                    t_start = i * step
                    events.extend(self._detect_events_in_text(line, t_start, t_start + step))
        elif isinstance(transcript, list):
            # Dict list [{'text': '...', 'start': 1.2, 'end': 3.4}]
            for item in transcript:
                text = str(item.get("text", ""))
                start = float(item.get("start", item.get("start_seconds", 0.0)))
                end = float(item.get("end", item.get("end_seconds", start + 2.0)))
                events.extend(self._detect_events_in_text(text, start, end))

        events.sort(key=lambda e: e.timestamp)
        return events

    def _detect_events_in_text(
        self,
        text: str,
        start_time: float,
        end_time: float,
    ) -> List[TimelineEvent]:
        """Match text against keyword patterns to locate events."""
        events: List[TimelineEvent] = []

        for event_type, base_score, pattern in KEYWORD_PATTERNS:
            for match in pattern.finditer(text):
                matched_word = match.group()
                # Estimate word position timestamp within block
                pos_ratio = match.start() / float(max(1, len(text)))
                timestamp = start_time + (end_time - start_time) * pos_ratio

                # Add small offset so SFX lands on or just after key word
                timestamp = round(timestamp, 3)

                events.append(
                    TimelineEvent(
                        type=event_type,
                        timestamp=timestamp,
                        description=f"Highlight '{matched_word}' ({event_type.value})",
                        impact_score=base_score,
                        duration=end_time - start_time,
                        text_snippet=text,
                    )
                )

        return events

    def find_beats(
        self,
        events: List[TimelineEvent],
        content_format: ContentFormat,
    ) -> List[BeatPoint]:
        """Convert timeline events into filtered, format-adjusted BeatPoints.

        Adjusts impact scores based on the content format (e.g. game boosts actions,
        podcast suppresses jokes).
        """
        beats: List[BeatPoint] = []

        for event in events:
            score = event.impact_score

            # Format-specific score modifications
            if content_format == ContentFormat.PODCAST:
                if event.type == EventType.JOKE:
                    score *= 0.4  # Suppress small jokes in podcasts
            elif content_format == ContentFormat.GAME:
                if event.type in (EventType.ACTION, EventType.SUCCESS, EventType.FAIL):
                    score *= 1.3  # Boost action in gaming
            elif content_format == ContentFormat.MEME:
                score *= 1.2  # Boost all reactions for meme edits

            score = min(1.0, max(0.1, score))

            beats.append(
                BeatPoint(
                    timestamp=event.timestamp,
                    event_type=event.type,
                    impact_score=round(score, 2),
                    description=event.description,
                )
            )

        beats.sort(key=lambda b: b.timestamp)
        return beats
