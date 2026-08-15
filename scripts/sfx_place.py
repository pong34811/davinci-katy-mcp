#!/usr/bin/env python3
"""Place an SFX plan onto the DaVinci Resolve timeline via the SFX engine.

Usage:
    python scripts/sfx_place.py --plan plan.json [--verify] [--dry-run] \
        [--raw-dir Z:/SFX] [--processed-dir Z:/SFX_processed]
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional, Tuple

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
MCP_DIR = os.path.join(REPO_ROOT, "davinci-resolve-mcp")
for _p in (REPO_ROOT, MCP_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

DEFAULT_RAW_DIR = "Z:/SFX"
DEFAULT_PROCESSED_DIR = "Z:/SFX_processed"
MIN_SPACING_SECONDS = 1.0
DEFAULT_DURATION_SECONDS = 0.5


def load_plan(path: str) -> Dict[str, Any]:
    """Load a plan JSON file. Raises ValueError if it has no 'sfx' key."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict) or "sfx" not in data:
        raise ValueError("plan must be a JSON object with an 'sfx' list")
    return data


def resolve_path(
    name: str, raw_dir: str, processed_dir: str
) -> Optional[str]:
    """Resolve a basename to a full path, processed dir first."""
    for base in (processed_dir, raw_dir):
        candidate = os.path.join(base, name)
        if os.path.isfile(candidate):
            return candidate
    return None


def validate_plan(
    plan: Dict[str, Any],
    raw_dir: str,
    processed_dir: str,
    timeline_duration: Optional[float] = None,
) -> Tuple[List[str], List[str]]:
    """Validate a plan. Returns (errors, warnings)."""
    errors: List[str] = []
    warnings: List[str] = []
    sfx = plan.get("sfx", [])
    if not sfx:
        return ["plan has no 'sfx' entries"], []

    timestamps: List[float] = []
    for i, entry in enumerate(sfx):
        name = entry.get("sfx_file", "")
        tag = f"[{i}] {name or '<no file>'}"
        if not name:
            errors.append(f"{tag}: missing 'sfx_file'")
            continue
        if resolve_path(name, raw_dir, processed_dir) is None:
            errors.append(f"{tag}: file not found in raw/processed dirs")

        ts = entry.get("timestamp_seconds")
        if not isinstance(ts, (int, float)):
            errors.append(f"{tag}: timestamp_seconds must be a number")
        else:
            if ts < 0:
                errors.append(f"{tag}: timestamp_seconds must be >= 0")
            if timeline_duration is not None and ts > timeline_duration:
                errors.append(
                    f"{tag}: timestamp {ts}s is past timeline end "
                    f"({timeline_duration}s)"
                )
            timestamps.append(float(ts))

        dur = entry.get("duration", DEFAULT_DURATION_SECONDS)
        if not isinstance(dur, (int, float)) or dur <= 0:
            errors.append(f"{tag}: duration must be a positive number")

        if not entry.get("reason"):
            warnings.append(f"{tag}: missing 'reason' (rule: every SFX needs one)")

    # Spacing: no two SFX closer than 1s
    timestamps.sort()
    for a, b in zip(timestamps, timestamps[1:]):
        if b - a < MIN_SPACING_SECONDS:
            warnings.append(
                f"spacing: {a:.2f}s and {b:.2f}s are closer than "
                f"{MIN_SPACING_SECONDS}s"
            )
    return errors, warnings


def build_placements(
    plan: Dict[str, Any], raw_dir: str, processed_dir: str
) -> List[Dict[str, Any]]:
    """Convert a plan into SFXPlacer.execute_plan placement dicts."""
    placements: List[Dict[str, Any]] = []
    for entry in plan.get("sfx", []):
        name = entry.get("sfx_file", "")
        full = resolve_path(name, raw_dir, processed_dir)
        if full is None:
            continue
        placements.append({
            "sfx_path": full,
            "timestamp_seconds": float(entry.get("timestamp_seconds", 0.0)),
            "duration_seconds": float(entry.get("duration", DEFAULT_DURATION_SECONDS)),
            "reason": entry.get("reason", ""),
        })
    return placements
