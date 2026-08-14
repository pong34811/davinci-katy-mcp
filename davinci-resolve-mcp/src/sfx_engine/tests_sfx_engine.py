"""Comprehensive Test Suite for DaVinci Resolve SFX Skill & Engine.

Tests:
1. SFXConfig loading and density limits.
2. SFXScanner directory parsing and taxonomy rules.
3. SFXSearch fuzzy string matching and taxonomy event lookups.
4. EventAnalyzer format detection, SRT parsing, and regex keyword detection.
5. SFXRecommender plan generation, density caps, and spacing/family rules.
6. SFXPlacer WAV trimming logic.
"""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from src.sfx_engine.analyzer import EventAnalyzer
from src.sfx_engine.config import SFXConfig
from src.sfx_engine.models import (
    ContentFormat,
    EventType,
    SFXCategory,
    SFXFile,
    SFXPlacement,
)
from src.sfx_engine.placer import trim_wav
from src.sfx_engine.recommender import SFXRecommender
from src.sfx_engine.scanner import SFXLibrary, SFXScanner
from src.sfx_engine.search import SFXSearch


class TestSFXEngine(unittest.TestCase):
    """Test suite for the SFX engine components."""

    def setUp(self) -> None:
        self.config = SFXConfig(
            sfx_raw_dir="C:/Users/warit/Desktop/davinci-katy-mcp/SFX",
            sfx_processed_dir="C:/Users/warit/Desktop/davinci-katy-mcp/SFX_processed",
            cache_dir=tempfile.gettempdir(),
        )

    def test_01_config(self) -> None:
        """Test configuration defaults and density limits."""
        self.assertEqual(self.config.default_fps, 60.0)
        density = self.config.get_density_limit("talking_head")
        self.assertEqual(density.max_per_minute, 5.0)

    def test_02_scanner(self) -> None:
        """Test directory scanning and taxonomy classification."""
        scanner = SFXScanner(self.config)
        library = scanner.scan(force_rescan=True)
        self.assertGreater(len(library.files), 0, "Library should contain scanned files")

        # Verify parsed processed file metadata
        pop_files = library.get_by_family("pop")
        self.assertGreater(len(pop_files), 0, "Should find 'pop' family files")
        self.assertEqual(pop_files[0].category, SFXCategory.COMEDY)

    def test_03_search(self) -> None:
        """Test fuzzy and taxonomy event searching."""
        scanner = SFXScanner(self.config)
        library = scanner.scan()
        search = SFXSearch(library, self.config)

        # Fuzzy search
        res = search.search("whoosh")
        self.assertGreater(len(res), 0)
        self.assertTrue("whoosh" in res[0].file.filename.lower())

        # Event search
        joke_sfx = search.search_by_event(EventType.JOKE)
        self.assertGreater(len(joke_sfx), 0)

    def test_04_analyzer(self) -> None:
        """Test SRT parsing and format detection."""
        analyzer = EventAnalyzer(self.config)

        # Format detection
        fmt = analyzer.detect_format({"name": "My Vlog Edit.drw", "duration_seconds": 120})
        self.assertEqual(fmt, ContentFormat.TALKING_HEAD)

        meme_fmt = analyzer.detect_format({"name": "Meme Clip", "duration_seconds": 25})
        self.assertEqual(meme_fmt, ContentFormat.MEME)

        # SRT parsing
        srt_sample = """1
00:00:01,000 --> 00:00:03,000
ยินดีต้อนรับสู่คลิปนี้ 555 ตลกมาก

2
00:00:10,000 --> 00:00:12,500
ยอดผู้ติดตามทะลุ 1,000 คนแล้ว เย้!
"""
        events = analyzer.analyze_subtitles(srt_sample)
        self.assertGreaterEqual(len(events), 2)
        event_types = [e.type for e in events]
        self.assertIn(EventType.JOKE, event_types)
        self.assertIn(EventType.REACTION, event_types)

    def test_05_recommender(self) -> None:
        """Test end-to-end plan generation and rule validation."""
        scanner = SFXScanner(self.config)
        library = scanner.scan()
        search = SFXSearch(library, self.config)
        analyzer = EventAnalyzer(self.config)
        recommender = SFXRecommender(search, analyzer, self.config)

        srt_path = "C:/Users/warit/Desktop/davinci-katy-mcp/subtitle_from_track1.srt"
        if os.path.exists(srt_path):
            plan = recommender.generate_plan(
                timeline_info={"name": "Day 10 Edit", "duration_seconds": 127.0, "fps": 60.0},
                subtitle_path=srt_path,
            )
            self.assertIsNotNone(plan)
            self.assertGreater(len(plan.placements), 0)
            self.assertLessEqual(len(plan.placements), 11)  # Max density limit applied

            # Check that placements are sorted chronologically
            timestamps = [p.timestamp for p in plan.placements]
            self.assertEqual(timestamps, sorted(timestamps))

    def test_06_wav_trimming(self) -> None:
        """Test external WAV trimming function."""
        raw_wav = Path("C:/Users/warit/Desktop/davinci-katy-mcp/SFX/Bell - Ding 02.wav")
        if raw_wav.exists():
            out_wav = Path(tempfile.gettempdir()) / "test_ding_sting.wav"
            res = trim_wav(str(raw_wav), str(out_wav), duration_seconds=0.5)
            self.assertTrue(res.get("success"))
            self.assertTrue(out_wav.exists())
            self.assertLessEqual(res.get("duration_seconds", 0.0), 0.55)


if __name__ == "__main__":
    unittest.main()
