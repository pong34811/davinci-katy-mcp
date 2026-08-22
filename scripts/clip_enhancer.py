#!/usr/bin/env python3
"""Enhance a clip by reading subtitle track 1 and adding SFX automatically.

This is the main entry point that ties together:
1. Reading subtitles from DaVinci Resolve (or SRT file)
2. Analyzing content for emotions and beats
3. Generating an SFX plan
4. Placing SFX on the timeline

Usage:
    python scripts/clip_enhancer.py [--format talking-head] [--dry-run] [--verify]
    python scripts/clip_enhancer.py --srt subtitle_from_track1.srt [--format talking-head]
    python scripts/clip_enhancer.py --subtitles subtitles.json [--format talking-head]
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
MCP_DIR = os.path.join(REPO_ROOT, "davinci-resolve-mcp")
for _p in (REPO_ROOT, MCP_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

DEFAULT_SFX_DIR = r"C:\Users\warit\Desktop\davinci-katy-mcp\SFX"


def run_full_pipeline(
    clip_format: str = "talking-head",
    srt_path: Optional[str] = None,
    subtitles_json: Optional[str] = None,
    beats_json: Optional[str] = None,
    plan_json: str = "plan.json",
    dry_run: bool = False,
    verify: bool = False,
    sfx_dir: str = DEFAULT_SFX_DIR,
    skip_place: bool = False,
) -> int:
    """Run the full subtitle-driven enhancement pipeline."""
    from analyze_subtitles import (
        analyze_subtitles,
        read_subtitles_from_resolve,
        read_subtitles_from_srt,
        format_beats_table,
    )
    from generate_sfx_plan import generate_plan, FORMAT_CONFIGS

    print("=" * 60)
    print("  Subtitle-Driven Clip Enhancement")
    print("=" * 60)

    # ── Step 1: Read Subtitles ──────────────────────────────────────────
    print("\n[Step 1] Reading subtitles...")
    subtitles = []

    if srt_path:
        subtitles = read_subtitles_from_srt(srt_path)
    elif subtitles_json:
        with open(subtitles_json, "r", encoding="utf-8") as f:
            subtitles = json.load(f)
    elif beats_json:
        # Skip to step 2 if beats already exist
        print(f"  Loading existing beats from {beats_json}")
        with open(beats_json, "r", encoding="utf-8") as f:
            beats = json.load(f)
        subtitles = beats  # Use beats as subtitles for step 2
    else:
        subtitles = read_subtitles_from_resolve()

    if not subtitles:
        print("ERROR: No subtitles found.", file=sys.stderr)
        return 1

    print(f"  Found {len(subtitles)} subtitle segments")

    # ── Step 2: Analyze Content ─────────────────────────────────────────
    print("\n[Step 2] Analyzing content...")
    if beats_json:
        # Beats already loaded
        pass
    else:
        beats = analyze_subtitles(subtitles)
        print(format_beats_table(beats))

        # Save beats
        beats_path = "subtitles_beats.json"
        with open(beats_path, "w", encoding="utf-8") as f:
            json.dump(beats, f, ensure_ascii=False, indent=2)
        print(f"\n  Saved beats to {beats_path}")

    # Summary
    non_neutral = [b for b in beats if b.get("beat_type", "neutral") != "neutral"]
    high_priority = [b for b in beats if b.get("priority", 0) >= 2]
    print(f"\n  Analysis summary:")
    print(f"    Total segments: {len(beats)}")
    print(f"    Segments with beats: {len(non_neutral)}")
    print(f"    High priority: {len(high_priority)}")

    # ── Step 3: Generate SFX Plan ───────────────────────────────────────
    print("\n[Step 3] Generating SFX plan...")
    config = FORMAT_CONFIGS.get(clip_format, FORMAT_CONFIGS["talking-head"])
    print(f"  Format: {config['description']}")
    print(f"  Density target: {config['density_per_minute']}/min")

    plan, warnings = generate_plan(beats, clip_format, sfx_dir)

    for w in warnings:
        print(f"  WARNING: {w}")

    # Save plan
    with open(plan_json, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)

    print(f"\n  Plan summary:")
    print(f"    SFX count: {plan['sfx_count']}")
    print(f"    Duration: {plan['duration_seconds']:.1f}s")
    if plan['duration_seconds'] > 0:
        density = plan['sfx_count'] / plan['duration_seconds'] * 60
        print(f"    Actual density: {density:.1f}/min")
    print(f"    Saved to: {plan_json}")

    if plan["sfx"]:
        print(f"\n  Planned SFX:")
        for s in plan["sfx"]:
            print(f"    {s['timestamp_seconds']:.2f}s: {s['sfx_file']} ({s['reason'][:60]})")

    # ── Step 4: Place SFX ───────────────────────────────────────────────
    if skip_place:
        print(f"\n[Step 4] Skipping placement (--skip-place)")
        print(f"  Plan saved to {plan_json}")
        print(f"  To place: python scripts/sfx_place.py --plan {plan_json} --verify")
        return 0

    print(f"\n[Step 4] Placing SFX on timeline...")
    if dry_run:
        print("  DRY RUN mode - validating plan only")

    # Build command for sfx_place.py
    sfx_place_cmd = [
        sys.executable,
        os.path.join(SCRIPT_DIR, "sfx_place.py"),
        "--plan", plan_json,
        "--raw-dir", sfx_dir,
    ]
    if dry_run:
        sfx_place_cmd.append("--dry-run")
    if verify:
        sfx_place_cmd.append("--verify")

    print(f"  Running: {' '.join(sfx_place_cmd)}")

    # Execute
    import subprocess
    result = subprocess.run(sfx_place_cmd, capture_output=False)

    if result.returncode == 0:
        print(f"\n{'=' * 60}")
        print(f"  Enhancement complete!")
        print(f"{'=' * 60}")
    else:
        print(f"\n{'=' * 60}")
        print(f"  Enhancement failed (exit code: {result.returncode})")
        print(f"{'=' * 60}")

    return result.returncode


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Enhance a clip by reading subtitle track 1 and adding SFX."
    )
    parser.add_argument(
        "--format",
        choices=["talking-head", "game", "meme", "podcast", "livestream"],
        default="talking-head",
        help="clip format (default: talking-head)",
    )
    parser.add_argument(
        "--srt",
        help="path to SRT subtitle file",
    )
    parser.add_argument(
        "--subtitles",
        help="path to subtitles JSON file",
    )
    parser.add_argument(
        "--beats",
        help="path to existing beats JSON (skip analysis step)",
    )
    parser.add_argument(
        "--output",
        default="plan.json",
        help="output plan JSON path (default: plan.json)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate plan without placing SFX",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="verify placement after placing SFX",
    )
    parser.add_argument(
        "--skip-place",
        action="store_true",
        help="generate plan only, don't place SFX",
    )
    parser.add_argument(
        "--sfx-dir",
        default=DEFAULT_SFX_DIR,
        help="path to SFX directory",
    )
    args = parser.parse_args(argv)

    return run_full_pipeline(
        clip_format=args.format,
        srt_path=args.srt,
        subtitles_json=args.subtitles,
        beats_json=args.beats,
        plan_json=args.output,
        dry_run=args.dry_run,
        verify=args.verify,
        sfx_dir=args.sfx_dir,
        skip_place=args.skip_place,
    )


if __name__ == "__main__":
    sys.exit(main())
