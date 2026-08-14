"""SFX Library Scanner & Indexer.

Scans raw and pre-processed SFX directories, extracts metadata,
classifies sound effects into families/categories, and maintains a cached library.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import wave
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from src.sfx_engine.config import SFXConfig
from src.sfx_engine.models import SFXCategory, SFXFile

logger = logging.getLogger(__name__)


# Family and Category Taxonomy mapping rules based on SKILL.md
TAXONOMY_RULES: List[Tuple[re.Pattern, str, SFXCategory, List[str]]] = [
    # Pattern, Family, Category, Tags
    (re.compile(r"pop", re.I), "pop", SFXCategory.COMEDY, ["pop", "short", "bubble", "punchline"]),
    (re.compile(r"blip", re.I), "blip", SFXCategory.COMEDY, ["blip", "silly", "marimba", "short"]),
    (re.compile(r"plink", re.I), "plink", SFXCategory.COMEDY, ["plink", "guitar", "slide", "funny"]),
    (re.compile(r"honk|duck", re.I), "honk", SFXCategory.COMEDY, ["honk", "horn", "duck", "silly"]),
    (re.compile(r"awkward", re.I), "awkward", SFXCategory.REACTION, ["awkward", "cricket", "moment", "pause"]),
    (re.compile(r"huh", re.I), "huh", SFXCategory.REACTION, ["huh", "confused", "voice", "question"]),
    (re.compile(r"awww", re.I), "awww", SFXCategory.REACTION, ["awww", "cute", "reaction", "crowd"]),
    (re.compile(r"ding|bell", re.I), "ding", SFXCategory.ACCENT, ["ding", "bell", "chime", "ting", "correct"]),
    (re.compile(r"collect", re.I), "collect", SFXCategory.SUCCESS, ["collect", "game", "pickup", "reward"]),
    (re.compile(r"kaching|cash", re.I), "kaching", SFXCategory.SUCCESS, ["kaching", "register", "money", "cash"]),
    (re.compile(r"sparkle|harp|magic|shimmer", re.I), "sparkle", SFXCategory.SUCCESS, ["sparkle", "harp", "magic", "shimmer"]),
    (re.compile(r"wrong", re.I), "wrong", SFXCategory.FAIL, ["wrong", "game", "error", "fail", "incorrect"]),
    (re.compile(r"scratch", re.I), "scratch", SFXCategory.FAIL, ["scratch", "record", "turntable", "stop"]),
    (re.compile(r"bleep|censor", re.I), "bleep", SFXCategory.FAIL, ["bleep", "censor", "beep"]),
    (re.compile(r"whoosh.*clean|whoosh-clean", re.I), "whoosh", SFXCategory.TRANSITION, ["whoosh", "clean", "fast", "swipe"]),
    (re.compile(r"whoosh.*fast|whoosh-fast", re.I), "whoosh", SFXCategory.TRANSITION, ["whoosh", "fast", "quick"]),
    (re.compile(r"whoosh.*intro|whoosh-intro|transition", re.I), "whoosh", SFXCategory.TRANSITION, ["whoosh", "intro", "transition"]),
    (re.compile(r"whoosh", re.I), "whoosh", SFXCategory.TRANSITION, ["whoosh", "air", "movement"]),
    (re.compile(r"rise|build", re.I), "rise", SFXCategory.DRAMATIC, ["rise", "buildup", "suspense", "tension"]),
    (re.compile(r"gong", re.I), "gong", SFXCategory.DRAMATIC, ["gong", "metal", "comical", "dramatic"]),
    (re.compile(r"impact|hit|punch|kung fu|stomp", re.I), "impact", SFXCategory.IMPACT, ["impact", "hit", "strike", "heavy"]),
    (re.compile(r"scream", re.I), "scream", SFXCategory.IMPACT, ["scream", "shout", "vocal", "fear"]),
    (re.compile(r"glass|shatter", re.I), "glass", SFXCategory.IMPACT, ["glass", "shatter", "break"]),
    (re.compile(r"click|button|mouse", re.I), "click", SFXCategory.UI, ["click", "button", "mouse", "ui"]),
    (re.compile(r"keyboard|typing", re.I), "keyboard", SFXCategory.UI, ["keyboard", "typing", "keys"]),
    (re.compile(r"digital|data|counter", re.I), "digital", SFXCategory.UI, ["digital", "data", "readout", "tech"]),
    (re.compile(r"cheer|crowd|applause", re.I), "crowd", SFXCategory.CROWD, ["crowd", "cheer", "applause", "kids"]),
]


class SFXLibrary:
    """Indexed container for SFX files."""

    def __init__(self, files: List[SFXFile]):
        self.files = files
        self._by_family: Dict[str, List[SFXFile]] = {}
        self._by_category: Dict[SFXCategory, List[SFXFile]] = {}
        self._by_filename: Dict[str, SFXFile] = {}

        self._build_indices()

    def _build_indices(self) -> None:
        """Index files by family, category, and filename."""
        for f in self.files:
            # By family
            family = f.family or "other"
            if family not in self._by_family:
                self._by_family[family] = []
            self._by_family[family].append(f)

            # By category
            cat = f.category
            if cat not in self._by_category:
                self._by_category[cat] = []
            self._by_category[cat].append(f)

            # By filename
            self._by_filename[f.filename] = f
            # Also index shortname if processed
            self._by_filename[f.name] = f

    def get_by_filename(self, filename: str) -> Optional[SFXFile]:
        """Get SFX file by filename or shortname."""
        return self._by_filename.get(filename)

    def get_by_family(self, family: str) -> List[SFXFile]:
        """Get all SFX files in a family."""
        return self._by_family.get(family, [])

    def get_by_category(self, category: SFXCategory) -> List[SFXFile]:
        """Get all SFX files in a category."""
        return self._by_category.get(category, [])

    def get_all_families(self) -> List[str]:
        """List all distinct families."""
        return list(self._by_family.keys())


class SFXScanner:
    """Scans SFX directories and builds/caches the SFX library index."""

    def __init__(self, config: Optional[SFXConfig] = None):
        self.config = config or SFXConfig.load()

    def scan(self, force_rescan: bool = False) -> SFXLibrary:
        """Scan configured directories and return indexed SFXLibrary.

        Tries loading from cache unless force_rescan is True.
        """
        if not force_rescan:
            cached = self._load_cache()
            if cached:
                logger.info("Loaded %d SFX files from cache", len(cached.files))
                return cached

        files: List[SFXFile] = []

        # 1. Scan processed directory first (preferred)
        proc_dir = Path(self.config.sfx_processed_dir)
        if proc_dir.exists() and proc_dir.is_dir():
            proc_files = self._scan_directory(proc_dir, is_processed=True)
            files.extend(proc_files)
            logger.info("Scanned %d files from processed dir %s", len(proc_files), proc_dir)

        # 2. Scan raw directory
        raw_dir = Path(self.config.sfx_raw_dir)
        if raw_dir.exists() and raw_dir.is_dir():
            raw_files = self._scan_directory(raw_dir, is_processed=False)
            files.extend(raw_files)
            logger.info("Scanned %d files from raw dir %s", len(raw_files), raw_dir)

        library = SFXLibrary(files)
        self._save_cache(library)
        return library

    def _scan_directory(self, directory: Path, is_processed: bool) -> List[SFXFile]:
        """Scan a single directory for wav and mp3 files."""
        sfx_files: List[SFXFile] = []

        for entry in directory.iterdir():
            if entry.is_file() and entry.suffix.lower() in (".wav", ".mp3"):
                sfx_file = self._parse_file(entry, is_processed)
                if sfx_file:
                    sfx_files.append(sfx_file)

        return sfx_files

    def _parse_file(self, path: Path, is_processed: bool) -> Optional[SFXFile]:
        """Parse file metadata and compute taxonomy classification."""
        filename = path.name
        ext = path.suffix.lower()
        size_bytes = path.stat().st_size

        # Parse processed filename structure: <shortname>-<dB>.wav or <shortname>-<dB>-sting.wav
        name = path.stem
        target_db: Optional[float] = None
        is_sting = False

        if is_processed:
            # Pattern e.g. pop-14.wav or whoosh-clean-12-sting.wav
            match = re.match(r"^(.+?)-(\d+)(?:-(sting))?$", path.stem, re.I)
            if match:
                short_name, db_str, sting_str = match.groups()
                name = short_name
                target_db = -float(db_str)
                is_sting = bool(sting_str)

        # Read audio properties (duration, sample rate)
        duration = 0.0
        sample_rate = 0
        channels = 0

        if ext == ".wav":
            try:
                with wave.open(str(path), "rb") as w:
                    frames = w.getnframes()
                    sample_rate = w.getframerate()
                    channels = w.getnchannels()
                    duration = frames / float(sample_rate) if sample_rate > 0 else 0.0
            except Exception as exc:
                logger.debug("Failed reading WAV metadata for %s: %s", filename, exc)
        else:
            # Rough estimate for MP3 based on bitrate ~128kbps if wave fails
            duration = (size_bytes * 8) / (128 * 1000)

        # Compute hash
        content_hash = hashlib.sha256(f"{filename}_{size_bytes}".encode("utf-8")).hexdigest()[:12]

        # Taxonomy matching
        family, category, tags = self._classify_taxonomy(filename)

        # Intensity heuristic
        intensity = "high" if (target_db and target_db >= -12) or "hit" in filename.lower() or "impact" in filename.lower() else "medium"

        return SFXFile(
            path=path,
            filename=filename,
            name=name,
            extension=ext,
            is_processed=is_processed,
            duration_seconds=round(duration, 3),
            sample_rate=sample_rate,
            channels=channels,
            file_size_bytes=size_bytes,
            target_db=target_db,
            category=category,
            tags=tags,
            family=family,
            intensity=intensity,
            is_sting=is_sting,
            content_hash=content_hash,
        )

    def _classify_taxonomy(self, filename: str) -> Tuple[str, SFXCategory, List[str]]:
        """Match filename against taxonomy rules."""
        for pattern, family, category, tags in TAXONOMY_RULES:
            if pattern.search(filename):
                return family, category, tags

        return "other", SFXCategory.ACCENT, ["sfx"]

    def _load_cache(self) -> Optional[SFXLibrary]:
        """Load library from cache file if available."""
        cache_dir = self.config.get_cache_path()
        if not cache_dir:
            return None

        cache_file = cache_dir / "sfx_library_cache.json"
        if not cache_file.exists():
            return None

        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            files = [SFXFile.from_dict(d) for d in data.get("files", [])]
            return SFXLibrary(files)
        except Exception as exc:
            logger.warning("Cache load failed: %s", exc)
            return None

    def _save_cache(self, library: SFXLibrary) -> None:
        """Save library to cache file."""
        cache_dir = self.config.get_cache_path()
        if not cache_dir:
            return

        cache_file = cache_dir / "sfx_library_cache.json"
        try:
            data = {
                "files": [f.to_dict() for f in library.files]
            }
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info("Saved SFX library cache to %s", cache_file)
        except Exception as exc:
            logger.warning("Failed saving cache: %s", exc)
