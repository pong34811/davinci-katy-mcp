import os, sys
os.environ["RESOLVE_SCRIPT_API"] = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
os.environ["RESOLVE_SCRIPT_LIB"] = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
sys.path.append(r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules")

import DaVinciResolveScript as dvr
resolve = dvr.scriptapp("Resolve")
proj = resolve.GetProjectManager().GetCurrentProject()
tl = proj.GetCurrentTimeline()
fps = float(tl.GetSetting("timelineFrameRate"))

print("=== AUDIO TRACKS ===")
for i in range(1, tl.GetTrackCount("audio") + 1):
    name = tl.GetTrackName("audio", i)
    items = tl.GetItemListInTrack("audio", i)
    print(f"  A{i}: {name} - {len(items)} items")
    for it in items:
        print(f"    {it.GetName()}: {it.GetStart()/fps:.2f}s - {it.GetEnd()/fps:.2f}s")

print()
print("=== SFX SPACING CHECK (min 1s apart) ===")
sfx = sorted([(it.GetStart(), it.GetEnd(), it.GetName()) for it in tl.GetItemListInTrack("audio", 3)])
for i in range(len(sfx) - 1):
    gap = (sfx[i + 1][0] - sfx[i][1]) / fps
    status = "OK" if gap >= 1.0 else "TOO CLOSE"
    print(f"  {sfx[i][2]} -> {sfx[i+1][2]}: gap={gap:.2f}s [{status}]")
print(f"  Total SFX: {len(sfx)}")