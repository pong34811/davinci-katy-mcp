#!/usr/bin/env python3
"""Combine face and voice emotion analysis into unified emotion timeline.

Usage:
    python scripts/emotion_analyzer.py --face face_emotions.json --voice voice_emotions.json --output emotions.json
    python scripts/emotion_analyzer.py --face face_emotions.json --output emotions.json  (face only)
    python scripts/emotion_analyzer.py --voice voice_emotions.json --output emotions.json  (voice only)
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


def combine_emotions(
    face_data: Optional[List[Dict[str, Any]]],
    voice_data: Optional[Dict[str, Any]],
    sample_rate: float = 0.5,
) -> Dict[str, Any]:
    """Combine face and voice emotion data into unified timeline.
    
    Args:
        face_data: List of face analysis results (from face_analyzer.py)
        voice_data: Voice analysis result (from voice_analyzer.py)
        sample_rate: Timeline sample rate in seconds
        
    Returns:
        Combined emotion timeline
    """
    # Get duration from available data
    duration = 0.0
    if face_data and face_data:
        duration = max(r.get("timestamp_seconds", 0) for r in face_data)
    if voice_data:
        duration = max(duration, voice_data.get("duration_seconds", 0))
    
    if duration <= 0:
        return {"timeline": [], "summary": {}, "duration": 0}

    # Create timeline samples
    n_samples = int(duration / sample_rate) + 1
    timeline = []

    for i in range(n_samples):
        t = i * sample_rate
        
        # Get face emotion at this time
        face_emotion = None
        if face_data:
            # Find closest face sample
            closest = min(face_data, key=lambda r: abs(r.get("timestamp_seconds", 0) - t))
            if closest.get("face_detected"):
                face_emotion = {
                    "dominant": closest.get("dominant", "neutral"),
                    "confidence": closest.get("confidence", 0),
                    "emotions": closest.get("emotions", {}),
                }
        
        # Get voice emotion (voice data applies to entire clip)
        voice_emotion = None
        if voice_data:
            voice_emotion = {
                "dominant": voice_data.get("dominant", "neutral"),
                "confidence": voice_data.get("confidence", 0),
                "emotions": voice_data.get("emotions", {}),
            }
        
        # Combine emotions
        combined = combine_single_moment(face_emotion, voice_emotion)
        
        timeline.append({
            "timestamp_seconds": round(t, 3),
            "face": face_emotion,
            "voice": voice_emotion,
            "combined": combined,
        })

    # Generate summary
    summary = generate_summary(timeline)
    
    return {
        "timeline": timeline,
        "summary": summary,
        "duration": round(duration, 3),
        "sample_rate": sample_rate,
        "has_face_data": face_data is not None,
        "has_voice_data": voice_data is not None,
    }


def combine_single_moment(
    face: Optional[Dict[str, Any]],
    voice: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """Combine face and voice emotions for a single moment."""
    # All emotion categories
    all_emotions = ["surprise", "happiness", "anger", "fear", "sadness", "neutral", "excitement", "calm"]
    
    combined_scores = {e: 0.0 for e in all_emotions}
    weights = {"face": 0.6, "voice": 0.4}  # Face has more weight
    
    # Add face scores
    if face and face.get("emotions"):
        for emotion, score in face["emotions"].items():
            if emotion in combined_scores:
                combined_scores[emotion] += score * weights["face"]
    
    # Add voice scores
    if voice and voice.get("emotions"):
        for emotion, score in voice["emotions"].items():
            if emotion in combined_scores:
                combined_scores[emotion] += score * weights["voice"]
    
    # Normalize
    total = sum(combined_scores.values())
    if total > 0:
        combined_scores = {k: round(v / total, 3) for k, v in combined_scores.items()}
    
    # Find dominant
    dominant = max(combined_scores, key=combined_scores.get)
    confidence = combined_scores[dominant]
    
    if confidence < 0.3:
        dominant = "neutral"
        combined_scores["neutral"] = max(combined_scores["neutral"], 0.5)
    
    return {
        "dominant": dominant,
        "confidence": round(confidence, 3),
        "emotions": combined_scores,
    }


def generate_summary(timeline: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate summary statistics from emotion timeline."""
    if not timeline:
        return {}
    
    # Count emotions
    emotion_counts = {}
    for entry in timeline:
        dom = entry["combined"]["dominant"]
        emotion_counts[dom] = emotion_counts.get(dom, 0) + 1
    
    # Find emotion segments (consecutive same emotion)
    segments = []
    current_emotion = None
    segment_start = 0
    
    for i, entry in enumerate(timeline):
        dom = entry["combined"]["dominant"]
        if dom != current_emotion:
            if current_emotion is not None:
                segments.append({
                    "emotion": current_emotion,
                    "start": round(segment_start, 3),
                    "end": round(entry["timestamp_seconds"], 3),
                    "duration": round(entry["timestamp_seconds"] - segment_start, 3),
                })
            current_emotion = dom
            segment_start = entry["timestamp_seconds"]
    
    # Add last segment
    if current_emotion is not None:
        segments.append({
            "emotion": current_emotion,
            "start": round(segment_start, 3),
            "end": round(timeline[-1]["timestamp_seconds"], 3),
            "duration": round(timeline[-1]["timestamp_seconds"] - segment_start, 3),
        })
    
    # Overall dominant
    overall_dominant = max(emotion_counts, key=emotion_counts.get) if emotion_counts else "neutral"
    
    return {
        "emotion_counts": emotion_counts,
        "segments": segments,
        "overall_dominant": overall_dominant,
        "total_samples": len(timeline),
    }


