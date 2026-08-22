#!/usr/bin/env python3
"""Analyze voice characteristics from audio files.

Usage:
    python scripts/voice_analyzer.py --audio clip.wav --output voice_emotions.json
    python scripts/voice_analyzer.py --video clip.mp4 --output voice_emotions.json
"""

import argparse
import json
import os
import struct
import sys
import wave
from typing import Any, Dict, List, Optional, Tuple

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
MCP_DIR = os.path.join(REPO_ROOT, "davinci-resolve-mcp")
for _p in (REPO_ROOT, MCP_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# ── Audio Processing ────────────────────────────────────────────────────────

def extract_audio_from_video(video_path: str, output_wav: str) -> bool:
    """Extract audio from video using ffmpeg (if available)."""
    import subprocess
    try:
        cmd = [
            "ffmpeg", "-i", video_path,
            "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
            output_wav, "-y"
        ]
        result = subprocess.run(cmd, capture_output=True, timeout=60)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def read_wav_file(wav_path: str) -> Tuple[Optional[List[int]], int, int]:
    """Read WAV file and return (samples, sample_rate, channels)."""
    try:
        with wave.open(wav_path, "rb") as wf:
            channels = wf.getnchannels()
            sample_width = wf.getsampwidth()
            sample_rate = wf.getframerate()
            n_frames = wf.getnframes()
            raw_data = wf.readframes(n_frames)
        
        # Convert to integers
        if sample_width == 2:
            samples = list(struct.unpack(f"<{n_frames * channels}h", raw_data))
        elif sample_width == 1:
            samples = [b - 128 for b in raw_data]
        else:
            return None, 0, 0
        
        # Mix to mono if stereo
        if channels > 1:
            mono = []
            for i in range(0, len(samples), channels):
                mono.append(sum(samples[i:i+channels]) // channels)
            samples = mono
        
        return samples, sample_rate, 1
    except Exception as exc:
        print(f"ERROR reading WAV: {exc}", file=sys.stderr)
        return None, 0, 0


def compute_rms_volume(samples: List[int], window_size: int = 1024) -> List[float]:
    """Compute RMS volume over windows."""
    volumes = []
    for i in range(0, len(samples) - window_size, window_size):
        window = samples[i:i + window_size]
        rms = (sum(s * s for s in window) / len(window)) ** 0.5
        db = 20 * log10(rms / 32768) if rms > 0 else -60
        volumes.append(round(db, 2))
    return volumes


def compute_pitch(samples: List[int], sample_rate: int, window_size: int = 2048) -> List[float]:
    """Estimate pitch using autocorrelation."""
    pitches = []
    for i in range(0, len(samples) - window_size, window_size // 2):
        window = samples[i:i + window_size]
        
        # Autocorrelation
        correlation = []
        for lag in range(sample_rate // 500, sample_rate // 50):  # 500Hz to 50Hz
            if lag >= len(window):
                break
            corr = sum(window[j] * window[j + lag] for j in range(len(window) - lag))
            correlation.append((lag, corr))
        
        if not correlation:
            continue
        
        # Find peak
        best_lag, best_corr = max(correlation, key=lambda x: x[1])
        if best_corr > 0:
            pitch = sample_rate / best_lag
            pitches.append(round(pitch, 1))
        else:
            pitches.append(0.0)
    
    return pitches


def compute_speaking_rate(samples: List[int], sample_rate: int) -> float:
    """Estimate speaking rate (syllables per second) from voice activity."""
    # Simple voice activity detection based on energy
    window_size = sample_rate // 10  # 100ms windows
    threshold = 100  # RMS threshold
    
    active_windows = 0
    total_windows = 0
    transitions = 0
    was_active = False
    
    for i in range(0, len(samples) - window_size, window_size):
        window = samples[i:i + window_size]
        rms = (sum(s * s for s in window) / len(window)) ** 0.5
        is_active = rms > threshold
        
        total_windows += 1
        if is_active:
            active_windows += 1
            if not was_active:
                transitions += 1
        was_active = is_active
    
    duration = len(samples) / sample_rate
    if duration > 0:
        # Estimate syllables from voice onset transitions
        return round(transitions / duration, 2)
    return 0.0


def log10(x: float) -> float:
    """Log base 10."""
    import math
    return math.log10(x) if x > 0 else -60


# ── Emotion Detection from Voice ────────────────────────────────────────────

def detect_emotion_from_voice(
    volumes: List[float],
    pitches: List[float],
    speaking_rate: float,
) -> Dict[str, Any]:
    """Detect emotion signals from voice characteristics."""
    emotions = {
        "excitement": 0.0,
        "anger": 0.0,
        "sadness": 0.0,
        "calm": 0.0,
        "fear": 0.0,
        "neutral": 0.0,
    }
    signals = {}

    # Volume analysis
    if volumes:
        avg_volume = sum(volumes) / len(volumes)
        max_volume = max(volumes)
        signals["avg_volume_db"] = round(avg_volume, 2)
        signals["max_volume_db"] = round(max_volume, 2)
        
        if avg_volume > -10:
            emotions["anger"] += 0.3
            emotions["excitement"] += 0.2
        elif avg_volume < -20:
            emotions["sadness"] += 0.3
            emotions["calm"] += 0.2

    # Pitch analysis
    if pitches:
        valid_pitches = [p for p in pitches if p > 0]
        if valid_pitches:
            avg_pitch = sum(valid_pitches) / len(valid_pitches)
            pitch_variance = sum((p - avg_pitch) ** 2 for p in valid_pitches) / len(valid_pitches)
            signals["avg_pitch_hz"] = round(avg_pitch, 1)
            signals["pitch_variance"] = round(pitch_variance, 1)
            
            if avg_pitch > 200:
                emotions["excitement"] += 0.4
                emotions["fear"] += 0.2
            elif avg_pitch < 100:
                emotions["sadness"] += 0.3
                emotions["calm"] += 0.3

    # Speaking rate analysis
    signals["speaking_rate"] = speaking_rate
    
    if speaking_rate > 5:
        emotions["excitement"] += 0.3
        emotions["anger"] += 0.2
    elif speaking_rate < 2:
        emotions["sadness"] += 0.2
        emotions["calm"] += 0.3

    # Find dominant emotion
    max_emotion = max(emotions, key=emotions.get)
    max_score = emotions[max_emotion]
    
    if max_score < 0.3:
        emotions["neutral"] = 0.7
        max_emotion = "neutral"

    return {
        "emotions": emotions,
        "dominant": max_emotion,
        "signals": signals,
        "confidence": max_score,
    }


# ── Main ────────────────────────────────────────────────────────────────────

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Analyze voice characteristics from audio files."
    )
    parser.add_argument(
        "--audio",
        help="path to audio file (WAV)",
    )
    parser.add_argument(
        "--video",
        help="path to video file (will extract audio)",
    )
    parser.add_argument(
        "--output",
        default="voice_emotions.json",
        help="output JSON path (default: voice_emotions.json)",
    )
    parser.add_argument(
        "--window-size",
        type=int,
        default=1024,
        help="analysis window size in samples (default: 1024)",
    )
    args = parser.parse_args(argv)

    if not args.audio and not args.video:
        print("ERROR: Provide --audio or --video", file=sys.stderr)
        return 1

    # Get audio file
    audio_path = args.audio
    temp_file = None
    
    if args.video and not audio_path:
        temp_file = os.path.join(REPO_ROOT, "temp_audio.wav")
        print(f"Extracting audio from {args.video}...")
        if not extract_audio_from_video(args.video, temp_file):
            print("ERROR: Cannot extract audio. Is ffmpeg installed?", file=sys.stderr)
            return 1
        audio_path = temp_file

    if not audio_path or not os.path.isfile(audio_path):
        print(f"ERROR: Audio file not found: {audio_path}", file=sys.stderr)
        return 1

    # Read audio
    print(f"Reading audio: {audio_path}")
    samples, sample_rate, channels = read_wav_file(audio_path)
    
    if samples is None:
        print("ERROR: Cannot read audio file.", file=sys.stderr)
        return 1

    print(f"  Sample rate: {sample_rate}, Duration: {len(samples)/sample_rate:.1f}s")

    # Analyze
    print("Analyzing voice characteristics...")
    volumes = compute_rms_volume(samples, args.window_size)
    pitches = compute_pitch(samples, sample_rate, args.window_size * 2)
    speaking_rate = compute_speaking_rate(samples, sample_rate)

    # Detect emotions
    result = detect_emotion_from_voice(volumes, pitches, speaking_rate)
    
    # Add metadata
    result["audio_file"] = audio_path
    result["sample_rate"] = sample_rate
    result["duration_seconds"] = round(len(samples) / sample_rate, 3)
    result["volumes"] = volumes
    result["pitches"] = pitches

    # Save
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\nSaved voice analysis to {args.output}")

    # Summary
    print(f"\n=== Voice Analysis Summary ===")
    print(f"  Dominant emotion: {result['dominant']} (confidence: {result['confidence']:.2f})")
    print(f"  Signals:")
    for key, value in result["signals"].items():
        print(f"    {key}: {value}")
    print(f"  Emotions:")
    for emotion, score in sorted(result["emotions"].items(), key=lambda x: -x[1]):
        if score > 0:
            print(f"    {emotion}: {score:.2f}")

    # Cleanup
    if temp_file and os.path.exists(temp_file):
        os.remove(temp_file)

    return 0


if __name__ == "__main__":
    sys.exit(main())
