import os, sys
os.environ["RESOLVE_SCRIPT_API"] = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
os.environ["RESOLVE_SCRIPT_LIB"] = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
sys.path.append(r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules")

import DaVinciResolveScript as dvr
resolve = dvr.scriptapp("Resolve")
proj = resolve.GetProjectManager().GetCurrentProject()
tl = proj.GetCurrentTimeline()
print("TIMELINE:", tl.GetName(), "FPS:", tl.GetSetting("timelineFrameRate"),
      "start:", tl.GetStartFrame(), "end:", tl.GetEndFrame())

fps = float(tl.GetSetting("timelineFrameRate"))
for kind in ("video", "audio"):
    n = tl.GetTrackCount(kind)
    print(f"== {kind} ({n} tracks) ==")
    for i in range(1, n + 1):
        name = tl.GetTrackName(kind, i)
        items = tl.GetItemListInTrack(kind, i)
        print(f"-- {kind} {i}: '{name}' ({len(items)} items)")
        for it in items:
            s = it.GetStart(); e = it.GetEnd()
            d = (e - s) / fps
            print(f"    [{s/fps:6.2f}s-{e/fps:6.2f}s] {it.GetName()}")

print("== markers ==")
markers = tl.GetMarkers() or {}
for frame, m in sorted(markers.items()):
    print(f"  {frame/fps:6.2f}s  color={m.get('color','')} name={m.get('name','')} notes={m.get('notes','')}")

try:
    tr = tl.GetTranscript()
    if tr:
        print("== transcript ==")
        for seg in tr:
            print(f"  [{seg.get('start',0)/1000:.1f}s-{seg.get('end',0)/1000:.1f}s] {seg.get('text','')[:100]}")
except Exception as exc:
    print("transcript unavailable:", exc)