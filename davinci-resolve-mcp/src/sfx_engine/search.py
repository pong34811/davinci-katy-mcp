"""SFX Search Engine.

Provides fuzzy matching, category search, taxonomy event lookup,
family filtering, and diversity recommendations across the SFX library.
"""

from __future__ import annotations

import difflib
import logging
from typing import Dict, List, Optional

from src.sfx_engine.config import SFXConfig
from src.sfx_engine.models import EventType, SFXCategory, SFXFile, SFXSearchResult
from src.sfx_engine.scanner import SFXLibrary

logger = logging.getLogger(__name__)


# Taxonomy mapping from SKILL.md: EventType -> Priority SFXCategories
EVENT_TAXONOMY_MAP: Dict[EventType, List[SFXCategory]] = {
    EventType.JOKE: [SFXCategory.COMEDY, SFXCategory.ACCENT],
    EventType.REACTION: [SFXCategory.REACTION, SFXCategory.COMEDY],
    EventType.SURPRISE: [SFXCategory.IMPACT, SFXCategory.COMEDY],
    EventType.EMPHASIS: [SFXCategory.ACCENT, SFXCategory.SUCCESS],
    EventType.FAIL: [SFXCategory.FAIL, SFXCategory.COMEDY],
    EventType.TRANSITION: [SFXCategory.TRANSITION, SFXCategory.WHOOSH],
    EventType.SUCCESS: [SFXCategory.SUCCESS, SFXCategory.ACCENT],
    EventType.DRAMATIC: [SFXCategory.DRAMATIC, SFXCategory.IMPACT],
    EventType.ACTION: [SFXCategory.ACTION, SFXCategory.IMPACT, SFXCategory.WHOOSH],
    EventType.UI_NOTIFICATION: [SFXCategory.UI, SFXCategory.ACCENT],
    EventType.INTRO: [SFXCategory.TRANSITION, SFXCategory.SUCCESS],
    EventType.OUTRO: [SFXCategory.TRANSITION, SFXCategory.ACCENT],
}

# Preferred Families by EventType
EVENT_FAMILY_MAP: Dict[EventType, List[str]] = {
    EventType.JOKE: ["pop", "blip", "plink", "honk", "awkward"],
    EventType.REACTION: ["awkward", "huh", "awww"],
    EventType.SURPRISE: ["impact", "scream", "glass", "pop"],
    EventType.EMPHASIS: ["ding", "pop", "collect"],
    EventType.FAIL: ["wrong", "scratch", "bleep"],
    EventType.TRANSITION: ["whoosh", "rise"],
    EventType.SUCCESS: ["collect", "kaching", "ding", "sparkle", "crowd"],
    EventType.DRAMATIC: ["rise", "gong", "metal"],
    EventType.ACTION: ["impact", "whoosh"],
    EventType.UI_NOTIFICATION: ["click", "digital", "keyboard"],
    EventType.INTRO: ["whoosh", "sparkle", "rise"],
    EventType.OUTRO: ["pop", "ding"],
}


class SFXSearch:
    """Search engine for finding the optimal SFX files from the library."""

    def __init__(self, library: SFXLibrary, config: Optional[SFXConfig] = None):
        self.library = library
        self.config = config or SFXConfig.load()

    def search(
        self,
        query: str,
        *,
        limit: int = 5,
        prefer_processed: bool = True,
    ) -> List[SFXSearchResult]:
        """Search SFX files by string query matching filename, tags, or family.

        Args:
            query: Free text search query (e.g., "whoosh", "bell", "punchline").
            limit: Maximum results to return.
            prefer_processed: Boost score of files from SFX_processed.

        Returns:
            List of SFXSearchResult objects sorted by score.
        """
        results: List[SFXSearchResult] = []
        query_lower = query.lower().strip()

        for file in self.library.files:
            score = 0.0
            filename_lower = file.filename.lower()
            family_lower = file.family.lower()

            # Exact family match
            if query_lower == family_lower:
                score += 0.9

            # Substring match in filename
            if query_lower in filename_lower:
                score += 0.7

            # Fuzzy match on filename
            ratio = difflib.SequenceMatcher(None, query_lower, filename_lower).ratio()
            score += ratio * 0.4

            # Tag match
            for tag in file.tags:
                if query_lower in tag.lower():
                    score += 0.5
                    break

            # Boost for processed files
            if prefer_processed and file.is_processed:
                score += 0.15

            if score > 0.2:
                results.append(SFXSearchResult(file=file, score=min(1.0, score)))

        results.sort(key=lambda r: r.score, reverse=True)
        return results[:limit]

    def search_by_category(
        self,
        category: SFXCategory,
        *,
        prefer_processed: bool = True,
    ) -> List[SFXFile]:
        """Get files matching a category.

        Prefers processed files if prefer_processed is True.
        """
        files = self.library.get_by_category(category)
        if prefer_processed:
            proc = [f for f in files if f.is_processed]
            if proc:
                return proc
        return files

    def search_by_event(
        self,
        event_type: EventType,
        *,
        intensity: str = "medium",
        exclude_families: Optional[List[str]] = None,
        prefer_processed: bool = True,
    ) -> List[SFXFile]:
        """Search for the best SFX candidates for a specific video event type.

        Uses the beat taxonomy rules to map events to preferred families and categories.

        Args:
            event_type: The EventType to search for.
            intensity: Event intensity ("low", "medium", "high").
            exclude_families: List of family names to exclude (for variety).
            prefer_processed: Prefer files from SFX_processed.

        Returns:
            List of matching SFXFile candidates.
        """
        excluded = set(f.lower() for f in (exclude_families or []))
        preferred_families = EVENT_FAMILY_MAP.get(event_type, [])

        candidates: List[Tuple[SFXFile, float]] = []

        # 1. Search by preferred families
        for fam in preferred_families:
            if fam.lower() in excluded:
                continue
            family_files = self.library.get_by_family(fam)
            for f in family_files:
                score = 0.8
                if f.is_processed and prefer_processed:
                    score += 0.15
                if f.intensity == intensity:
                    score += 0.1
                candidates.append((f, score))

        # 2. Search by mapped categories if candidates are sparse
        if len(candidates) < 3:
            categories = EVENT_TAXONOMY_MAP.get(event_type, [SFXCategory.ACCENT])
            for cat in categories:
                cat_files = self.library.get_by_category(cat)
                for f in cat_files:
                    if f.family.lower() in excluded:
                        continue
                    # Don't add duplicate
                    if not any(c[0].filename == f.filename for c in candidates):
                        score = 0.5
                        if f.is_processed and prefer_processed:
                            score += 0.15
                        candidates.append((f, score))

        candidates.sort(key=lambda item: item[1], reverse=True)
        return [item[0] for item in candidates]

    def search_by_family(self, family: str) -> List[SFXFile]:
        """Find all files in a specific family."""
        return self.library.get_by_family(family)

    def find_similar(
        self,
        sfx: SFXFile,
        *,
        exclude_same_family: bool = True,
    ) -> List[SFXFile]:
        """Find similar files for fallback or alternative suggestions."""
        results = []
        for file in self.library.files:
            if file.filename == sfx.filename:
                continue
            if exclude_same_family and file.family == sfx.family:
                continue
            if file.category == sfx.category:
                results.append(file)
        return results
