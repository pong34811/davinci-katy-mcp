import os, sys
os.environ["RESOLVE_SCRIPT_API"] = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
os.environ["RESOLVE_SCRIPT_LIB"] = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
sys.path.append(r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules")

import DaVinciResolveScript as dvr
resolve = dvr.scriptapp("Resolve")
proj = resolve.GetProjectManager().GetCurrentProject()
tl = proj.GetCurrentTimeline()
print("FPS:", tl.GetSetting("timelineFrameRate"), "START:", tl.GetStartFrame(), "END:", tl.GetEndFrame())

print("== audio tracks ==")
na = tl.GetTrackCount("audio")
print("audio count:", na)
for i in range(1, na+1):
    try:
        name = tl.GetTrackName("audio", i)
    except Exception as e:
        name = "?"
    items = tl.GetItemListInTrack("audio", i)
    print(f"audio track {i}: name={name} items={len(items)}")

print("== video tracks ==")
nv = tl.GetTrackCount("video")
print("video count:", nv)
for i in range(1, nv+1):
    try:
        name = tl.GetTrackName("video", i)
    except Exception as e:
        name = "?"
    items = tl.GetItemListInTrack("video", i)
    print(f"video track {i}: name={name} items={len(items)}")

print("== markers ==")
for m in tl.GetMarkers().values():
    print(m["name"], m["start"]/60.0, "s")
