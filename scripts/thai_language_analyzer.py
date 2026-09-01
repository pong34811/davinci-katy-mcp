#!/usr/bin/env python3
"""Thai Language Analyzer — detect sarcasm, idioms, and cultural references.

Enhances beat detection with Thai-specific language understanding:
- Sarcasm detection (Thai indirect criticism)
- Idiom recognition
- Cultural reference handling
- Politeness particle analysis
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# Thai Sarcasm Patterns
SARCASM_PATTERNS = [
    # "เก่งมาก" (sarcastic)
    (r"เก่ง[^ก]+มาก", "sarcastic_praise"),
    (r"เก่งสุดๆ", "sarcastic_praise"),
    (r"สุดยอด", "sarcastic_praise"),
    (r"เยี่ยม[^่]+เลย", "sarcastic_praise"),
    (r"ดี[^่]+ว่ะ", "sarcastic_praise"),
    # "ฉลาด" used sarcastically
    (r"ฉลาด[^ๆ]+เลย", "sarcastic_praise"),
    # Negative setup with positive words
    (r"แต่.*เก่ง", "contrast_sarcasm"),
    (r"แต่.*ดี", "contrast_sarcasm"),
    (r"แต่ว่า.*เยี่ยม", "contrast_sarcasm"),
]

# Thai Idioms and Expressions
THAI_IDIOMS = {
    "chib_hai_wat": [
        "ชิบหายวายวอด",
        "ชิบฮา้ย",
        "ชิบหาย",
    ],
    "mai_pen_rai": [
        "ไม่เปนไร",
        "ไม่ว่าไร",
        "โอเค",
    ],
    "sanuk": [
        "สนุก",
        "สนุ๊ก",
        "ฮา",
    ],
    "jai_muen_lung": [
        "ใจมืดlung",
        "ใจเสื่ยว",
        "หวาดไก่",
    ],
}

# Cultural References
CULTURAL_REFS = {
    "555": ["555", "5555", "ฮ่าๆๆ", "หุหุ"],
    "kra_rong": ["เกร็ง", "เคร่ง", "ตึง"],
    "nak_ruk": ["น่ารัก", "น่ารักมาก", "ปิ๊ง"],
    "sad_sud": ["sad_sud", "sad Sud", "sadสุด"],
}

# Politeness Particles (affects tone analysis)
POLITENESS_PARTICLES = {
    "khrap": ["ครับ", "ครับ", "ครับผม"],
    "ka": ["ค่ะ", "ค๊ะ", "คับ"],
    "ja": ["จ้่า", "จ้า", "จิ้"],
    "na": ["น่า", "นะ", "นานะ"],
}


@dataclass
class ThaiLinguisticFeatures:
    """Features extracted from Thai text."""
    is_sarcasm: bool = False
    sarcasm_type: str = ""
    has_idiom: bool = False
    idiom_type: str = ""
    has_cultural_ref: bool = False
    cultural_ref: str = ""
    politeness_level: str = ""  # "formal", "casual", "slang"
    emotional_intensity: float = 0.0  # 0-1
    indirectness_score: float = 0.0  # 0-1, higher = more indirect


class ThaiLanguageAnalyzer:
    """Analyze Thai language for sarcasm, idioms, and cultural context."""

    def __init__(self):
        self._compiled_patterns = self._compile_patterns()

    def _compile_patterns(self) -> Dict[str, re.Pattern]:
        """Pre-compile regex patterns for performance."""
        compiled = {}
        for pattern in SARCASM_PATTERNS:
            compiled[pattern[0]] = re.compile(pattern[0], re.UNICODE)
        return compiled

    def analyze(
        self,
        text: str,
        previous_text: Optional[str] = None,
        next_text: Optional[str] = None,
    ) -> ThaiLinguisticFeatures:
        """Analyze Thai text for linguistic features.

        Args:
            text: The subtitle text to analyze.
            previous_text: Previous subtitle text for context.
            next_text: Next subtitle text for context.

        Returns:
            ThaiLinguisticFeatures with detected patterns.
        """
        features = ThaiLinguisticFeatures()
        text_lower = text.lower()

        # 1. Sarcasm Detection
        features.is_sarcasm, features.sarcasm_type = self._detect_sarcasm(text, text_lower, previous_text)

        # 2. Idiom Detection
        features.has_idiom, features.idiom_type = self._detect_idioms(text, text_lower)

        # 3. Cultural Reference Detection
        features.has_cultural_ref, features.cultural_ref = self._detect_cultural_refs(text, text_lower)

        # 4. Politeness Level
        features.politeness_level = self._detect_politeness(text, text_lower)

        # 5. Emotional Intensity
        features.emotional_intensity = self._calculate_emotional_intensity(text, text_lower, features)

        # 6. Indirectness Score
        features.indirectness_score = self._calculate_indirectness(text, features)

        return features

    def _detect_sarcasm(
        self,
        text: str,
        text_lower: str,
        previous_text: Optional[str] = None,
    ) -> Tuple[bool, str]:
        """Detect sarcasm in Thai text."""
        # Check direct sarcasm patterns
        for pattern_str, sarcasm_type in SARCASM_PATTERNS:
            if self._compiled_patterns[pattern_str].search(text):
                return True, sarcasm_type

        # Check for positive words after negative setup
        if previous_text:
            prev_lower = previous_text.lower()
            if any(neg in prev_lower for neg in ["แย่", "เสีย", "ผิดพลาด", "fail"]):
                if any(pos in text_lower for pos in ["ดี", "เก่ง", "เยี่ยม", "good", "great"]):
                    return True, "contrast_sarcasm"

        # Check for exaggerated praise
        if re.search(r"มาก[^ๆ]*มาก|สุด[^ๆ]*สุด|ที่สุด", text):
            return True, "exaggerated_praise"

        return False, ""

    def _detect_idioms(self, text: str, text_lower: str) -> Tuple[bool, str]:
        """Detect Thai idioms and expressions."""
        for idiom_type, variations in THAI_IDIOMS.items():
            for variation in variations:
                if variation.lower() in text_lower:
                    return True, idiom_type
        return False, ""

    def _detect_cultural_refs(self, text: str, text_lower: str) -> Tuple[bool, str]:
        """Detect cultural references."""
        for ref_type, markers in CULTURAL_REFS.items():
            for marker in markers:
                if marker.lower() in text_lower:
                    return True, ref_type
        return False, ""

    def _detect_politeness(self, text: str, text_lower: str) -> str:
        """Detect politeness level."""
        # Check for formal particles
        if any(p in text for p in POLITENESS_PARTICLES["khrap"]):
            return "formal"
        if any(p in text for p in POLITENESS_PARTICLES["ka"]):
            return "formal"

        # Check for casual particles
        if any(p in text for p in POLITENESS_PARTICLES["ja"]):
            return "casual"
        if any(p in text for p in POLITENESS_PARTICLES["na"]):
            return "casual"

        # Check for slang
        slang_markers = ["ว่ะ", "ว้าย", "เอ้ย", "อ๊าย", "555", "หุหุ"]
        if any(s in text for s in slang_markers):
            return "slang"

        return "neutral"

    def _calculate_emotional_intensity(
        self,
        text: str,
        text_lower: str,
        features: ThaiLinguisticFeatures,
    ) -> float:
        """Calculate emotional intensity (0-1)."""
        score = 0.0

        # Exclamation marks
        score += text.count("!") * 0.1
        score += text.count("!") * 0.05

        # Repetition (indicates emphasis)
        if re.search(r"(.)\1{2,}", text):
            score += 0.3

        # Sarcasm increases intensity
        if features.is_sarcasm:
            score += 0.2

        # Idioms often have high emotional content
        if features.has_idiom:
            score += 0.15

        # Cultural references
        if features.has_cultural_ref:
            score += 0.1

        # Emotional words
        emotional_words = ["ว้าว", "โอ้", "โหย", "เฮ้ย", "อ้าว", "ว้าย", "wow", "omg"]
        for word in emotional_words:
            if word in text_lower:
                score += 0.1

        return min(1.0, score)

    def _calculate_indirectness(
        self,
        text: str,
        features: ThaiLinguisticFeatures,
    ) -> float:
        """Calculate how indirect the communication is (0-1)."""
        score = 0.0

        # Sarcasm is inherently indirect
        if features.is_sarcasm:
            score += 0.4

        # Idioms are indirect expressions
        if features.has_idiom:
            score += 0.3

        # Polite particles can indicate indirectness
        if features.politeness_level == "formal":
            score += 0.1

        # Questions are indirect
        if "?" in text or "ไหม" in text or "หรือ" in text:
            score += 0.2

        # "But" markers indicate indirectness
        if re.search(r"แต่ว่า|แต่ว่า|แต่ทว่า", text):
            score += 0.2

        return min(1.0, score)


def analyze_thai_text(
    text: str,
    previous_text: Optional[str] = None,
    next_text: Optional[str] = None,
) -> ThaiLinguisticFeatures:
    """Convenience function for Thai text analysis."""
    analyzer = ThaiLanguageAnalyzer()
    return analyzer.analyze(text, previous_text, next_text)


if __name__ == "__main__":
    # Test cases
    test_cases = [
        ("เก่งมากเลย!", "แย่จริงๆ", None),
        ("ชิบหายวายวอด", None, None),
        ("555+ ตลกมาก", None, None),
        ("ดีว่ะ", None, None),
        ("แต่เก่งมากเลยนะ", "ทำผิดมา", None),
    ]

    print("=== Thai Language Analysis ===\n")
    for text, prev, next_text in test_cases:
        features = analyze_thai_text(text, prev, next_text)
        print(f"Text: {text}")
        print(f"  Sarcasm: {features.is_sarcasm} ({features.sarcasm_type})")
        print(f"  Idiom: {features.has_idiom} ({features.idiom_type})")
        print(f"  Cultural Ref: {features.has_cultural_ref} ({features.cultural_ref})")
        print(f"  Politeness: {features.politeness_level}")
        print(f"  Emotional Intensity: {features.emotional_intensity:.2f}")
        print(f"  Indirectness: {features.indirectness_score:.2f}")
        print()
