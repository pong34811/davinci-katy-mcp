#!/usr/bin/env python3
"""Impact Scorer — multi-factor scoring for subtitle segments.

Replaces simple keyword matching with a weighted scoring system that
considers comedy, emotion, surprise, emphasis, transition, retention,
and context signals. Every subtitle gets a composite impact score
and a ranked list of SFX family recommendations.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# ── Impact Signal Dictionaries ────────────────────────────────────────

# Thai emotional particles and exclamations
THAI_EXCLAMATIONS = {
    "wow": ["ว้าว", "ว้าย", "โหย", "โอ้", "อุ้", "อุ๊ย"],
    "surprise": ["อะไรนะ", "อะไรกัน", "มาจากไหน", "ไหนวะ", "ห๊ะ", "หุ้ย", "เฮ้ย", "อ้าว", "อ๊ะ", "โอ้โห", "เซ็งแซ่"],
    "excitement": ["เย้", "วู่วาม", "วูบ", "ปัง", "ปัง!", "โคตร", "เทพ", "สุดยอด", "เจ๋ง", "ย๊าย", "ดีใจ", "ดีจัง", "ยินดี"],
    "sadness": ["เศร้า", "เสียใจ", "อยากร้องไห้", "ใจหาย", "เจ็บ", "เจ็บใจ", "เหงา", "สงสาร", "น่าสงสาร"],
    "anger": ["โกรธ", "โมโห", "ขยะแขยง", "น่ารำคาญ", "แสบ", "หวิว", "หมั่นไส้", "เกลียด"],
    "confusion": ["งง", "ไม่เข้าใจ", "ไม่รู้ว่า", "ทำไม", "ยังไง", "อย่างไร", "อะไร", "ไม่รู้นะ", "งงมาก"],
    "disbelief": ["ไม่เชื่่อ", "จริงดิ", "จริงหรอ", "จริงๆหรอ", "เหรอ", "หรอ", "จริงๆนะ", "อะไรกันแน่"],
    "emphasis": ["เลย", "นะ", "ค่ะ", "ครับ", "จ้า", "อ่ะ", "อะ", "เอาจริง", "จริงๆ"],
}

# English emotional words
ENGLISH_EXCLAMATIONS = {
    "wow": ["wow", "omg", "oh my", "holy", "no way"],
    "surprise": ["surprise", "what", "wait", "hold on", "seriously"],
    "excitement": ["yay", "yes!", "finally", "awesome", "amazing", "great", "love it", "best ever"],
    "sadness": ["sad", "unfortunately", "alas", "too bad", "regret"],
    "anger": ["angry", "hate", "annoying", "frustrating", "ridiculous"],
    "confusion": ["confused", "what?", "huh?", "why?", "how?", "wait what"],
}

# Number patterns (for emphasis scoring)
NUMBER_PATTERNS = [
    r"\b\d{4,}\b",        # 1,000+
    r"\b\d{1,3}(,\d{3})+\b",  # 1,234
    r"\b\d+\s*(ล้าน|หมื่น|พัน|เศษ|เปอร์เซ็นต์|percent|million|thousand)\b",
]

# Sarcasm markers (Thai + English)
SARCASM_MARKERS = [
    "เก่งมาก", "เก่งสุดๆ", "สุดยอด", "เยี่ยมเลย", "ดีว่ะ", "เท่", "ฉลาด",
    "smart", "brilliant", "amazing", "fantastic", "wonderful",
    "555", "หุหุ", "ฮ่าๆ", "ขำ",
]

# Joke / meme patterns
JOKE_PATTERNS = [
    r"555+", r"ฮ่า", r"ห๊า", r"ตลก", r"มุก", r"ขำ", r"funny", r"lol", r"lmao",
    r"haha", r" joke ", r" meme ", r"มุกดัง",
]

# Transition markers
TRANSITION_MARKERS = [
    "ต่อมา", "แล้วก็ตาม", "ถัดมา", "ต่อไป", "ทีนี้", "ถัดจากนี้",
    "next", "then", "moving on", "now let's", "after that",
]

# Punchline indicators
PUNCHLINE_MARKERS = [
    "แต่", "แต่ว่า", "แต่ทว่า", "however", "but", "actually",
    "finally", "ในที่สุด", "จริงๆแล้ว", "ที่จริง",
]

# Reaction patterns (what to listen for after a punchline)
REACTION_MARKERS = [
    "เลย", "เหรอ", "ว่ะ", "ว้าย", "เอ้ย", "อ๊าย",
    "really?", "seriously?", "no way", "for real?",
]


# ── Data Models ───────────────────────────────────────────────────────

@dataclass
class ImpactSignals:
    """Raw impact signals detected in a subtitle segment."""
    text: str
    # Individual scores
    comedy_score: float = 0.0
    emotion_score: float = 0.0
    surprise_score: float = 0.0
    emphasis_score: float = 0.0
    transition_score: float = 0.0
    retention_score: float = 0.0
    context_score: float = 0.0
    # Flags
    is_sarcasm: bool = False
    is_joke: bool = False
    is_punchline: bool = False
    is_reaction: bool = False
    has_numbers: bool = False
    number_values: List[str] = field(default_factory=list)
    detected_emotions: List[str] = field(default_factory=list)
    # Composite
    impact_score: float = 0.0
    # Recommendations
    sfx_families: List[str] = field(default_factory=list)
    timing_offset: float = 0.0  # -0.2 = pre-hit, 0 = on-hit, +0.2 = post-hit


@dataclass
class SegmentContext:
    """Context window around a subtitle segment."""
    previous: List[str] = field(default_factory=list)
    next: List[str] = field(default_factory=list)
    section_label: str = ""  # "setup", "build-up", "punchline", "reaction", "resolution"
    story_arc_position: str = ""  # "start", "middle", "climax", "end"


# ── Impact Scorer ─────────────────────────────────────────────────────

class ImpactScorer:
    """Multi-factor impact scoring for subtitle segments.

    Scores each subtitle on 7 dimensions, then produces a composite
    impact score and SFX family recommendations.
    """

    # Weight map for composite score
    WEIGHTS = {
        "comedy": 0.15,
        "emotion": 0.20,
        "surprise": 0.20,
        "emphasis": 0.15,
        "transition": 0.10,
        "retention": 0.10,
        "context": 0.10,
    }

    def __init__(
        self,
        format_type: str = "talking-head",
        context_window: int = 3,
    ):
        self.format_type = format_type
        self.context_window = context_window
        self._compiled_patterns = self._compile_patterns()

    def _compile_patterns(self) -> Dict[str, re.Pattern]:
        """Pre-compile regex patterns for performance."""
        patterns = {}
        for key, items in [
            ("numbers", NUMBER_PATTERNS),
            ("jokes", JOKE_PATTERNS),
            ("transitions", TRANSITION_MARKERS),
        ]:
            combined = "|".join(items)
            patterns[key] = re.compile(combined, re.I | re.UNICODE)
        return patterns

    def score_segment(
        self,
        text: str,
        context: Optional[SegmentContext] = None,
        start_time: float = 0.0,
        end_time: float = 0.0,
    ) -> ImpactSignals:
        """Score a single subtitle segment across all dimensions.

        Args:
            text: The subtitle text to score.
            context: Surrounding subtitles for context analysis.
            start_time: Start timestamp in seconds.
            end_time: End timestamp in seconds.

        Returns:
            ImpactSignals with all scores and recommendations.
        """
        signals = ImpactSignals(text=text)
        text_lower = text.lower()

        # 1. Comedy Score
        signals.comedy_score = self._score_comedy(text, text_lower)

        # 2. Emotion Score
        emotion_scores, detected_emotions = self._score_emotion(text, text_lower)
        signals.emotion_score = max(emotion_scores.values()) if emotion_scores else 0.0
        signals.detected_emotions = detected_emotions

        # 3. Surprise Score
        signals.surprise_score = self._score_surprise(text, text_lower)

        # 4. Emphasis Score
        signals.emphasis_score = self._score_emphasis(text, text_lower)

        # 5. Transition Score
        signals.transition_score = self._score_transition(text, text_lower)

        # 6. Retention Score
        signals.retention_score = self._score_retention(text, text_lower)

        # 7. Context Score
        if context:
            signals.context_score = self._score_context(text, context, text_lower)

        # Composite Impact Score
        signals.impact_score = self._compute_composite(signals)

        # Flags
        signals.is_sarcasm = self._detect_sarcasm(text, text_lower)
        signals.is_joke = bool(self._compiled_patterns["jokes"].search(text))
        signals.is_punchline = self._detect_punchline(text, context)
        signals.is_reaction = self._detect_reaction(text, context)
        signals.has_numbers, signals.number_values = self._extract_numbers(text)

        # Timing offset (pre-hit / on-hit / post-hit)
        signals.timing_offset = self._determine_timing(signals, context)

        # SFX Family Recommendations
        signals.sfx_families = self._recommend_families(signals)

        return signals

    def _score_comedy(self, text: str, text_lower: str) -> float:
        """Score how comedic a segment is."""
        score = 0.0
        # Laughter patterns
        if re.search(r"555+", text):
            score += 0.5
        if re.search(r"หุหุ|ฮ่า|ขำ", text):
            score += 0.3
        # English laughter
        if any(w in text_lower for w in ["lol", "lmao", "haha"]):
            score += 0.3
        # Joke patterns
        if self._compiled_patterns["jokes"].search(text):
            score += 0.4
        # Sarcasm
        if self._detect_sarcasm(text, text_lower):
            score += 0.3
        return min(1.0, score)

    def _score_emotion(self, text: str, text_lower: str) -> Tuple[Dict[str, float], List[str]]:
        """Score emotional intensity across multiple emotion types."""
        scores: Dict[str, float] = {}
        detected: List[str] = []

        for emotion, words in {
            **{k: v for d in [THAI_EXCLAMATIONS, ENGLISH_EXCLAMATIONS] for k, v in d.items()},
        }.items():
            score = 0.0
            for word in words:
                if word.lower() in text_lower:
                    score += 0.3
                    if emotion not in detected:
                        detected.append(emotion)
            if score > 0:
                scores[emotion] = min(1.0, score)

        return scores, detected

    def _score_surprise(self, text: str, text_lower: str) -> float:
        """Score surprise/shock intensity."""
        score = 0.0
        for emotions in [THAI_EXCLAMATIONS, ENGLISH_EXCLAMATIONS]:
            if "surprise" in emotions:
                for word in emotions["surprise"]:
                    if word.lower() in text_lower:
                        score += 0.4
                        break
            if "disbelief" in emotions:
                for word in emotions["disbelief"]:
                    if word.lower() in text_lower:
                        score += 0.3
                        break
        return min(1.0, score)

    def _score_emphasis(self, text: str, text_lower: str) -> float:
        """Score emphasis/important information."""
        score = 0.0
        # Number detection
        has_large_nums = bool(re.search(r"\b\d{4,}\b", text))
        has_percent = bool(re.search(r"เปอร์เซ็นต์|percent|%", text))
        has_rank = bool(re.search(r"ที่.*\d+|rank|อันดับ", text))
        if has_large_nums:
            score += 0.4
        if has_percent:
            score += 0.3
        if has_rank:
            score += 0.3
        # Emphatic particles
        if re.search(r"เลย|นะ|ค่ะ|ครับ", text):
            score += 0.2
        return min(1.0, score)

    def _score_transition(self, text: str, text_lower: str) -> float:
        """Score transition/importance."""
        score = 0.0
        if self._compiled_patterns["transitions"].search(text):
            score += 0.5
        if re.search(r"ตอน|ช่วง|ครั้ง|episode", text, re.I):
            score += 0.2
        return min(1.0, score)

    def _score_retention(self, text: str, text_lower: str) -> float:
        """Score retention value — will viewers remember this?"""
        score = 0.0
        # Questions create curiosity
        if re.search(r"ทำไม|ยังไง|อะไร|ที่ไหน|เมื่อไหร่|ใคร", text):
            score += 0.3
        # Teasers
        if re.search(r"เดี๋ยวก่อน|รอ before|actually|secret|hidden|reveal", text, re.I):
            score += 0.3
        # Numbers with context
        if self._extract_numbers(text)[0]:
            score += 0.2
        return min(1.0, score)

    def _score_context(self, text: str, context: SegmentContext, text_lower: str) -> float:
        """Score based on surrounding context (setup → punchline → reaction)."""
        score = 0.0
        all_text = " ".join(context.previous + [text] + context.next)
        all_lower = all_text.lower()

        # Check for story arc position
        if context.story_arc_position in ("punchline", "climax"):
            score += 0.4
        elif context.story_arc_position == "setup":
            score += 0.1  # Setup rarely needs SFX
        elif context.story_arc_position == "reaction":
            score += 0.3

        # Check if previous segments build up to this one
        prev_text = " ".join(context.previous[-3:]) if context.previous else ""
        if any(w in prev_text.lower() for w in ["แต่", "however", "wait", "แต่ทว่า", "แต่ก็"]):
            score += 0.2

        # Check for emotional escalation
        prev_emotions = [self._score_emotion(p, p.lower())[0] for p in context.previous[-2:]]
        if prev_emotions and max(prev_emotions) < 0.3:
            score += 0.1  # Building from neutral

        return min(1.0, score)

    def _detect_sarcasm(self, text: str, text_lower: str) -> bool:
        """Detect sarcasm in text."""
        for marker in SARCASM_MARKERS:
            if marker.lower() in text_lower:
                return True
        # Sarcasm often follows a negative setup with positive words
        if re.search(r"แต่.*เก่ง|แต่.*ดี|แต่.*เยี่ยม", text):
            return True
        return False

    def _detect_punchline(self, text: str, context: Optional[SegmentContext]) -> bool:
        """Detect if this segment is a punchline."""
        if not context:
            return False
        # Punchline often follows "แต่" or "แต่ทว่า"
        prev_text = " ".join(context.previous[-2:]) if context.previous else ""
        if re.search(r"แต่|however|but|actually", prev_text, re.I):
            return True
        # Punchline often has short, punchy text
        if len(text) < 20 and self._score_surprise(text, text.lower()) > 0.3:
            return True
        return False

    def _detect_reaction(self, text: str, context: Optional[SegmentContext]) -> bool:
        """Detect if this segment is a reaction to a previous event."""
        if not context:
            return False
        # Reaction often follows a surprise or punchline
        prev_text = " ".join(context.previous[-1:]) if context.previous else ""
        if self._score_surprise(prev_text, prev_text.lower()) > 0.3:
            return True
        # Reaction markers
        for marker in REACTION_MARKERS:
            if marker.lower() in text.lower():
                return True
        return False

    def _extract_numbers(self, text: str) -> Tuple[bool, List[str]]:
        """Extract numeric values from text."""
        numbers = re.findall(r"\b\d[\d,]*\.?\d*\b", text)
        cleaned = [n.replace(",", "") for n in numbers]
        return bool(cleaned), cleaned

    def _compute_composite(self, signals: ImpactSignals) -> float:
        """Compute weighted composite impact score."""
        total = 0.0
        total += signals.comedy_score * self.WEIGHTS["comedy"]
        total += signals.emotion_score * self.WEIGHTS["emotion"]
        total += signals.surprise_score * self.WEIGHTS["surprise"]
        total += signals.emphasis_score * self.WEIGHTS["emphasis"]
        total += signals.transition_score * self.WEIGHTS["transition"]
        total += signals.retention_score * self.WEIGHTS["retention"]
        total += signals.context_score * self.WEIGHTS["context"]

        # Bonus for sarcasm (always needs SFX)
        if signals.is_sarcasm:
            total += 0.1
        # Bonus for punchlines
        if signals.is_punchline:
            total += 0.15
        # Penalty for filler
        if signals.impact_score < 0.2 and not signals.is_transition:
            total *= 0.5

        return min(1.0, total)

    def _determine_timing(
        self,
        signals: ImpactSignals,
        context: Optional[SegmentContext],
    ) -> float:
        """Determine timing offset: pre-hit, on-hit, or post-hit."""
        # Punchlines often benefit from pre-hit anticipation
        if signals.is_punchline and context:
            prev_text = " ".join(context.previous[-1:]) if context.previous else ""
            if re.search(r"แต่|however|but|wait", prev_text, re.I):
                return -0.15  # Pre-hit

        # Reactions should be post-hit
        if signals.is_reaction:
            return 0.1  # Post-hit

        # Surprise on the word itself
        if signals.surprise_score > 0.5:
            return 0.0  # On-hit

        # Transitions can be flexible
        if signals.transition_score > 0.3:
            return -0.1  # Slight pre-hit

        return 0.0  # Default on-hit

    def _recommend_families(self, signals: ImpactSignals) -> List[str]:
        """Recommend SFX families based on impact signals."""
        families = []

        if signals.comedy_score > 0.4:
            families.extend(["pop", "blip", "honk", "awkward"])
        if signals.surprise_score > 0.4:
            families.extend(["impact", "pop", "scream"])
        if signals.emotion_score > 0.3:
            if any(e in signals.detected_emotions for e in ["excitement", "surprise"]):
                families.extend(["sparkle", "collect", "ding"])
            elif any(e in signals.detected_emotions for e in ["sadness", "anger"]):
                families.extend(["wrong", "scratch", "glass"])
        if signals.emphasis_score > 0.4:
            families.extend(["ding", "collect", "pop"])
        if signals.transition_score > 0.3:
            families.extend(["whoosh", "rise"])
        if signals.is_joke:
            families.extend(["pop", "blip", "plink"])
        if signals.is_sarcasm:
            families.extend(["wrong", "scratch", "awkward"])

        # Deduplicate while preserving order
        seen = set()
        unique = []
        for f in families:
            if f not in seen:
                seen.add(f)
                unique.append(f)
        return unique

    def score_transcript(
        self,
        subtitles: List[Dict[str, Any]],
        format_type: str = "talking-head",
    ) -> List[Tuple[Dict[str, Any], ImpactSignals]]:
        """Score a full transcript with context windows.

        Args:
            subtitles: List of subtitle dicts with 'text', 'start_seconds', 'end_seconds'.
            format_type: Content format for context adjustments.

        Returns:
            List of (subtitle, signals) tuples.
        """
        scorer = ImpactScorer(format_type=format_type, context_window=3)
        results = []

        for i, sub in enumerate(subtitles):
            # Build context window
            prev_subs = [subtitles[j]["text"] for j in range(max(0, i - 3), i)]
            next_subs = [subtitles[j]["text"] for j in range(i + 1, min(len(subtitles), i + 4))]

            context = SegmentContext(
                previous=prev_subs,
                next=next_subs,
            )

            signals = scorer.score_segment(
                text=sub["text"],
                context=context,
                start_time=sub.get("start_seconds", 0),
                end_time=sub.get("end_seconds", 0),
            )

            results.append((sub, signals))

        return results


# ── Impact Level Classification ───────────────────────────────────────

def classify_impact(score: float) -> str:
    """Classify impact score into discrete levels."""
    if score >= 0.7:
        return "CRITICAL"
    elif score >= 0.5:
        return "HIGH"
    elif score >= 0.3:
        return "MEDIUM"
    elif score > 0.15:
        return "LOW"
    else:
        return "NONE"


def should_place_sfx(signals: ImpactSignals, min_impact: float = 0.3) -> bool:
    """Decision: should we place an SFX for this segment?"""
    # Hard rules
    if signals.impact_score < min_impact:
        return False
    # Transitions can be lower threshold
    if signals.transition_score > 0.3 and signals.impact_score >= 0.2:
        return True
    # Emphasis with numbers is always a candidate
    if signals.has_numbers and signals.emphasis_score > 0.3:
        return True
    return signals.impact_score >= min_impact


if __name__ == "__main__":
    # Test the scorer
    test_subs = [
        {"text": "สวัสดีทุกคน", "start_seconds": 0.0, "end_seconds": 2.0},
        {"text": "วันนี้เป็นวันที่ 9 แล้ว", "start_seconds": 2.0, "end_seconds": 5.0},
        {"text": "ว้าว! 1,000วิวแล้ว!", "start_seconds": 10.0, "end_seconds": 13.0},
        {"text": "อะไรกันนะ หมูมาจากไหนวะ", "start_seconds": 15.0, "end_seconds": 18.0},
        {"text": "ผิดแล้วจ้าาา", "start_seconds": 20.0, "end_seconds": 22.0},
    ]

    scorer = ImpactScorer(format_type="talking-head")
    results = scorer.score_transcript(test_subs)

    print("=== Impact Scoring Results ===\n")
    for sub, signals in results:
        level = classify_impact(signals.impact_score)
        print(f"[{level:8}] score={signals.impact_score:.2f} | impact={signals.impact_score:.2f}")
        print(f"       text: {sub['text']}")
        print(f"       emotions: {signals.detected_emotions}")
        print(f"       families: {signals.sfx_families}")
        print(f"       timing: {signals.timing_offset:+.2f}s")
        print()