def format_emotion_timeline(result: Dict[str, Any]) -> str:
    """Format emotion timeline as readable table."""
    lines = [
        f"{'Time':>8} | {'Face':<12} | {'Voice':<12} | {'Combined':<12} | {'Conf':>5}",
        "-" * 70,
    ]
    
    timeline = result.get("timeline", [])
    for entry in timeline:
        t = entry["timestamp_seconds"]
        face_dom = entry.get("face", {}).get("dominant", "-") if entry.get("face") else "-"
        voice_dom = entry.get("voice", {}).get("dominant", "-") if entry.get("voice") else "-"
        combined = entry["combined"]
        
        lines.append(
            f"{t:>7.1f}s | {face_dom:<12} | {voice_dom:<12} | {combined['dominant']:<12} | {combined['confidence']:>5.2f}"
        )
    
    return "\n".join(lines)


# ── Main ────────────────────────────────────────────────────────────────────

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Combine face and voice emotion analysis."
    )
    parser.add_argument(
        "--face",
        help="path to face emotions JSON (from face_analyzer.py)",
    )
    parser.add_argument(
        "--voice",
        help="path to voice emotions JSON (from voice_analyzer.py)",
    )
    parser.add_argument(
        "--output",
        default="emotions.json",
        help="output JSON path (default: emotions.json)",
    )
    parser.add_argument(
        "--sample-rate",
        type=float,
        default=0.5,
        help="timeline sample rate in seconds (default: 0.5)",
    )
    args = parser.parse_args(argv)

    if not args.face and not args.voice:
        print("ERROR: Provide at least --face or --voice", file=sys.stderr)
        return 1

    # Load data
    face_data = None
    voice_data = None

    if args.face:
        with open(args.face, "r", encoding="utf-8") as f:
            face_data = json.load(f)
        print(f"Loaded face data: {len(face_data)} frames")

    if args.voice:
        with open(args.voice, "r", encoding="utf-8") as f:
            voice_data = json.load(f)
        print(f"Loaded voice data: {voice_data.get('duration_seconds', 0):.1f}s")

    # Combine
    result = combine_emotions(face_data, voice_data, args.sample_rate)
    
    # Save
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\nSaved combined emotion timeline to {args.output}")

    # Display
    print(f"\n=== Emotion Timeline ===\n")
    print(format_emotion_timeline(result))

    # Summary
    summary = result.get("summary", {})
    print(f"\n=== Summary ===")
    print(f"  Duration: {result['duration']:.1f}s")
    print(f"  Samples: {result['timeline'].__len__()}")
    print(f"  Overall dominant: {summary.get('overall_dominant', 'unknown')}")
    
    if "emotion_counts" in summary:
        print(f"  Emotion distribution:")
        for emotion, count in sorted(summary["emotion_counts"].items(), key=lambda x: -x[1]):
            pct = count / len(result["timeline"]) * 100
            print(f"    {emotion}: {count} ({pct:.1f}%)")

    if "segments" in summary:
        print(f"\n  Emotion segments:")
        for seg in summary["segments"][:10]:  # Show first 10
            print(f"    {seg['start']:.1f}s - {seg['end']:.1f}s: {seg['emotion']} ({seg['duration']:.1f}s)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
