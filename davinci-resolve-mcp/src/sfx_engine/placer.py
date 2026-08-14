"""Timeline SFX Placement Engine for DaVinci Resolve.

Handles the actual placement of SFX files onto the DaVinci Resolve timeline,
including track management, media import, audio trimming, and verification.

This module bridges the SFX recommendation engine with the DaVinci Resolve
scripting API. It handles:
- Track discovery and creation
- Media Pool import with deduplication
- Pre-trimming WAV files to sting duration (Resolve API workaround)
- Precise frame-accurate placement
- Post-placement verification and readback
"""

from __future__ import annotations

import logging
import os
import struct
import wave
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# ─── Constants ───────────────────────────────────────────────────────────────

DEFAULT_STING_DURATION_SECONDS = 0.5
DEFAULT_FADE_OUT_SECONDS = 0.03
MEDIA_TYPE_AUDIO = 2
DEFAULT_SFX_TRACK_NAME = "SFX 1"
SFX_BIN_PATH = "Master/SFX"


# ─── Data Classes ────────────────────────────────────────────────────────────

@dataclass
class PlacementResult:
    """Result of placing a single SFX on the timeline."""
    success: bool
    sfx_filename: str
    target_seconds: float
    target_frame: int
    actual_frame: Optional[int] = None
    track_index: int = 0
    error: Optional[str] = None
    clip_name: Optional[str] = None


@dataclass
class PlacementReport:
    """Complete report from an SFX placement session."""
    success: bool
    total_planned: int
    total_placed: int
    total_failed: int
    track_index: int
    fps: float
    results: List[PlacementResult] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


# ─── WAV Trimming (Resolve API Workaround) ───────────────────────────────────

def trim_wav(
    src_path: str,
    dst_path: str,
    duration_seconds: float,
    fade_out_seconds: float = DEFAULT_FADE_OUT_SECONDS,
) -> Dict[str, Any]:
    """Pre-trim a WAV file to a sting duration with fade-out.

    DaVinci Resolve's scripting API ignores the `endFrame` parameter when
    placing audio clips via `AppendToTimeline`. The workaround is to
    pre-trim WAV files to the desired sting length externally and import
    the trimmed version.

    Only supports 16-bit PCM WAV files (the standard for SFX).

    Args:
        src_path: Source WAV file path.
        dst_path: Destination path for trimmed WAV.
        duration_seconds: Target duration in seconds.
        fade_out_seconds: Fade-out duration at the end to prevent clicks.

    Returns:
        Dict with success status, output path, and duration info.
    """
    try:
        with wave.open(src_path, "rb") as src:
            params = src.getparams()
            sample_rate = params.framerate
            channels = params.nchannels
            sampwidth = params.sampwidth
            total_frames = params.nframes

            if sampwidth != 2:
                return {
                    "success": False,
                    "error": f"Only 16-bit PCM WAV supported, got {sampwidth * 8}-bit",
                    "src": src_path,
                }

            # Calculate frames to keep
            target_frames = min(
                int(duration_seconds * sample_rate),
                total_frames,
            )
            fade_frames = min(
                int(fade_out_seconds * sample_rate),
                target_frames,
            )

            # Read raw audio data
            raw_data = src.readframes(target_frames)

        # Apply fade-out to prevent clicks
        if fade_frames > 0 and target_frames > 0:
            bytes_per_sample = sampwidth
            samples_per_frame = channels
            total_samples = target_frames * samples_per_frame
            fade_start_sample = (target_frames - fade_frames) * samples_per_frame

            # Unpack all samples
            fmt = f"<{total_samples}h"
            samples = list(struct.unpack(fmt, raw_data))

            # Apply linear fade-out
            for i in range(fade_start_sample, total_samples):
                frame_in_fade = (i - fade_start_sample) // samples_per_frame
                gain = 1.0 - (frame_in_fade / fade_frames)
                gain = max(0.0, min(1.0, gain))
                samples[i] = int(samples[i] * gain)

            raw_data = struct.pack(fmt, *samples)

        # Write trimmed file
        os.makedirs(os.path.dirname(dst_path) or ".", exist_ok=True)
        with wave.open(dst_path, "wb") as dst:
            dst.setparams(params)
            dst.setnframes(target_frames)
            dst.writeframes(raw_data)

        actual_duration = target_frames / sample_rate if sample_rate > 0 else 0.0

        logger.info(
            "Trimmed %s -> %s (%.3fs, %d frames, fade %.3fs)",
            src_path, dst_path, actual_duration, target_frames, fade_out_seconds,
        )

        return {
            "success": True,
            "output_path": dst_path,
            "duration_seconds": round(actual_duration, 4),
            "total_frames": target_frames,
            "sample_rate": sample_rate,
            "fade_frames": fade_frames,
        }

    except Exception as exc:
        logger.error("Failed to trim WAV %s: %s", src_path, exc)
        return {
            "success": False,
            "error": str(exc),
            "src": src_path,
        }


