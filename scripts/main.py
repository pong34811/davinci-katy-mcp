#!/usr/bin/env python3
"""
DaVinci Resolve SFX Enhancement System — Entry Point

Usage:
    python scripts/main.py status                    # Show system status
    python scripts/main.py analyze --srt <srt_file>  # Analyze subtitle
    python scripts/main.py plan --format <format>    # Create SFX plan
    python scripts/main.py place --plan <plan.json>  # Place SFX
    python scripts/main.py enhance --srt <srt_file>  # Full pipeline
"""

import sys
import os

# Ensure venv python is used
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import get_system_status, get_srt_source


def cmd_status():
    """Show system status."""
    status = get_system_status()
    print(status)


def cmd_analyze(srt_file):
    """Analyze subtitle file."""
    from analyze_subtitles import analyze_subtitles
    srt_path = srt_file or get_srt_source()
    print(f"Analyzing: {srt_path}")
    result = analyze_subtitles(srt_path)
    print(f"Result: {len(result)} segments found")


def cmd_plan(format_type="talking-head"):
    """Create SFX plan."""
    from generate_sfx_plan import generate_sfx_plan
    beats = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "subtitles_beats.json")))
    plan = generate_sfx_plan(beats, format_type)
    output = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plan.json")
    with open(output, "w") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    print(f"Plan saved to {output}")


def cmd_place(plan_file):
    """Place SFX on timeline."""
    from sfx_place import place_sfx
    plan_path = plan_file or os.path.join(os.path.dirname(os.path.abspath(__file__)), "plan.json")
    place_sfx(plan_path)


def cmd_enhance(srt_file):
    """Full pipeline: analyze → plan → place."""
    cmd_analyze(srt_file)
    cmd_plan()
    cmd_place()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "status":
        cmd_status()
    elif command == "analyze":
        srt = sys.argv[2] if len(sys.argv) > 2 else None
        cmd_analyze(srt)
    elif command == "plan":
        fmt = sys.argv[2] if len(sys.argv) > 2 else "talking-head"
        cmd_plan(fmt)
    elif command == "place":
        pf = sys.argv[2] if len(sys.argv) > 2 else None
        cmd_place(pf)
    elif command == "enhance":
        srt = sys.argv[2] if len(sys.argv) > 2 else None
        cmd_enhance(srt)
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)
