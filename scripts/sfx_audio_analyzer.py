#!/usr/bin/env python3
"""SFX Audio Analyzer — extract audio features from SFX files.

Analyzes WAV files for loudness, RMS, peak, and energy profile.
Creates enriched metadata for better SFX selection.
"""

from __future__ import annotations

import logging
import wave
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass
class AudioFeatures:
    """Audio features extracted from an SFX file."""
    duration_seconds: float = 0.0
    sample_rate: int = 0
    channels: int = 0
    rms_db: float = 0.0       # Root mean square (perceived loudness)
    peak_db: float = 0.0      # Peak amplitude
    energy_profile: str = ""  # "transient", "sustained", "渐增", "渐减", "mixed"
    energy_score: float = 0.0  # 0-1, higher = more energetic


def analyze_wav(path: Path) -> AudioFeatures:
    """Extract audio features from a WAV file."""
    features = AudioFeatures()
    try:
        with wave.open(str(path), "rb") as w:
            features.sample_rate = w.getframerate()
            features.channels = w.getnchannels()
            n_frames = w.getnframes()
            features.duration_seconds = n_frames / float(features.sample_rate) if features.sample_rate > 0 else 0.0

            # Read audio data
            frames = w.readframes(n_frames)
            if not frames:
                return features

            # Convert to integers
            if features.channels == 1:
                raw = list(struct.unpack(f"<{n_frames}h", frames))
            else:
                # Stereo - average channels
                raw = []
                for i in range(0, len(frames), 2 * 2):  # 2 bytes per sample
                    left = struct.unpack("<h", frames[i:i+2])[0]
                    right = struct.unpack("<h", frames[i+2:i+4])[0]
                    raw.append((left + right) // 2)

            if not raw:
                return features

            # Calculate RMS
            rms = (sum(x * x for x in raw) / len(raw)) ** 0.5
            max_val = 32768.0  # 16-bit
            features.rms_db = 20 * math.log10(rms / max_val) if rms > 0 else -inf

            # Calculate peak
            peak = max(abs(x) for x in raw)
            features.peak_db = 20 * math.log10(peak / max_val) if peak > 0 else -inf

            # Determine energy profile
            features.energy_profile = _classify_energy_profile(raw)
            features.energy_score = _calculate_energy_score(raw, features.duration_seconds)

    except Exception as e:
        logger.debug("Failed to analyze WAV %s: %s", path.name, e)

    return features


def _classify_energy_profile(samples: List[int]) -> str:
    """Classify the energy profile of audio samples."""
    if not samples:
        return "unknown"

    n = len(samples)
    chunk_size = max(1, n // 10)

    # Divide into 10 chunks and calculate energy per chunk
    energies = []
    for i in range(0, n, chunk_size):
        chunk = samples[i:i + chunk_size]
        if chunk:
            energy = sum(x * x for x in chunk) / len(chunk)
            energies.append(energy)

    if len(energies) < 3:
        return "unknown"

    # Analyze energy trend
    first_third = sum(energies[:len(energies)//3]) / 3
    last_third = sum(energies[-len(energies)//3:]) / 3

    if last_third > first_third * 1.5:
        return "渐增"
    elif first_third > last_third * 1.5:
        return "渐减"
    elif max(energies) / (min(energies) + 0.001) > 3.0:
        return "transient"
    else:
        return "mixed"


def _calculate_energy_score(samples: List[int], duration: float) -> float:
    """Calculate energy score (0-1) based on RMS and duration."""
    if not samples or duration <= 0:
        return 0.0

    rms = (sum(x * x for x in samples) / len(samples)) ** 0.5
    max_val = 32768.0
    normalized_rms = rms / max_val  # 0-1

    # Shorter sounds with higher RMS = more energetic
    duration_factor = min(1.0, 1.0 / (duration + 0.1))
    energy_score = normalized_rms * 0.6 + duration_factor * 0.4
    return min(1.0, max(0.0, energy_score))


def analyze_sfx_library(sfx_dir: Path) -> List[AudioFeatures]:
    """Analyze all WAV files in a directory."""
    features_list = []
    for path in sfx_dir.glob("*.wav"):
        features = analyze_wav(path)
        features_list.append(features)
    return features_list


if __name__ == "__main__":
    import sys
    from pathlib import Path
    import struct
    import math

    sfx_dir = Path(r"C:\Users\warit\Desktop\davinci-katy-mcp\SFX")
    if not sfx_dir.exists():
        print(f"Directory not found: {sfx_dir}")
        sys.exit(1)

    print("Analyzing SFX library...")
    features = analyze_sfx_library(sfx_dir)
    print(f"Analyzed {len(features)} files")

    # Show summary
    print("\nTop 10 most energetic SFX:")
    sorted_features = sorted(features, key=lambda f: f.energy_score, reverse=True)
    for i, f in enumerate(sorted_features[:10]):
        print(f"  {i+1}. energy={f.energy_score:.2f} rms={f.rms_db:.1f}dB dur={f.duration_seconds:.2f}s")
