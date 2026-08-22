import os, sys
os.environ["RESOLVE_SCRIPT_API"] = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
os.environ["RESOLVE_SCRIPT_LIB"] = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
sys.path.append(r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules")

import DaVinciResolveScript as dvr
resolve = dvr.scriptapp("Resolve")
proj = resolve.GetProjectManager().GetCurrentProject()
tl = proj.GetCurrentTimeline()
fps = float(tl.GetSetting("timelineFrameRate"))

print("=== SFX TRACK 3 ITEM DETAILS ===")
items = tl.GetItemListInTrack("audio", 3)
for it in items:
    name = it.GetName()
    start = it.GetStart()
    end = it.GetEnd()
    # Get source clip duration for comparison
    print(f"  {name}: start={start}f ({start/fps:.2f}s) end={end}f ({end/fps:.2f}s) dur={(end-start)}f ({(end-start)/fps:.2f}s)")
    print(f"    leftOffset={it.GetLeftOffset()} rightOffset={it.GetRightOffset()}")
    try:
        print(f"    sourceStart={it.GetSourceStartFrame()} sourceEnd={it.GetSourceEndFrame()}")
    except Exception:
        pass