#!/usr/bin/env python3
"""Generate an SFX plan from subtitle beat analysis.

Usage:
    python scripts/generate_sfx_plan.py --beats beats.json [--format talking-head] [--output plan.json]
    python scripts/generate_sfx_plan.py --subtitles subtitles.json [--format talking-head] [--output plan.json]
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

# Import from config
from config import (
    SFX_DIR as DEFAULT_SFX_DIR,
    SFX_FAMILIES,
    BEAT_TO_SFX,
    FORMAT_CONFIGS,
    MIN_SPACING_SECONDS,
    get_sfx_file as _get_sfx_file_config,
)

# Use imported configs directly - no local duplicates
# All config values are now single-sourced from config.py


# ── Plan Generator ──────────────────────────────────────────────────────────

def get_sfx_file(family: str, sfx_dir: str) -> Optional[str]:
    """Get the first available SFX file from a family."""
    candidates = SFX_FAMILIES.get(family, [])
    for name in candidates:
        path = os.path.join(sfx_dir, name)
        if os.path.isfile(path):
            return name
    return None


def check_spacing(timestamps: List[float], min_spacing: float = MIN_SPACING_SECONDS) -> List[str]:
    """Check for spacing violations."""
    warnings = []
    sorted_ts = sorted(timestamps)
    for i, (a, b) in enumerate(zip(sorted_ts, sorted_ts[1:])):
        if b - a < min_spacing:
            warnings.append(
                f"Spacing violation: {a:.2f}s and {b:.2f}s are {b-a:.2f}s apart "
                f"(minimum {min_spacing}s)"
            )
    return warnings


def check_family_repetition(sfx_files: List[str], min_distance: int = 3) -> List[str]:
    """Check for same-family SFX too close together."""
    warnings = []
    # Map file to family
    file_to_family = {}
    for family, files in SFX_FAMILIES.items():
        for f in files:
            file_to_family[f] = family

    families = [file_to_family.get(f, f) for f in sfx_files]
    for i, fam in enumerate(families):
        for j in range(max(0, i - min_distance), i):
            if families[j] == fam and fam != "neutral":
                warnings.append(
                    f"Family repetition: '{fam}' used at index {j} and {i} "
                    f"({min_distance} positions apart)"
                )
    return warnings


def generate_plan(
    beats: List[Dict[str, Any]],
    clip_format: str = "talking-head",
    sfx_dir: str = DEFAULT_SFX_DIR,
) -> Tuple[Dict[str, Any], List[str]]:
    """Generate an SFX plan from analyzed beats.

    Returns (plan, warnings).
    """
    config = FORMAT_CONFIGS.get(clip_format, FORMAT_CONFIGS["talking-head"])
    warnings = []

    # Calculate duration
    if beats:
        duration = max(b.get("end_seconds", 0) for b in beats)
    else:
        duration = 0

    # Calculate max SFX count based on density
    max_sfx = int(duration / 60 * config["density_per_minute"]) + 1

    # Filter to non-neutral beats with suggestions
    candidates = [b for b in beats if b.get("sfx_suggestion") and b.get("beat_type") != "neutral"]

    # Sort by priority (high first), then by timestamp
    candidates.sort(key=lambda b: (-b.get("priority", 0), b.get("start_seconds", 0)))

    # Select SFX, respecting spacing and family repetition
    plan_sfx = []
    used_families = []
    used_timestamps = []

    for beat in candidates:
        if len(plan_sfx) >= max_sfx:
            warnings.append(f" density cap reached ({max_sfx} SFX for {duration:.0f}s clip)")
            break

        ts = beat.get("start_seconds", 0)
        sfx_family = beat.get("sfx_suggestion", "")

        # Check spacing
        too_close = any(abs(ts - ut) < MIN_SPACING_SECONDS for ut in used_timestamps)
        if too_close:
            continue

        # Check family repetition (last 3)
        recent_families = used_families[-3:]
        if sfx_family in recent_families:
            # Try alternate family
            alt_families = BEAT_TO_SFX.get(beat.get("beat_type", ""), [])
            found_alt = False
            for alt in alt_families:
                if alt != sfx_family and alt not in recent_families:
                    sfx_family = alt
                    found_alt = True
                    break
            if not found_alt:
                continue

        # Get actual file
        sfx_file = get_sfx_file(sfx_family, sfx_dir)
        if not sfx_file:
            warnings.append(f"No file found for family '{sfx_family}' at {ts:.2f}s")
            continue

        plan_sfx.append({
            "sfx_file": sfx_file,
            "timestamp_seconds": ts,
            "duration": 0.5,
            "reason": f"{beat.get('beat_type', 'unknown')} - {beat.get('text', '')[:40]}",
            "beat_type": beat.get("beat_type"),
            "priority": beat.get("priority", 0),
        })
        used_families.append(sfx_family)
        used_timestamps.append(ts)

    # Check spacing violations
    spacing_warnings = check_spacing(used_timestamps)
    warnings.extend(spacing_warnings)

    # Check family repetition
    family_warnings = check_family_repetition([s["sfx_file"] for s in plan_sfx])
    warnings.extend(family_warnings)

    plan = {
        "format": clip_format,
        "duration_seconds": duration,
        "density_per_minute": config["density_per_minute"],
        "sfx_count": len(plan_sfx),
        "sfx": plan_sfx,
    }

    return plan, warnings


# ── Main ────────────────────────────────────────────────────────────────────

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate an SFX plan from subtitle beat analysis."
    )
    parser.add_argument(
        "--beats",
        help="path to beats JSON file (from analyze_subtitles.py)",
    )
    parser.add_argument(
        "--subtitles",
        help="path to subtitles JSON file (will analyze first)",
    )
    parser.add_argument(
        "--format",
        choices=list(FORMAT_CONFIGS.keys()),
        default="talking-head",
        help="clip format (default: talking-head)",
    )
    parser.add_argument(
        "--output",
        default="plan.json",
        help="output plan JSON path (default: plan.json)",
    )
    parser.add_argument(
        "--sfx-dir",
        default=DEFAULT_SFX_DIR,
        help="path to SFX directory",
    )
    args = parser.parse_args(argv)

    if not args.beats and not args.subtitles:
        print("ERROR: Provide --beats or --subtitles", file=sys.stderr)
        return 1

    # Load or generate beats
    beats = []
    if args.beats:
        with open(args.beats, "r", encoding="utf-8") as f:
            beats = json.load(f)
    elif args.subtitles:
        sys.path.insert(0, SCRIPT_DIR)
        from analyze_subtitles import analyze_subtitles, read_subtitles_from_srt

        if args.subtitles.endswith(".srt"):
            subs = read_subtitles_from_srt(args.subtitles)
        else:
            with open(args.subtitles, "r", encoding="utf-8") as f:
                subs = json.load(f)
        beats = analyze_subtitles(subs)

    if not beats:
        print("ERROR: No beats to generate plan from.", file=sys.stderr)
        return 1

    # Generate plan
    config = FORMAT_CONFIGS[args.format]
    print(f"Generating SFX plan for format: {config['description']}")
    print(f"  Density: {config['density_per_minute']}/min, Volume: {config['sfx_volume_db']}dB")
    print(f"  SFX directory: {args.sfx_dir}")

    plan, warnings = generate_plan(beats, args.format, args.sfx_dir)

    # Print warnings
    for w in warnings:
        print(f"  WARNING: {w}")

    # Save plan
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)

    print(f"\n=== Plan Generated ===")
    print(f"  SFX count: {plan['sfx_count']}")
    print(f"  Duration: {plan['duration_seconds']:.1f}s")
    print(f"  Density: {plan['sfx_count'] / max(plan['duration_seconds'], 1) * 60:.1f}/min")
    print(f"  Saved to: {args.output}")

    if plan["sfx"]:
        print(f"\n  SFX placements:")
        for s in plan["sfx"]:
            print(f"    {s['timestamp_seconds']:.2f}s: {s['sfx_file']} ({s['reason'][:50]})")

    return 0


if __name__ == "__main__":
    sys.exit(main())
