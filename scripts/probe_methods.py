import os, sys
os.environ["RESOLVE_SCRIPT_API"] = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
os.environ["RESOLVE_SCRIPT_LIB"] = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
sys.path.append(r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules")

import DaVinciResolveScript as dvr
resolve = dvr.scriptapp("Resolve")
proj = resolve.GetProjectManager().GetCurrentProject()
tl = proj.GetCurrentTimeline()

items = tl.GetItemListInTrack("audio", 3)
it = items[2]  # sparkle
methods = [m for m in dir(it) if not m.startswith("_")]
print("TimelineItem methods:")
for m in sorted(methods):
    print(f"  {m}")