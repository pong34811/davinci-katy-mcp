"""SFX Engine Package Entry Point.

Exposes public classes and high-level pipeline runner function.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from src.sfx_engine.analyzer import EventAnalyzer
from src.sfx_engine.config import SFXConfig
from src.sfx_engine.models import (
    BeatPoint,
    ContentFormat,
    EventType,
    SFXCategory,
    SFXFile,
    SFXPlacement,
    SFXPlan,
    TimelineEvent,
)
from src.sfx_engine.placer import PlacementReport, PlacementResult, SFXPlacer
from src.sfx_engine.recommender import SFXRecommender
from src.sfx_engine.scanner import SFXLibrary, SFXScanner
from src.sfx_engine.search import SFXSearch

logger = logging.getLogger(__name__)


def create_sfx_engine(config: Optional[SFXConfig] = None) -> Dict[str, Any]:
    """Factory helper to instantiate complete SFX engine components."""
    cfg = config or SFXConfig.load()
    scanner = SFXScanner(cfg)
    library = scanner.scan()
    search = SFXSearch(library, cfg)
    analyzer = EventAnalyzer(cfg)
    recommender = SFXRecommender(search, analyzer, cfg)

    return {
        "config": cfg,
        "scanner": scanner,
        "library": library,
        "search": search,
        "analyzer": analyzer,
        "recommender": recommender,
    }


__all__ = [
    "SFXConfig",
    "SFXCategory",
    "EventType",
    "ContentFormat",
    "SFXFile",
    "SFXPlacement",
    "SFXPlan",
    "TimelineEvent",
    "BeatPoint",
    "SFXLibrary",
    "SFXScanner",
    "SFXSearch",
    "EventAnalyzer",
    "SFXRecommender",
    "SFXPlacer",
    "PlacementReport",
    "PlacementResult",
    "create_sfx_engine",
]
