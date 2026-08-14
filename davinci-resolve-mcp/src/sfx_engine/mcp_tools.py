"""MCP Tools for the SFX Intelligence Engine.

Provides high-level compound MCP actions for:
- sfx_scan: Scanning and inspecting the SFX library.
- sfx_search: Searching SFX by text, category, or event type.
- sfx_analyze: Analyzing video timeline/subtitles to identify beats.
- sfx_plan: Generating an intelligent SFX recommendation plan.
- sfx_execute: Applying the SFX plan onto the DaVinci Resolve timeline.
- sfx_verify: Auditing timeline SFX placements and spacing.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from src.sfx_engine import (
    ContentFormat,
    EventAnalyzer,
    EventType,
    SFXCategory,
    SFXConfig,
    SFXPlacer,
    SFXRecommender,
    SFXScanner,
    SFXSearch,
)

logger = logging.getLogger(__name__)

# Global instances cache
_engine_cache: Dict[str, Any] = {}


def _get_engine(config: Optional[SFXConfig] = None) -> Dict[str, Any]:
    """Get or initialize cached SFX engine components."""
    if "recommender" not in _engine_cache:
        cfg = config or SFXConfig.load()
        scanner = SFXScanner(cfg)
        library = scanner.scan()
        search = SFXSearch(library, cfg)
        analyzer = EventAnalyzer(cfg)
        recommender = SFXRecommender(search, analyzer, cfg)

        _engine_cache.update({
            "config": cfg,
            "scanner": scanner,
            "library": library,
            "search": search,
            "analyzer": analyzer,
            "recommender": recommender,
        })
    return _engine_cache


def handle_sfx_action(action: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Action router for SFX MCP tools.

    Actions:
    - 'scan': Rescan or query SFX library contents.
    - 'search': Search SFX library by query or event.
    - 'analyze': Analyze SRT subtitles or transcript text.
    - 'plan': Generate intelligent SFX recommendation plan.
    - 'execute': Place SFX plan onto DaVinci Resolve timeline.
    - 'verify': Audit timeline SFX placements and spacing.
    - 'remove_all': Clear SFX track on current timeline.
    """
    params = params or {}
    engine = _get_engine()
    action = (action or "").lower().strip()

    if action == "scan":
        force = params.get("force", False)
        library = engine["scanner"].scan(force_rescan=force)
        return {
            "success": True,
            "total_files": len(library.files),
            "families": library.get_all_families(),
            "processed_count": sum(1 for f in library.files if f.is_processed),
            "raw_count": sum(1 for f in library.files if not f.is_processed),
        }

    elif action == "search":
        query = params.get("query")
        event_type = params.get("event_type")
        category = params.get("category")
        limit = params.get("limit", 10)

        if query:
            results = engine["search"].search(query, limit=limit)
            return {
                "success": True,
                "query": query,
                "count": len(results),
                "results": [
                    {
                        "filename": r.file.filename,
                        "family": r.file.family,
                        "category": r.file.category.value,
                        "is_processed": r.file.is_processed,
                        "target_db": r.file.target_db,
                        "score": round(r.score, 2),
                    }
                    for r in results
                ],
            }
        elif event_type:
            try:
                ev = EventType(event_type)
            except ValueError:
                return {"success": False, "error": f"Invalid event_type: {event_type}"}
            candidates = engine["search"].search_by_event(ev)
            return {
                "success": True,
                "event_type": event_type,
                "count": len(candidates),
                "candidates": [c.to_dict() for c in candidates[:limit]],
            }
        elif category:
            try:
                cat = SFXCategory(category)
            except ValueError:
                return {"success": False, "error": f"Invalid category: {category}"}
            files = engine["search"].search_by_category(cat)
            return {
                "success": True,
                "category": category,
                "count": len(files),
                "files": [f.to_dict() for f in files[:limit]],
            }
        else:
            return {"success": False, "error": "Must specify 'query', 'event_type', or 'category'"}

    elif action == "analyze":
        srt_content = params.get("srt_content")
        srt_path = params.get("subtitle_path")
        transcript = params.get("transcript")

        events = []
        if srt_path:
            try:
                with open(srt_path, "r", encoding="utf-8") as f:
                    content = f.read()
                events = engine["analyzer"].analyze_subtitles(content)
            except Exception as exc:
                return {"success": False, "error": f"Failed reading SRT file: {exc}"}
        elif srt_content:
            events = engine["analyzer"].analyze_subtitles(srt_content)
        elif transcript:
            events = engine["analyzer"].analyze_transcript(transcript)
        else:
            return {"success": False, "error": "Must specify 'srt_content', 'subtitle_path', or 'transcript'"}

        beats = engine["analyzer"].find_beats(events, ContentFormat.TALKING_HEAD)
        return {
            "success": True,
            "total_events": len(events),
            "events": [
                {
                    "type": e.type.value,
                    "timestamp": round(e.timestamp, 3),
                    "description": e.description,
                    "score": e.impact_score,
                }
                for e in events
            ],
            "beats": [
                {
                    "type": b.event_type.value,
                    "timestamp": round(b.timestamp, 3),
                    "impact_score": b.impact_score,
                    "description": b.description,
                }
                for b in beats
            ],
        }

    elif action == "plan":
        timeline_info = params.get("timeline_info") or {
            "name": params.get("timeline_name", "Current Timeline"),
            "duration_seconds": params.get("duration_seconds", 120.0),
            "fps": params.get("fps", 60.0),
        }
        srt_path = params.get("subtitle_path")
        srt_content = params.get("srt_content")
        transcript = params.get("transcript")
        format_str = params.get("format")

        override_fmt = None
        if format_str:
            try:
                override_fmt = ContentFormat(format_str)
            except ValueError:
                pass

        plan = engine["recommender"].generate_plan(
            timeline_info=timeline_info,
            transcript=transcript,
            subtitle_path=srt_path,
            srt_content=srt_content,
            override_format=override_fmt,
        )

        return {
            "success": True,
            "plan": plan.to_dict(),
        }

    elif action in ("execute", "verify", "remove_all"):
        # Resolve-dependent actions requiring live app connection handles
        return {
            "success": False,
            "error": f"Action '{action}' must be called with live Resolve context objects.",
            "remediation": "Pass resolve, project, timeline, and media_pool parameters to SFXPlacer.",
        }

    else:
        return {
            "success": False,
            "error": f"Unknown action: '{action}'",
            "supported_actions": ["scan", "search", "analyze", "plan", "execute", "verify", "remove_all"],
        }
