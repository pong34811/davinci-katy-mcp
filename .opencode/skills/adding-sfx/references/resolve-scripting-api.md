# Resolve Scripting API — Python Import & Connection Reference

> Session detail: 2026-08-28 live placement on "เรื่องแปลกของยามะ" (20.4s comedy short, 60fps).

## The Segfault Problem

When `DaVinciResolveScript` is imported from the Hermes venv (Python 3.11) **without** DLL path setup, it crashes with Signal 11 / exit 139. This happens because `DaVinciResolveScript.py` is a shim that loads `fusionscript.dll`, a native COM bridge DLL that only resolves when the DLL search path includes the Resolve install directory.

The fix (replicated from `src/server.py` lines 794-813):

```python
import os, sys

RESOLVE_LIB = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
RESOLVE_MODULES = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules"

# 1. Make the .py shim findable
sys.path.insert(0, RESOLVE_MODULES)

# 2. Set up DLL search paths BEFORE import
if os.path.isfile(RESOLVE_LIB):
    _d = os.path.dirname(RESOLVE_LIB)
    if not os.environ.get("PYTHONHOME"):
        os.environ["PYTHONHOME"] = sys.base_prefix
    _cur_path = os.environ.get("PATH", "")
    if _d.lower() not in _cur_path.lower():
        os.environ["PATH"] = _d + os.pathsep + _cur_path
    if hasattr(os, "add_dll_directory"):
        try:
            os.add_dll_directory(_d)
        except OSError:
            pass

# 3. NOW import — no segfault
import DaVinciResolveScript as dvr
resolve = dvr.scriptapp("Resolve")
```

**Critical order**: `sys.path.insert` → set env vars → `add_dll_directory` → `import`. Any reordering causes the segfault.

## Two Connection Modes

### Direct (preferred for CLI scripts)
- Works from the Hermes venv with the DLL setup above
- `resolve = dvr.scriptapp("Resolve")` connects directly to the running Resolve process
- Used by: `scripts/sfx_place.py`, `scripts/analyze_subtitles.py`, direct API calls
- **Check**: `resolve.GetProjectManager().GetCurrentProject()` — returns project or None
- **Verify timeline**: `project.GetCurrentTimeline()` → `GetItemListInTrack("subtitle", 1)`

### In-app bridge (server's normal path)
- Starts from inside Resolve: `Workspace > Scripts > resolve_bridge`
- Connects over loopback; the server uses `BridgeProxy`
- Requires env var `DAVINCI_RESOLVE_BRIDGE=1`
- Used by: `src/server.py` (the MCP server)
- Fallback when direct import segfaults, but requires the bridge script to be running first

## Common Scripting Tasks

```python
# Read subtitles from track 1
timeline = project.GetCurrentTimeline()
subs = timeline.GetItemListInTrack("subtitle", 1)
fps = float(timeline.GetSetting("timelineFrameRate") or 30.0)
for s in sorted(subs, key=lambda x: x.GetStart()):
    print(f"{s.GetStart()/fps:.2f}s: {s.GetName()}")

# Get timeline info
print(f"Tracks: {timeline.GetTrackCount('audio')}")
for i in range(1, timeline.GetTrackCount('audio') + 1):
    print(f"  {i}: {timeline.GetTrackName('audio', i)}")

# Place SFX on a track
media_pool = project.GetMediaPool()
sfx_bin = media_pool.GetRootFolder()  # find Master/SFX
# ... import, find clip, AppendToTimeline
```

## Verified Working (2026-08-28)

- Project: "เรื่องแปลกของยามะ", Timeline 1, 60fps
- 21 subtitle segments on track 1
- 9 SFX placed on Track 2 (SFX 1) — all verified via readback
- Connection: direct via `dvr.scriptapp("Resolve")` with DLL setup
