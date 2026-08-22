#!/usr/bin/env python3
"""Analyze facial expressions from video frames using OpenCV + MediaPipe.

Usage:
    python scripts/face_analyzer.py --video clip.mp4 --output face_emotions.json
    python scripts/face_analyzer.py --video clip.mp4 --sample-rate 2 --output face_emotions.json
"""

import argparse
import json
import os
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
MCP_DIR = os.path.join(REPO_ROOT, "davinci-resolve-mcp")
for _p in (REPO_ROOT, MCP_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# ── Emotion Detection ───────────────────────────────────────────────────────

def detect_emotion_from_landmarks(landmarks: Dict[str, Any]) -> Dict[str, Any]:
    """Detect emotion signals from face landmarks.
    
    Returns dict with emotion scores and detected emotions.
    """
    emotions = {
        "surprise": 0.0,
        "happiness": 0.0,
        "anger": 0.0,
        "fear": 0.0,
        "sadness": 0.0,
        "neutral": 0.0,
    }
    signals = {}

    # Mouth analysis
    mouth = landmarks.get("mouth")
    if mouth:
        mouth_width = _dist(mouth["left"], mouth["right"]) or 1.0
        mouth_height = _dist(mouth["top"], mouth["bottom"])
        mouth_open_ratio = mouth_height / mouth_width
        
        signals["mouth_open"] = mouth_open_ratio
        
        if mouth_open_ratio > 0.3:
            emotions["surprise"] += 0.4
            emotions["happiness"] += 0.2
        elif mouth_open_ratio > 0.15:
            emotions["happiness"] += 0.3

    # Brow analysis
    brow = landmarks.get("brow")
    face = landmarks.get("face")
    if brow and face:
        face_height = _dist(face["top"], face["bottom"]) or 1.0
        brow_height = (brow["left"][1] + brow["right"][1]) / 2
        face_top = face["top"][1]
        brow_raise_ratio = (brow_height - face_top) / face_height
        
        signals["brow_raise"] = brow_raise_ratio
        
        if brow_raise_ratio > 0.3:
            emotions["surprise"] += 0.3
            emotions["fear"] += 0.2

    # Eye analysis
    for eye_key in ["left_eye", "right_eye"]:
        eye = landmarks.get(eye_key)
        if eye:
            ear = _eye_aspect_ratio(eye)
            signals[f"{eye_key}_ear"] = ear
            
            if ear > 0.35:
                emotions["surprise"] += 0.2
                emotions["fear"] += 0.1
            elif ear < 0.2:
                emotions["anger"] += 0.2

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


def _dist(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    """Euclidean distance between two points."""
    import math
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _eye_aspect_ratio(eye: Dict[str, Tuple[float, float]]) -> float:
    """Calculate Eye Aspect Ratio (EAR)."""
    horiz = _dist(eye["outer"], eye["inner"])
    if horiz <= 0:
        return 0.0
    return (_dist(eye["top1"], eye["bot1"]) + _dist(eye["top2"], eye["bot2"])) / (2.0 * horiz)


# ── Video Processing ────────────────────────────────────────────────────────

def analyze_video(
    video_path: str,
    sample_rate: float = 2.0,
    max_frames: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """Analyze facial expressions in a video file.
    
    Args:
        video_path: Path to video file
        sample_rate: Frames per second to analyze (default: 2)
        max_frames: Maximum number of frames to analyze
        
    Returns:
        List of frame analysis results
    """
    try:
        import cv2
    except ImportError:
        print("ERROR: OpenCV (cv2) not available. Install with: pip install opencv-python", file=sys.stderr)
        return []

    try:
        import mediapipe as mp
    except ImportError:
        print("ERROR: MediaPipe not available. Install with: pip install mediapipe", file=sys.stderr)
        return []

    if not os.path.isfile(video_path):
        print(f"ERROR: Video file not found: {video_path}", file=sys.stderr)
        return []

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"ERROR: Cannot open video: {video_path}", file=sys.stderr)
        return []

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_interval = int(fps / sample_rate) if sample_rate > 0 else int(fps / 2)
    
    print(f"Video: {video_path}")
    print(f"  FPS: {fps}, Duration: {total_frames/fps:.1f}s")
    print(f"  Analyzing every {frame_interval} frames ({sample_rate} fps)")

    # Initialize MediaPipe Face Mesh
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    results = []
    frame_idx = 0
    analyzed = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_idx % frame_interval == 0:
            timestamp = frame_idx / fps
            
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process with MediaPipe
            mp_results = face_mesh.process(rgb_frame)
            
            if mp_results.multi_face_landmarks:
                face_landmarks = mp_results.multi_face_landmarks[0]
                landmarks = _extract_landmarks(face_landmarks, frame.shape)
                emotion_result = detect_emotion_from_landmarks(landmarks)
                
                results.append({
                    "frame": frame_idx,
                    "timestamp_seconds": round(timestamp, 3),
                    "face_detected": True,
                    **emotion_result,
                })
            else:
                results.append({
                    "frame": frame_idx,
                    "timestamp_seconds": round(timestamp, 3),
                    "face_detected": False,
                    "dominant": "unknown",
                    "confidence": 0.0,
                })
            
            analyzed += 1
            if analyzed % 50 == 0:
                print(f"  Analyzed {analyzed} frames...")
        
        frame_idx += 1
        if max_frames and analyzed >= max_frames:
            break

    cap.release()
    face_mesh.close()
    
    print(f"  Analyzed {len(results)} frames total")
    return results


def _extract_landmarks(face_landmarks, frame_shape: Tuple[int, int]) -> Dict[str, Any]:
    """Extract key landmarks from MediaPipe face mesh."""
    h, w = frame_shape[:2]
    
    # Key landmark indices (MediaPipe face mesh topology)
    LEFT_EYE = {"outer": 33, "inner": 133, "top1": 160, "top2": 158, "bot1": 144, "bot2": 153}
    RIGHT_EYE = {"outer": 362, "inner": 263, "top1": 385, "top2": 387, "bot1": 380, "bot2": 373}
    MOUTH = {"left": 61, "right": 291, "top": 13, "bottom": 14}
    BROW = {"left": 105, "right": 334}
    FACE = {"top": 10, "bottom": 152}

    def get_point(idx: int) -> Tuple[float, float]:
        lm = face_landmarks.landmark[idx]
        return (lm.x * w, lm.y * h)

    return {
        "left_eye": {k: get_point(v) for k, v in LEFT_EYE.items()},
        "right_eye": {k: get_point(v) for k, v in RIGHT_EYE.items()},
        "mouth": {k: get_point(v) for k, v in MOUTH.items()},
        "brow": {k: get_point(v) for k, v in BROW.items()},
        "face": {k: get_point(v) for k, v in FACE.items()},
    }


# ── Main ────────────────────────────────────────────────────────────────────

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Analyze facial expressions from video frames."
    )
    parser.add_argument(
        "--video",
        required=True,
        help="path to video file",
    )
    parser.add_argument(
        "--output",
        default="face_emotions.json",
        help="output JSON path (default: face_emotions.json)",
    )
    parser.add_argument(
        "--sample-rate",
        type=float,
        default=2.0,
        help="frames per second to analyze (default: 2)",
    )
    parser.add_argument(
        "--max-frames",
        type=int,
        help="maximum number of frames to analyze",
    )
    args = parser.parse_args(argv)

    results = analyze_video(args.video, args.sample_rate, args.max_frames)
    
    if not results:
        print("ERROR: No face analysis results.", file=sys.stderr)
        return 1

    # Save results
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\nSaved {len(results)} frame analyses to {args.output}")

    # Summary
    face_detected = [r for r in results if r.get("face_detected")]
    emotions_count = {}
    for r in face_detected:
        dom = r.get("dominant", "unknown")
        emotions_count[dom] = emotions_count.get(dom, 0) + 1

    print(f"\n=== Summary ===")
    print(f"  Total frames: {len(results)}")
    print(f"  Face detected: {len(face_detected)} ({len(face_detected)/len(results)*100:.1f}%)")
    print(f"  Emotions distribution:")
    for emotion, count in sorted(emotions_count.items(), key=lambda x: -x[1]):
        print(f"    {emotion}: {count} ({count/len(face_detected)*100:.1f}%)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