# ─── Timeline Placement Engine ───────────────────────────────────────────────

class SFXPlacer:
    """Places SFX files onto the DaVinci Resolve timeline.

    This class manages the complete placement workflow:
    1. Discover or create the SFX audio track
    2. Ensure the SFX bin exists in Media Pool
    3. Import SFX files (with deduplication)
    4. Pre-trim WAV files to sting duration if needed
    5. Place clips at precise frame positions
    6. Verify placement via readback

    Usage:
        placer = SFXPlacer(resolve, project, timeline, media_pool)
        report = placer.execute_plan(sfx_plan)
    """

    def __init__(
        self,
        resolve: Any,
        project: Any,
        timeline: Any,
        media_pool: Any,
        *,
        sting_cache_dir: Optional[str] = None,
    ):
        """Initialize the SFX placer.

        Args:
            resolve: DaVinci Resolve application object.
            project: Current project object.
            timeline: Current timeline object.
            media_pool: Media pool object.
            sting_cache_dir: Directory for caching pre-trimmed sting files.
                If None, uses a temp directory alongside the SFX source.
        """
        self.resolve = resolve
        self.project = project
        self.timeline = timeline
        self.media_pool = media_pool
        self.sting_cache_dir = sting_cache_dir

        # Cached state
        self._fps: Optional[float] = None
        self._start_frame: Optional[int] = None
        self._sfx_track_index: Optional[int] = None
        self._sfx_bin: Any = None
        self._imported_clips: Dict[str, Any] = {}  # filename -> MediaPoolItem

    # ─── Properties ──────────────────────────────────────────────────

    @property
    def fps(self) -> float:
        """Timeline frame rate."""
        if self._fps is None:
            rate_str = self.timeline.GetSetting("timelineFrameRate")
            self._fps = float(rate_str) if rate_str else 60.0
            logger.info("Timeline FPS: %s", self._fps)
        return self._fps

    @property
    def start_frame(self) -> int:
        """Timeline start frame offset."""
        if self._start_frame is None:
            sf = self.timeline.GetStartFrame()
            self._start_frame = int(sf) if sf is not None else 0
            logger.info("Timeline start frame: %d", self._start_frame)
        return self._start_frame

    # ─── Track Management ────────────────────────────────────────────

    def find_or_create_sfx_track(
        self, track_name: str = DEFAULT_SFX_TRACK_NAME
    ) -> int:
        """Find existing SFX track or create a new one.

        Args:
            track_name: Name to search for or assign to the new track.

        Returns:
            1-based track index for the SFX track.
        """
        # Search for existing track with matching name
        track_count = self.timeline.GetTrackCount("audio")
        if track_count:
            for i in range(1, int(track_count) + 1):
                name = self.timeline.GetTrackName("audio", i)
                if name and "SFX" in name.upper():
                    self._sfx_track_index = i
                    logger.info(
                        "Found existing SFX track: '%s' at index %d", name, i
                    )
                    return i

        # Create new audio track
        result = self.timeline.AddTrack("audio")
        if result:
            new_count = self.timeline.GetTrackCount("audio")
            self._sfx_track_index = int(new_count)
            self.timeline.SetTrackName(
                "audio", self._sfx_track_index, track_name
            )
            logger.info(
                "Created SFX track '%s' at index %d",
                track_name, self._sfx_track_index,
            )
        else:
            # Fallback: use last audio track
            self._sfx_track_index = int(track_count) if track_count else 2
            logger.warning(
                "AddTrack failed, using track index %d", self._sfx_track_index
            )

        return self._sfx_track_index

    def get_sfx_track_index(self) -> int:
        """Get the SFX track index, finding or creating it if needed."""
        if self._sfx_track_index is None:
            self.find_or_create_sfx_track()
        return self._sfx_track_index  # type: ignore[return-value]

    # ─── Media Pool Management ───────────────────────────────────────

    def ensure_sfx_bin(self) -> Any:
        """Ensure the Master/SFX bin exists in Media Pool.

        Creates the folder hierarchy if it doesn't exist.

        Returns:
            The SFX bin (folder) object.
        """
        if self._sfx_bin is not None:
            return self._sfx_bin

        root = self.media_pool.GetRootFolder()
        if root is None:
            logger.error("Cannot get Media Pool root folder")
            return None

        # Find or create 'Master' folder
        master = None
        for sub in root.GetSubFolderList() or []:
            if sub.GetName() == "Master":
                master = sub
                break
        if master is None:
            master = self.media_pool.AddSubFolder(root, "Master")
            logger.info("Created 'Master' bin")

        if master is None:
            logger.error("Failed to create 'Master' bin")
            return None

        # Find or create 'SFX' folder inside Master
        sfx_bin = None
        for sub in master.GetSubFolderList() or []:
            if sub.GetName() == "SFX":
                sfx_bin = sub
                break
        if sfx_bin is None:
            sfx_bin = self.media_pool.AddSubFolder(master, "SFX")
            logger.info("Created 'Master/SFX' bin")

        self._sfx_bin = sfx_bin
        return sfx_bin

    def import_sfx_files(
        self, file_paths: List[str]
    ) -> Dict[str, Any]:
        """Import SFX files into Media Pool with deduplication.

        Args:
            file_paths: List of absolute file paths to import.

        Returns:
            Dict mapping filename -> MediaPoolItem for all imported clips.
        """
        sfx_bin = self.ensure_sfx_bin()
        if sfx_bin is None:
            return {}

        # Get existing clips in the SFX bin
        existing_names = set()
        existing_clips = sfx_bin.GetClipList() or []
        for clip in existing_clips:
            name = clip.GetName() if hasattr(clip, "GetName") else str(clip)
            existing_names.add(name)
            # Also index by filename without extension
            base = os.path.splitext(name)[0] if name else ""
            self._imported_clips[name] = clip
            self._imported_clips[base] = clip

        # Filter out already imported files
        to_import = []
        for path in file_paths:
            filename = os.path.basename(path)
            if filename not in existing_names:
                to_import.append(path)
            else:
                logger.debug("Skipping already imported: %s", filename)

        # Import new files
        if to_import:
            self.media_pool.SetCurrentFolder(sfx_bin)
            imported = self.media_pool.ImportMedia(to_import)
            if imported:
                for clip in imported:
                    name = clip.GetName() if hasattr(clip, "GetName") else ""
                    self._imported_clips[name] = clip
                    base = os.path.splitext(name)[0] if name else ""
                    self._imported_clips[base] = clip
                logger.info(
                    "Imported %d new SFX files into Media Pool", len(imported)
                )
            else:
                logger.warning("ImportMedia returned empty/None for %s", to_import)

        return self._imported_clips

    def get_clip_by_name(self, filename: str) -> Optional[Any]:
        """Look up a MediaPoolItem by filename.

        Tries exact match first, then without extension.
        """
        if filename in self._imported_clips:
            return self._imported_clips[filename]

        base = os.path.splitext(filename)[0]
        if base in self._imported_clips:
            return self._imported_clips[base]

        # Re-scan the SFX bin
        sfx_bin = self.ensure_sfx_bin()
        if sfx_bin:
            for clip in sfx_bin.GetClipList() or []:
                name = clip.GetName() if hasattr(clip, "GetName") else ""
                if name == filename or os.path.splitext(name)[0] == base:
                    self._imported_clips[name] = clip
                    self._imported_clips[base] = clip
                    return clip

        return None

    # ─── Frame Calculation ───────────────────────────────────────────

    def seconds_to_frame(self, seconds: float) -> int:
        """Convert seconds to timeline frame number.

        Uses the timeline's FPS and start frame offset.
        """
        return int(self.start_frame + round(seconds * self.fps))

    def frame_to_seconds(self, frame: int) -> float:
        """Convert timeline frame number to seconds."""
        return (frame - self.start_frame) / self.fps if self.fps > 0 else 0.0

    # ─── Sting Preparation ───────────────────────────────────────────

    def prepare_sting(
        self,
        sfx_path: str,
        duration_seconds: float = DEFAULT_STING_DURATION_SECONDS,
    ) -> Optional[str]:
        """Pre-trim an SFX file to a sting duration.

        If the file is already short enough, returns the original path.
        Otherwise creates a trimmed version with '-sting' suffix.

        Args:
            sfx_path: Path to the source SFX file.
            duration_seconds: Target sting duration.

        Returns:
            Path to the sting file (original or trimmed), or None on failure.
        """
        # Only trim WAV files
        if not sfx_path.lower().endswith(".wav"):
            return sfx_path

        # Check current duration
        try:
            with wave.open(sfx_path, "rb") as w:
                current_duration = w.getnframes() / w.getframerate()
        except Exception as exc:
            logger.warning("Cannot read WAV %s: %s", sfx_path, exc)
            return sfx_path

        # If already short enough, use as-is
        if current_duration <= duration_seconds * 1.2:  # 20% tolerance
            return sfx_path

        # Generate sting path
        base = os.path.splitext(sfx_path)
        if self.sting_cache_dir:
            sting_filename = (
                os.path.splitext(os.path.basename(sfx_path))[0]
                + "-sting.wav"
            )
            sting_path = os.path.join(self.sting_cache_dir, sting_filename)
        else:
            sting_path = base[0] + "-sting.wav"

        # Check if sting already exists
        if os.path.exists(sting_path):
            logger.debug("Using cached sting: %s", sting_path)
            return sting_path

        # Trim
        result = trim_wav(sfx_path, sting_path, duration_seconds)
        if result.get("success"):
            return sting_path

        logger.error("Failed to create sting: %s", result.get("error"))
        return sfx_path  # Fall back to original

    # ─── Placement ───────────────────────────────────────────────────

    def place_single(
        self,
        sfx_path: str,
        timestamp_seconds: float,
        *,
        duration_seconds: Optional[float] = None,
        track_index: Optional[int] = None,
        auto_sting: bool = True,
    ) -> PlacementResult:
        """Place a single SFX clip on the timeline.

        Args:
            sfx_path: Path to the SFX file.
            timestamp_seconds: Where to place the SFX (in seconds).
            duration_seconds: Desired clip duration. If shorter than the file,
                the file will be pre-trimmed.
            track_index: Audio track index. If None, uses the SFX track.
            auto_sting: If True, auto-trim long files to sting duration.

        Returns:
            PlacementResult with success/failure details.
        """
        filename = os.path.basename(sfx_path)
        target_frame = self.seconds_to_frame(timestamp_seconds)
        tidx = track_index or self.get_sfx_track_index()

        # Prepare sting if needed
        actual_path = sfx_path
        if auto_sting and duration_seconds:
            sting_path = self.prepare_sting(sfx_path, duration_seconds)
            if sting_path:
                actual_path = sting_path

        # Import the file
        self.import_sfx_files([actual_path])
        actual_filename = os.path.basename(actual_path)
        clip = self.get_clip_by_name(actual_filename)

        if clip is None:
            return PlacementResult(
                success=False,
                sfx_filename=filename,
                target_seconds=timestamp_seconds,
                target_frame=target_frame,
                track_index=tidx,
                error=f"Failed to find imported clip: {actual_filename}",
            )

        # Build clip info for AppendToTimeline
        clip_info = {
            "mediaPoolItem": clip,
            "startFrame": 0,
            "endFrame": 0,  # Use full length (pre-trimmed)
            "recordFrame": target_frame,
            "trackIndex": tidx,
            "mediaType": MEDIA_TYPE_AUDIO,
        }

        # Execute placement
        try:
            result = self.media_pool.AppendToTimeline([clip_info])
            if not result:
                return PlacementResult(
                    success=False,
                    sfx_filename=filename,
                    target_seconds=timestamp_seconds,
                    target_frame=target_frame,
                    track_index=tidx,
                    error="AppendToTimeline returned empty/None",
                )
        except Exception as exc:
            return PlacementResult(
                success=False,
                sfx_filename=filename,
                target_seconds=timestamp_seconds,
                target_frame=target_frame,
                track_index=tidx,
                error=str(exc),
            )

        logger.info(
            "Placed %s at %.2fs (frame %d) on track %d",
            filename, timestamp_seconds, target_frame, tidx,
        )

        return PlacementResult(
            success=True,
            sfx_filename=filename,
            target_seconds=timestamp_seconds,
            target_frame=target_frame,
            track_index=tidx,
            clip_name=actual_filename,
        )

    def execute_plan(
        self,
        placements: List[Dict[str, Any]],
        *,
        sfx_track_name: str = DEFAULT_SFX_TRACK_NAME,
    ) -> PlacementReport:
        """Execute a complete SFX placement plan.

        Each placement dict should contain:
        - sfx_path: str - Path to the SFX file
        - timestamp_seconds: float - Timeline position in seconds
        - duration_seconds: float (optional) - Desired clip duration
        - reason: str (optional) - Why this SFX was chosen

        Args:
            placements: List of placement dictionaries.
            sfx_track_name: Name for the SFX track.

        Returns:
            PlacementReport with complete results.
        """
        report = PlacementReport(
            success=True,
            total_planned=len(placements),
            total_placed=0,
            total_failed=0,
            track_index=0,
            fps=self.fps,
        )

        if not placements:
            report.warnings.append("No placements in plan")
            return report

        # Step 1: Setup track
        track_idx = self.find_or_create_sfx_track(sfx_track_name)
        report.track_index = track_idx

        # Step 2: Collect all file paths for batch import
        all_paths = []
        for p in placements:
            sfx_path = p.get("sfx_path", "")
            duration = p.get("duration_seconds")
            if sfx_path and os.path.exists(sfx_path):
                if duration and sfx_path.lower().endswith(".wav"):
                    sting_path = self.prepare_sting(sfx_path, duration)
                    if sting_path:
                        all_paths.append(sting_path)
                    else:
                        all_paths.append(sfx_path)
                else:
                    all_paths.append(sfx_path)
            elif sfx_path:
                report.errors.append(f"File not found: {sfx_path}")

        # Batch import
        if all_paths:
            self.import_sfx_files(all_paths)

        # Step 3: Place each SFX
        for p in sorted(placements, key=lambda x: x.get("timestamp_seconds", 0)):
            sfx_path = p.get("sfx_path", "")
            timestamp = p.get("timestamp_seconds", 0.0)
            duration = p.get("duration_seconds")

            if not sfx_path or not os.path.exists(sfx_path):
                report.total_failed += 1
                report.results.append(PlacementResult(
                    success=False,
                    sfx_filename=os.path.basename(sfx_path),
                    target_seconds=timestamp,
                    target_frame=self.seconds_to_frame(timestamp),
                    error=f"File not found: {sfx_path}",
                ))
                continue

            result = self.place_single(
                sfx_path,
                timestamp,
                duration_seconds=duration,
                track_index=track_idx,
            )
            report.results.append(result)

            if result.success:
                report.total_placed += 1
            else:
                report.total_failed += 1
                report.errors.append(
                    f"Failed to place {result.sfx_filename}: {result.error}"
                )

        report.success = report.total_failed == 0

        logger.info(
            "Placement complete: %d/%d placed, %d failed",
            report.total_placed, report.total_planned, report.total_failed,
        )

        return report

    # ─── Verification ────────────────────────────────────────────────

    def verify_placements(
        self,
        expected_count: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Verify SFX placements on the timeline via readback.

        Reads back all items on the SFX track and validates:
        - Items exist on the correct track
        - Items are at expected frame positions
        - No overlapping items
        - Spacing between items meets minimum requirement

        Returns:
            Verification report dict.
        """
        track_idx = self.get_sfx_track_index()
        items = self.timeline.GetItemListInTrack("audio", track_idx) or []

        verified = []
        issues = []
        prev_end = -1

        for item in items:
            name = item.GetName() if hasattr(item, "GetName") else "unknown"
            start = item.GetStart() if hasattr(item, "GetStart") else 0
            end = item.GetEnd() if hasattr(item, "GetEnd") else 0
            start_sec = self.frame_to_seconds(int(start))
            end_sec = self.frame_to_seconds(int(end))

            entry = {
                "name": name,
                "start_frame": int(start),
                "end_frame": int(end),
                "start_seconds": round(start_sec, 3),
                "end_seconds": round(end_sec, 3),
                "duration_seconds": round(end_sec - start_sec, 3),
                "track_index": track_idx,
            }

            # Check for overlap with previous item
            if prev_end > 0 and int(start) < prev_end:
                gap_seconds = self.frame_to_seconds(int(start)) - self.frame_to_seconds(prev_end)
                issues.append({
                    "type": "overlap",
                    "item": name,
                    "gap_seconds": round(gap_seconds, 3),
                    "detail": f"{name} overlaps previous item by {abs(gap_seconds):.3f}s",
                })
            elif prev_end > 0:
                gap_seconds = self.frame_to_seconds(int(start)) - self.frame_to_seconds(prev_end)
                if gap_seconds < 1.0:
                    issues.append({
                        "type": "too_close",
                        "item": name,
                        "gap_seconds": round(gap_seconds, 3),
                        "detail": f"{name} is only {gap_seconds:.3f}s after previous item",
                    })

            verified.append(entry)
            prev_end = int(end)

        result = {
            "success": len(issues) == 0,
            "track_index": track_idx,
            "track_name": self.timeline.GetTrackName("audio", track_idx),
            "total_items": len(verified),
            "items": verified,
            "issues": issues,
        }

        if expected_count is not None:
            result["expected_count"] = expected_count
            if len(verified) != expected_count:
                result["success"] = False
                issues.append({
                    "type": "count_mismatch",
                    "detail": (
                        f"Expected {expected_count} items, found {len(verified)}"
                    ),
                })

        return result

    # ─── Cleanup ─────────────────────────────────────────────────────

    def remove_all_sfx(self) -> Dict[str, Any]:
        """Remove all SFX items from the SFX track.

        Returns:
            Dict with success status and count of removed items.
        """
        track_idx = self.get_sfx_track_index()
        items = self.timeline.GetItemListInTrack("audio", track_idx) or []

        if not items:
            return {"success": True, "removed": 0, "message": "No items to remove"}

        try:
            result = self.timeline.DeleteTimelineItems(list(items))
            count = len(items)
            logger.info("Removed %d SFX items from track %d", count, track_idx)
            return {"success": bool(result), "removed": count}
        except Exception as exc:
            logger.error("Failed to remove SFX items: %s", exc)
            return {"success": False, "removed": 0, "error": str(exc)}

    # ─── Timeline Info ───────────────────────────────────────────────

    def get_timeline_info(self) -> Dict[str, Any]:
        """Get current timeline information relevant to SFX placement.

        Returns:
            Dict with timeline properties.
        """
        fps = self.fps
        start = self.start_frame
        end_frame = self.timeline.GetEndFrame()
        end = int(end_frame) if end_frame is not None else 0
        duration_frames = end - start
        duration_seconds = duration_frames / fps if fps > 0 else 0.0

        # Count tracks
        audio_tracks = int(self.timeline.GetTrackCount("audio") or 0)
        video_tracks = int(self.timeline.GetTrackCount("video") or 0)

        # Audio track details
        audio_track_info = []
        for i in range(1, audio_tracks + 1):
            name = self.timeline.GetTrackName("audio", i)
            items = self.timeline.GetItemListInTrack("audio", i) or []
            audio_track_info.append({
                "index": i,
                "name": name,
                "item_count": len(items),
            })

        return {
            "name": self.timeline.GetName() if hasattr(self.timeline, "GetName") else "unknown",
            "fps": fps,
            "start_frame": start,
            "end_frame": end,
            "duration_frames": duration_frames,
            "duration_seconds": round(duration_seconds, 3),
            "audio_track_count": audio_tracks,
            "video_track_count": video_tracks,
            "audio_tracks": audio_track_info,
        }
