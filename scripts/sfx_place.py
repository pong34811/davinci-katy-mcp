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
    with open(path, "r", encoding="utf-8-sig") as f:
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


def _connect_resolve() -> Optional[Tuple[Any, Any, Any, Any]]:
    """Connect to the running DaVinci Resolve app. Returns (resolve, project, media_pool, timeline)."""
    from src.utils.platform import get_resolve_paths

    paths = get_resolve_paths()
    os.environ.setdefault("RESOLVE_SCRIPT_API", paths["api_path"])
    os.environ.setdefault("RESOLVE_SCRIPT_LIB", paths["lib_path"])
    modules = paths["modules_path"]
    if modules not in sys.path:
        sys.path.append(modules)

    try:
        import DaVinciResolveScript as dvr
    except ImportError:
        print("ERROR: cannot import DaVinciResolveScript; is Resolve's Scripting module installed?")
        return None
    resolve = dvr.scriptapp("Resolve")
    if resolve is None:
        print("ERROR: cannot connect to Resolve. Is it running?")
        return None
    project = resolve.GetProjectManager().GetCurrentProject()
    if project is None:
        print("ERROR: no project open.")
        return None
    media_pool = project.GetMediaPool()
    timeline = project.GetCurrentTimeline()
    if timeline is None:
        print("ERROR: no timeline open.")
        return None
    return resolve, project, media_pool, timeline


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Place an SFX plan onto the DaVinci Resolve timeline."
    )
    parser.add_argument("--plan", required=True, help="path to plan JSON")
    parser.add_argument("--dry-run", action="store_true",
                        help="validate the plan without touching Resolve")
    parser.add_argument("--verify", action="store_true",
                        help="run placement readback verification after placing")
    parser.add_argument("--raw-dir", default=DEFAULT_RAW_DIR)
    parser.add_argument("--processed-dir", default=DEFAULT_PROCESSED_DIR)
    parser.add_argument("--track-name", default="SFX 1")
    args = parser.parse_args(argv)

    try:
        plan = load_plan(args.plan)
    except (json.JSONDecodeError, ValueError, OSError) as exc:
        print(f"ERROR: cannot load plan: {exc}")
        return 2

    errors, warnings = validate_plan(
        plan, args.raw_dir, args.processed_dir, timeline_duration=None
    )
    for w in warnings:
        print(f"WARN: {w}")
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 2

    placements = build_placements(plan, args.raw_dir, args.processed_dir)
    print(f"PLAN OK: {len(placements)} SFX to place")
    for p in placements:
        print(f"  {os.path.basename(p['sfx_path'])} @ {p['timestamp_seconds']:.2f}s "
              f"({p['duration_seconds']}s) — {p['reason']}")

    if args.dry_run:
        return 0

    conn = _connect_resolve()
    if conn is None:
        return 3
    resolve, project, media_pool, timeline = conn

    try:
        from src.sfx_engine.placer import SFXPlacer
    except ImportError as exc:
        print(f"ERROR: cannot import SFX engine: {exc}")
        return 3
    placer = SFXPlacer(resolve, project, timeline, media_pool)
    report = placer.execute_plan(placements, sfx_track_name=args.track_name)

    print(f"\n=== RESULT: {report.total_placed}/{report.total_planned} placed "
          f"(failed {report.total_failed}) on track {report.track_index} ===")
    for r in report.results:
        status = "OK" if r.success else f"FAIL: {r.error}"
        print(f"  {r.sfx_filename} @ {r.target_seconds:.2f}s "
              f"-> track {r.track_index} frame {r.actual_frame or r.target_frame} [{status}]")
    for e in report.errors:
        print(f"ERROR: {e}")

    if args.verify:
        verify = placer.verify_placements()
        print(f"\n=== VERIFY: success={verify['success']} items={verify['total_items']} "
              f"issues={len(verify['issues'])} ===")
        for issue in verify["issues"]:
            print(f"  ISSUE: {issue}")

    return 0 if report.total_failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
