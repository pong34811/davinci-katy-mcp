#!/usr/bin/env python3
"""Centralized configuration for DaVinci Resolve SFX System.

All paths and settings are defined here. Import this module to access configuration.
"""

import os
from pathlib import Path
from typing import Dict, Any

# ── Project Paths ────────────────────────────────────────────────────────────

# Root directory (where this file is located)
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent

# SFX directories
SFX_DIR = Path(r"C:\Users\warit\Desktop\davinci-katy-mcp\SFX")
SFX_PROCESSED_DIR = PROJECT_ROOT / "SFX_processed"

# MCP server directory
MCP_DIR = PROJECT_ROOT / "davinci-resolve-mcp"

# Obsidian vault directory
OBSIDIAN_VAULT_DIR = PROJECT_ROOT / "obsidian-vault"

# ── SFX Configuration ────────────────────────────────────────────────────────

# SFX family to file mapping
SFX_FAMILIES: Dict[str, list] = {
    "pop": ["Pop - Short 06.mp3"],
    "ding": ["Bell - Ding 02.wav", "Bell - Ting.mp3"],
    "collect": ["Game - Correct Collect Answer.mp3"],
    "sparkle": ["Harp - Sparkle 01.mp3", "Harp - Sparkle 06.mp3", "Magic - Shimmer 01.mp3"],
    "whoosh": ["Whoosh - Clean Fast.mp3", "Whoosh - Fast 01.mp3", "Transition - Whoosh 01.mp3"],
    "impact": ["Impact - Comedy Hit 01.mp3", "Impact - Comedy Hit 02.mp3"],
    "wrong": ["Game - Wrong Answer.mp3"],
    "honk": ["Horn - Duck Honk 01.mp3", "Horn - Duck Honk 02.mp3"],
    "gong": ["Gong - Comical Metal.wav", "Gong - Metal.wav"],
    "kaching": ["Cash Register - Ka Ching 01.mp3", "Cash Register - Ka Ching 02.mp3"],
    "blip": ["Comedy - Silly Blip 01.mp3", "Marimba - Comedy Blip 02.mp3"],
    "plink": ["Guitar - Plink Slide 13.wav"],
    "scratch": ["Scratch - Turntable Record.mp3"],
    "rise": ["Rise - Build Up.mp3"],
    "awkward": ["Awkward Moment.mp3"],
    "scream": ["Scream - Female 01.mp3", "Scream - Male 01.wav"],
    "glass": ["Glass - Wine Glass Shatter.mp3"],
    "explosion": ["Explosion - Medium 02.wav"],
    "click": ["Click - Button Press.wav", "Click - Sharp 02.wav"],
    "ui": ["UI - Enter Confirm.mp3", "UI - Loading Bar.mp3"],
}

# Beat to SFX family mapping
BEAT_TO_SFX: Dict[str, list] = {
    "surprise": ["pop", "impact"],
    "excitement": ["sparkle", "kaching", "ding"],
    "success": ["collect", "kaching", "ding", "sparkle"],
    "fail": ["wrong", "scratch"],
    "emphasis": ["ding", "pop", "collect"],
    "question": ["pop", "blip"],
    "transition": ["whoosh", "rise"],
    "closing": ["sparkle", "whoosh"],
    "neutral": [],
}

# ── Format Configurations ────────────────────────────────────────────────────

FORMAT_CONFIGS: Dict[str, Dict[str, Any]] = {
    "talking-head": {
        "density_per_minute": 4,
        "max_density_per_minute": 5,
        "sfx_volume_db": -12,
        "bed": "speech",
        "description": "Talking-head / vlog style",
    },
    "game": {
        "density_per_minute": 6,
        "max_density_per_minute": 8,
        "sfx_volume_db": -8,
        "bed": "game_audio",
        "description": "Game footage style",
    },
    "meme": {
        "density_per_minute": 10,
        "max_density_per_minute": 15,
        "sfx_volume_db": -10,
        "bed": "none",
        "description": "Meme / short clip style",
    },
    "podcast": {
        "density_per_minute": 1,
        "max_density_per_minute": 2,
        "sfx_volume_db": -16,
        "bed": "speech_music",
        "description": "Podcast style",
    },
    "livestream": {
        "density_per_minute": 2,
        "max_density_per_minute": 4,
        "sfx_volume_db": -14,
        "bed": "streamer_game",
        "description": "Livestream style",
    },
}

