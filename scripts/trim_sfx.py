import os, sys
os.environ["RESOLVE_SCRIPT_API"] = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
os.environ["RESOLVE_SCRIPT_LIB"] = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
sys.path.append(r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules")

import DaVinciResolveScript as dvr
resolve = dvr.scriptapp("Resolve")
proj = resolve.GetProjectManager().GetCurrentProject()
tl = proj.GetCurrentTimeline()
fps = float(tl.GetSetting("timelineFrameRate"))

# Targets: name -> desired end frame
# sparkle: 1718 + 36 = 1754, whoosh: 2160 + 30 = 2190
targets = {
    "sparkle-10.wav": 1754,
    "whoosh-clean-12.wav": 2190,
}

items = tl.GetItemListInTrack("audio", 3)
for it in items:
    name = it.GetName()
    if name in targets:
        new_end = targets[name]
        cur_end = it.GetEnd()
        print(f"{name}: current end={cur_end}f ({cur_end/fps:.2f}s), target end={new_end}f ({new_end/fps:.2f}s)")
        ok = it.SetEndFrame(new_end)
        print(f"  SetEndFrame({new_end}) -> {ok}")
        # readback
        print(f"  now: start={it.GetStart()}f end={it.GetEnd()}f dur={it.GetEnd()-it.GetStart()}f")

print()
print("=== FINAL SFX TRACK 3 ===")
for it in tl.GetItemListInTrack("audio", 3):
    s = it.GetStart()
    e = it.GetEnd()
    print(f"  {it.GetName()}: {s/fps:.2f}s - {e/fps:.2f}s ({(e-s)/fps:.2f}s)")