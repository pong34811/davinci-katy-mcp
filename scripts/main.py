#!/usr/bin/env python3
"""Main entry point for DaVinci Resolve SFX System.

Usage:
    python scripts/main.py enhance --srt subtitle_from_track1.srt --format talking-head
    python scripts/main.py analyze --srt subtitle_from_track1.srt
    python scripts/main.py plan --beats beats.json --format talking-head
    python scripts/main.py place --plan plan.json --verify
    python scripts/main.py status
"""

import argparse
import sys
import os

# Add scripts directory to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from config import validate_config, SFX_DIR, FORMAT_CONFIGS


def _to_str(path) -> str:
    """Convert Path/str to string for downstream string operations."""
    return str(path) if hasattr(path, '__fspath__') or not isinstance(path, str) else path


def cmd_enhance(args):
    """Run the full enhancement pipeline."""
    try:
        from clip_enhancer import run_full_pipeline
        
        return run_full_pipeline(
            clip_format=args.format,
            srt_path=args.srt,
            plan_json=args.output,
            dry_run=args.dry_run,
            verify=args.verify,
            sfx_dir=str(SFX_DIR),
            skip_place=args.skip_place,
        )
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


def cmd_analyze(args):
    """Analyze subtitles and generate beats."""
    try:
        from analyze_subtitles import read_subtitles_from_srt, analyze_subtitles, format_beats_table
        
        if args.srt:
            subs = read_subtitles_from_srt(args.srt)
        else:
            print("ERROR: Provide --srt file", file=sys.stderr)
            return 1
        
        beats = analyze_subtitles(subs)
        print(format_beats_table(beats))
        
        # Save beats
        import json
        output = args.output or "beats.json"
        with open(output, "w", encoding="utf-8") as f:
            json.dump(beats, f, ensure_ascii=False, indent=2)
        print(f"\nSaved {len(beats)} beats to {output}")
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


def cmd_plan(args):
    """Generate SFX plan from beats."""
    try:
        from generate_sfx_plan import generate_plan
        import json
        
        with open(args.beats, "r", encoding="utf-8") as f:
            beats = json.load(f)
        
        plan, warnings = generate_plan(beats, args.format)
        
        for w in warnings:
            print(f"WARNING: {w}")
        
        output = args.output or "plan.json"
        with open(output, "w", encoding="utf-8") as f:
            json.dump(plan, f, ensure_ascii=False, indent=2)
        
        print(f"\nPlan generated:")
        print(f"  SFX count: {plan['sfx_count']}")
        print(f"  Duration: {plan['duration_seconds']:.1f}s")
        print(f"  Saved to: {output}")
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


def cmd_place(args):
    """Place SFX on timeline."""
    try:
        import subprocess
        
        cmd = [
            sys.executable,
            os.path.join(SCRIPT_DIR, "sfx_place.py"),
            "--plan", args.plan,
            "--sfx-dir", str(SFX_DIR),
        ]
        if args.dry_run:
            cmd.append("--dry-run")
        if args.verify:
            cmd.append("--verify")
        
        result = subprocess.run(cmd)
        return result.returncode
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


def cmd_status(args):
    """Show system status."""
    print("=== DaVinci Resolve SFX System Status ===\n")
    
    status = validate_config()
    print("Configuration:")
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    print("\nAvailable formats:")
    for name, config in FORMAT_CONFIGS.items():
        print(f"  {name}: {config['description']}")
    
    print("\nSFX families:")
    from config import SFX_FAMILIES, get_sfx_file
    for family in SFX_FAMILIES:
        sfx_file = get_sfx_file(family)
        status = "✓" if sfx_file else "✗"
        print(f"  {family}: {status}")
    
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="DaVinci Resolve SFX System"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # enhance command
    enhance_parser = subparsers.add_parser("enhance", help="Run full enhancement pipeline")
    enhance_parser.add_argument("--srt", help="path to SRT subtitle file")
    enhance_parser.add_argument("--format", choices=list(FORMAT_CONFIGS.keys()), default="talking-head")
    enhance_parser.add_argument("--output", default="plan.json")
    enhance_parser.add_argument("--dry-run", action="store_true")
    enhance_parser.add_argument("--verify", action="store_true")
    enhance_parser.add_argument("--skip-place", action="store_true")
    
    # analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze subtitles")
    analyze_parser.add_argument("--srt", help="path to SRT subtitle file")
    analyze_parser.add_argument("--output", default="beats.json")
    
    # plan command
    plan_parser = subparsers.add_parser("plan", help="Generate SFX plan")
    plan_parser.add_argument("--beats", required=True, help="path to beats JSON")
    plan_parser.add_argument("--format", choices=list(FORMAT_CONFIGS.keys()), default="talking-head")
    plan_parser.add_argument("--output", default="plan.json")
    
    # place command
    place_parser = subparsers.add_parser("place", help="Place SFX on timeline")
    place_parser.add_argument("--plan", required=True, help="path to plan JSON")
    place_parser.add_argument("--dry-run", action="store_true")
    place_parser.add_argument("--verify", action="store_true")
    
    # status command
    subparsers.add_parser("status", help="Show system status")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    commands = {
        "enhance": cmd_enhance,
        "analyze": cmd_analyze,
        "plan": cmd_plan,
        "place": cmd_place,
        "status": cmd_status,
    }
    
    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
