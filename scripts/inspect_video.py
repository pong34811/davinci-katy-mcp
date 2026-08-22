import os, sys
os.environ["RESOLVE_SCRIPT_API"] = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
os.environ["RESOLVE_SCRIPT_LIB"] = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
sys.path.append(r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules")
import DaVinciResolveScript as dvr
resolve = dvr.scriptapp("Resolve")
proj = resolve.GetProjectManager().GetCurrentProject()
tl = proj.GetCurrentTimeline()
print("---VIDEO item names---")
for m in range(1, tl.GetTrackCount("video")+1):
    for it in tl.GetItemListInTrack("video", m):
        name = it.GetName()
        print(f"  V{m}: '{name}' clipStart={it.GetLeftOffset()} start={it.GetStart()} end={it.GetEnd()}")
print("---AUDIO item names---")
for it in tl.GetItemListInTrack("audio", 1):
    print(f"  A1: '{it.GetName()}' start={it.GetStart()} end={it.GetEnd()}")
print("---TEXT+ contents on V3---")
for it in tl.GetItemListInTrack("video", 3):
    props = it.GetProperty("Text")
    print(f"  T+ start={it.GetStart()/60:.2f}s end={it.GetEnd()/60:.2f}s text='{props}'")