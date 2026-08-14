"""Data models for the SFX Engine.

Defines all data structures for categories, event types, audio files,
placements, search results, timeline events, and recommendation plans.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class SFXCategory(str, Enum):
    """Categories of Sound Effects."""
    COMEDY = "comedy"           # pop, blip, plink, honk, marimba
    REACTION = "reaction"       # awkward, huh, awww
    IMPACT = "impact"           # impact, scream, glass
    ACCENT = "accent"           # ding, pop, collect, sparkle
    FAIL = "fail"               # wrong, scratch, bleep
    TRANSITION = "transition"   # whoosh variants, rise
    SUCCESS = "success"         # collect, kaching, ding, crowd-cheer
    DRAMATIC = "dramatic"       # rise, gong, metal, glitch
    ACTION = "action"           # impact, whoosh, explosion, stomp
    UI = "ui"                   # click, UI-enter, digital, keyboard
    MUSIC = "music"             # harp, guitar, marimba stingers
    CROWD = "crowd"             # crowd noises, cheers, applause
    WHOOSH = "whoosh"           # clean, fast, intro whooshes


class EventType(str, Enum):
    """Types of video/audio events requiring SFX."""
    JOKE = "joke"               # มุก / punchline
    REACTION = "reaction"       # อึ้ง/งง/เขิน
    SURPRISE = "surprise"       # ตกใจ / เซอร์ไพรส์
    EMPHASIS = "emphasis"       # เน้นคำ/ข้อความสำคัญ
    FAIL = "fail"               # พลาด / ไม่ทัน
    TRANSITION = "transition"   # เปลี่ยน scene
    SUCCESS = "success"         # สำเร็จ / ได้ของ
    DRAMATIC = "dramatic"       # Dramatic / suspense
    ACTION = "action"           # Visual action ใหญ่
    UI_NOTIFICATION = "ui"      # UI / notification
    INTRO = "intro"             # Opening / intro
    OUTRO = "outro"             # Closing / outro


class ContentFormat(str, Enum):
    """Video content format classification."""
    TALKING_HEAD = "talking_head"  # Vlog, single speaker talking
    PODCAST = "podcast"            # Long form multi-speaker dialogue
    GAME = "game"                  # Gameplay, action, kills, alerts
    MEME = "meme"                  # Short video, high density meme edits
    LIVESTREAM = "livestream"      # Long stream, alert-driven


@dataclass
class SFXFile:
    """Represents a single SFX audio file with extracted metadata."""
    path: Path
    filename: str
    name: str                     # Human-readable short name
    extension: str                # .wav, .mp3
    is_processed: bool            # True if from SFX_processed

    # Audio properties
    duration_seconds: float = 0.0
    sample_rate: int = 0
    channels: int = 0
    file_size_bytes: int = 0

    # Volume & Loudness
    target_db: Optional[float] = None  # Level specified in processed filename (e.g. -14)
    peak_db: Optional[float] = None
    rms_db: Optional[float] = None

    # Classifications & Taxonomy
    category: SFXCategory = SFXCategory.ACCENT
    tags: List[str] = field(default_factory=list)
    family: str = ""              # e.g. "whoosh", "pop", "ding", "honk"
    intensity: str = "medium"     # low, medium, high

    # Sting properties
    is_sting: bool = False
    sting_path: Optional[Path] = None

    # Hash for caching
    content_hash: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert object to dict representation."""
        return {
            "path": str(self.path),
            "filename": self.filename,
            "name": self.name,
            "extension": self.extension,
            "is_processed": self.is_processed,
            "duration_seconds": round(self.duration_seconds, 3),
            "sample_rate": self.sample_rate,
            "channels": self.channels,
            "file_size_bytes": self.file_size_bytes,
            "target_db": self.target_db,
            "category": self.category.value if isinstance(self.category, SFXCategory) else self.category,
            "tags": self.tags,
            "family": self.family,
            "intensity": self.intensity,
            "is_sting": self.is_sting,
            "sting_path": str(self.sting_path) if self.sting_path else None,
            "content_hash": self.content_hash,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SFXFile:
        """Construct object from dict."""
        cat = data.get("category", SFXCategory.ACCENT)
        if isinstance(cat, str):
            try:
                cat = SFXCategory(cat)
            except ValueError:
                cat = SFXCategory.ACCENT

        return cls(
            path=Path(data["path"]),
            filename=data["filename"],
            name=data["name"],
            extension=data["extension"],
            is_processed=data.get("is_processed", False),
            duration_seconds=data.get("duration_seconds", 0.0),
            sample_rate=data.get("sample_rate", 0),
            channels=data.get("channels", 0),
            file_size_bytes=data.get("file_size_bytes", 0),
            target_db=data.get("target_db"),
            category=cat,
            tags=data.get("tags", []),
            family=data.get("family", ""),
            intensity=data.get("intensity", "medium"),
            is_sting=data.get("is_sting", False),
            sting_path=Path(data["sting_path"]) if data.get("sting_path") else None,
            content_hash=data.get("content_hash", ""),
        )


@dataclass
class SFXSearchResult:
    """SearchResult container with matching score."""
    file: SFXFile
    score: float


@dataclass
class TimelineEvent:
    """An identified event on the video timeline requiring SFX consideration."""
    type: EventType
    timestamp: float
    description: str
    impact_score: float = 0.5  # 0.0 to 1.0 importance
    duration: float = 0.0
    text_snippet: Optional[str] = None


@dataclass
class BeatPoint:
    """A scored beat point extracted for potential SFX alignment."""
    timestamp: float
    event_type: EventType
    impact_score: float
    description: str


@dataclass
class SFXPlacement:
    """Represents a planned SFX placement on the timeline."""
    sfx: SFXFile
    timestamp: float
    beat: BeatPoint
    volume_db: float = -14.0
    record_frame: int = 0
    duration_seconds: float = 0.5
    track_index: int = 2
    confidence: float = 0.8
    reason: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert object to dict representation."""
        return {
            "sfx_path": str(self.sfx.path),
            "sfx_filename": self.sfx.filename,
            "sfx_family": self.sfx.family,
            "timestamp_seconds": round(self.timestamp, 3),
            "record_frame": self.record_frame,
            "duration_seconds": round(self.duration_seconds, 3),
            "volume_db": self.volume_db,
            "track_index": self.track_index,
            "event_type": self.beat.event_type.value if hasattr(self.beat.event_type, "value") else str(self.beat.event_type),
            "reason": self.reason or self.beat.description,
            "confidence": round(self.confidence, 2),
        }


@dataclass
class SFXPlan:
    """Complete SFX recommendation plan for a video timeline."""
    format: ContentFormat
    placements: List[SFXPlacement]
    timeline_duration_seconds: float = 0.0
    fps: float = 60.0
    density_per_minute: float = 0.0
    warnings: List[str] = field(default_factory=list)
    spacing_violations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert plan to dictionary structure."""
        return {
            "format": self.format.value if hasattr(self.format, "value") else str(self.format),
            "timeline_duration_seconds": round(self.timeline_duration_seconds, 2),
            "fps": self.fps,
            "total_sfx_count": len(self.placements),
            "density_per_minute": round(self.density_per_minute, 2),
            "placements": [p.to_dict() for p in self.placements],
            "warnings": self.warnings,
            "spacing_violations": self.spacing_violations,
        }