# ── Spacing Configuration ────────────────────────────────────────────────────

MIN_SPACING_SECONDS = 1.0
DEFAULT_DURATION_SECONDS = 0.5

# ── Emotion Keywords ─────────────────────────────────────────────────────────

EMOTION_KEYWORDS: Dict[str, Dict[str, list]] = {
    "surprise": {
        "th": ["มาจากไหน", "ตกใจ", "โอ้โห", "ไม่น่าเชื่อ", "เซอร์ไพรส์", "ทำไม", "จริงหรอ", "เฮ้ย"],
        "en": ["wow", "omg", "surprise", "really", "no way", "holy", "what"],
    },
    "excitement": {
        "th": ["เย้", "สุดยอด", "เจ๋ง", "เทพ", "โคตร", "เริ่ด", "ปัง", "ยินดี"],
        "en": ["yay", "awesome", "amazing", "great", "cool", "love", "best"],
    },
    "success": {
        "th": ["สำเร็จ", "ได้แล้ว", "ชนะ", "ผ่าน", "ถูกต้อง", "เยี่ยม", "สมหวัง"],
        "en": ["success", "win", "pass", "correct", "done", "complete"],
    },
    "fail": {
        "th": ["ล้มเหลว", "ผิด", "ไม่ได้", "พัง", "เจ๊ง", "พลาด", "ตาย"],
        "en": ["fail", "wrong", "lose", "die", "dead", "broken", "error"],
    },
    "emphasis": {
        "th": ["ตัวเลข", "สถิติ", "จำนวน", "เปอร์เซ็นต์", "ล้าน", "พัน", "ร้อย", "บาท"],
        "en": ["first", "second", "third", "most", "only", "every", "always", "never"],
    },
    "question": {
        "th": ["ทำไม", "ยังไง", "อะไร", "ที่ไหน", "เมื่อไหร่", "ใคร"],
        "en": ["why", "how", "what", "where", "when", "who"],
    },
    "transition": {
        "th": ["ต่อไป", "แล้วก็", "นอกจากนี้", "มาดู", "ไปดู", "สำหรับ"],
        "en": ["next", "then", "also", "now", "let's", "moving on"],
    },
    "closing": {
        "th": ["ลาก่อน", "บาย", "เจอกัน", "ขอบคุณ", "ฝากกด", "ติดตาม"],
        "en": ["bye", "see you", "thanks", "subscribe", "follow", "end"],
    },
}


def get_sfx_file(family: str) -> str:
    """Get the first available SFX file from a family."""
    candidates = SFX_FAMILIES.get(family, [])
    for name in candidates:
        path = SFX_DIR / name
        if path.is_file():
            return name
    return ""


def get_sfx_path(filename: str) -> str:
    """Get full path to an SFX file."""
    return str(SFX_DIR / filename)


def get_format_config(format_name: str) -> Dict[str, Any]:
    """Get configuration for a clip format."""
    return FORMAT_CONFIGS.get(format_name, FORMAT_CONFIGS["talking-head"])


# ── Validation ───────────────────────────────────────────────────────────────

def validate_config() -> Dict[str, Any]:
    """Validate configuration and return status."""
    status = {
        "sfx_dir_exists": SFX_DIR.is_dir(),
        "sfx_processed_dir_exists": SFX_PROCESSED_DIR.is_dir(),
        "mcp_dir_exists": MCP_DIR.is_dir(),
        "obsidian_vault_exists": OBSIDIAN_VAULT_DIR.is_dir(),
        "sfx_files_count": 0,
        "missing_files": [],
    }

    if status["sfx_dir_exists"]:
        status["sfx_files_count"] = len(list(SFX_DIR.glob("*")))
        
        # Check if all mapped files exist
        for family, files in SFX_FAMILIES.items():
            for f in files:
                if not (SFX_DIR / f).is_file():
                    status["missing_files"].append(f)

    return status


if __name__ == "__main__":
    # Test configuration
    print("=== Configuration Status ===")
    status = validate_config()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    print("\n=== SFX Families ===")
    for family in SFX_FAMILIES:
        sfx_file = get_sfx_file(family)
        status = "✓" if sfx_file else "✗"
        print(f"  {family}: {status} -> {sfx_file or 'NOT FOUND'}")
