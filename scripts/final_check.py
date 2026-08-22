import os, sys
os.environ["RESOLVE_SCRIPT_API"] = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
os.environ["RESOLVE_SCRIPT_LIB"] = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
sys.path.append(r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules")
import DaVinciResolveScript as dvr
resolve = dvr.scriptapp("Resolve")
if resolve is None:
    print("NO_RESOLVE"); sys.exit(1)
proj = resolve.GetProjectManager().GetCurrentProject()
tl = proj.GetCurrentTimeline()
print("PROJECT:", proj.GetName())
print("TIMELINE:", tl.GetName())
print("FPS:", tl.GetSetting("timelineFrameRate"))
na = tl.GetTrackCount("audio")
for i in range(1, na+1):
    print(f"audio track {i}: '{tl.GetTrackName('audio', i)}' items={len(tl.GetItemListInTrack('audio', i))}")
for item in tl.GetItemListInTrack("audio", na):
    print("  SFX item:", item.GetName(), "start:", item.GetStart(), "end:", item.GetEnd())