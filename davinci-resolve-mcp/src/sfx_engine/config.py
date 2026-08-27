"""SFX Engine configuration management.

Centralized configuration for the DaVinci Resolve SFX Skill system.
Supports loading from JSON file and environment variables.
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# Default SFX library paths (ponytail: single source of truth lives in scripts/config.py)
import os as _os
_DEFAULT_SFX_RAW = _os.path.join(
    _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))),
    "SFX",
)
DEFAULT_SFX_RAW_DIR = _DEFAULT_SFX_RAW
DEFAULT_SFX_PROCESSED_DIR = _DEFAULT_SFX_RAW  # ponytail: no SFX_processed dir on this machine, both point to SFX/


@dataclass
class FormatDensity:
    """SFX density limits for a content format (per minute)."""
    min_per_minute: float
    max_per_minute: float


@dataclass
class SFXConfig:
    """Configuration for the SFX engine.

    All paths and thresholds are configurable. The defaults match the
    existing project conventions documented in SKILL.md.
    """

    # ── Library Paths ────────────────────────────────────────────────
    sfx_raw_dir: str = DEFAULT_SFX_RAW_DIR
    sfx_processed_dir: str = DEFAULT_SFX_PROCESSED_DIR

    # ── Timeline Defaults ────────────────────────────────────────────
    default_fps: float = 60.0
    default_sfx_track_name: str = "SFX 1"

    # ── Placement Constraints ────────────────────────────────────────
    min_spacing_seconds: float = 1.0
    default_sting_duration_seconds: float = 0.5
    max_sfx_duration_seconds: float = 2.0

    # ── Volume Settings (dB relative to bed) ─────────────────────────
    sfx_volume_db_min: float = -16.0
    sfx_volume_db_max: float = -10.0
    default_volume_db: float = -14.0

    # ── Fade Settings ────────────────────────────────────────────────
    default_fade_out_seconds: float = 0.03
    default_fade_in_seconds: float = 0.0

    # ── Format-Specific Density Limits ───────────────────────────────
    density_limits: Dict[str, Dict[str, float]] = field(default_factory=lambda: {
        "talking_head": {"min": 3.0, "max": 5.0},
        "podcast": {"min": 0.0, "max": 2.0},
        "game": {"min": 5.0, "max": 8.0},
        "meme": {"min": 5.0, "max": 15.0},
        "livestream": {"min": 0.0, "max": 3.0},
    })

    # ── Cache Settings ───────────────────────────────────────────────
    cache_dir: Optional[str] = None
    cache_ttl_hours: int = 24

    # ── Media Pool ───────────────────────────────────────────────────
    sfx_bin_path: str = "Master/SFX"

    def get_density_limit(self, format_name: str) -> FormatDensity:
        """Get density limits for a content format.

        Args:
            format_name: One of 'talking_head', 'podcast', 'game', 'meme', 'livestream'.

        Returns:
            FormatDensity with min/max per-minute limits.
        """
        limits = self.density_limits.get(format_name, {"min": 3.0, "max": 5.0})
        return FormatDensity(
            min_per_minute=limits.get("min", 3.0),
            max_per_minute=limits.get("max", 5.0),
        )

    def get_cache_path(self) -> Optional[Path]:
        """Get the cache directory path, creating it if needed."""
        if self.cache_dir:
            path = Path(self.cache_dir)
            path.mkdir(parents=True, exist_ok=True)
            return path
        return None

    @classmethod
    def load(cls, path: Optional[str] = None) -> SFXConfig:
        """Load configuration from a JSON file.

        Falls back to environment variables and then defaults.

        Args:
            path: Path to a JSON config file. If None, looks for
                  SFX_CONFIG_PATH env var or uses defaults.

        Returns:
            SFXConfig instance.
        """
        config = cls()

        # Try to load from file
        config_path = path or os.environ.get("SFX_CONFIG_PATH")
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                config = cls._from_dict(data)
                logger.info("Loaded SFX config from %s", config_path)
            except (json.JSONDecodeError, OSError) as exc:
                logger.warning("Failed to load config from %s: %s", config_path, exc)

        # Override with environment variables
        if os.environ.get("SFX_RAW_DIR"):
            config.sfx_raw_dir = os.environ["SFX_RAW_DIR"]
        if os.environ.get("SFX_PROCESSED_DIR"):
            config.sfx_processed_dir = os.environ["SFX_PROCESSED_DIR"]
        if os.environ.get("SFX_DEFAULT_FPS"):
            config.default_fps = float(os.environ["SFX_DEFAULT_FPS"])
        if os.environ.get("SFX_CACHE_DIR"):
            config.cache_dir = os.environ["SFX_CACHE_DIR"]

        return config

    @classmethod
    def _from_dict(cls, data: Dict[str, Any]) -> SFXConfig:
        """Create config from a dictionary."""
        config = cls()
        for key, value in data.items():
            if hasattr(config, key):
                setattr(config, key, value)
        return config

    def save(self, path: str) -> None:
        """Save configuration to a JSON file.

        Args:
            path: Target file path.
        """
        data = {
            "sfx_raw_dir": self.sfx_raw_dir,
            "sfx_processed_dir": self.sfx_processed_dir,
            "default_fps": self.default_fps,
            "default_sfx_track_name": self.default_sfx_track_name,
            "min_spacing_seconds": self.min_spacing_seconds,
            "default_sting_duration_seconds": self.default_sting_duration_seconds,
            "max_sfx_duration_seconds": self.max_sfx_duration_seconds,
            "sfx_volume_db_min": self.sfx_volume_db_min,
            "sfx_volume_db_max": self.sfx_volume_db_max,
            "default_volume_db": self.default_volume_db,
            "default_fade_out_seconds": self.default_fade_out_seconds,
            "default_fade_in_seconds": self.default_fade_in_seconds,
            "density_limits": self.density_limits,
            "cache_dir": self.cache_dir,
            "cache_ttl_hours": self.cache_ttl_hours,
            "sfx_bin_path": self.sfx_bin_path,
        }
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info("Saved SFX config to %s", path)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "sfx_raw_dir": self.sfx_raw_dir,
            "sfx_processed_dir": self.sfx_processed_dir,
            "default_fps": self.default_fps,
            "default_sfx_track_name": self.default_sfx_track_name,
            "min_spacing_seconds": self.min_spacing_seconds,
            "default_sting_duration_seconds": self.default_sting_duration_seconds,
            "max_sfx_duration_seconds": self.max_sfx_duration_seconds,
            "sfx_volume_db_min": self.sfx_volume_db_min,
            "sfx_volume_db_max": self.sfx_volume_db_max,
            "default_volume_db": self.default_volume_db,
            "density_limits": self.density_limits,
            "cache_dir": self.cache_dir,
        }
