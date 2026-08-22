import os, sys
os.environ["RESOLVE_SCRIPT_API"] = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
os.environ["RESOLVE_SCRIPT_LIB"] = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
sys.path.append(r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules")

import DaVinciResolveScript as dvr
resolve = dvr.scriptapp("Resolve")
proj = resolve.GetProjectManager().GetCurrentProject()
tl = proj.GetCurrentTimeline()
fps = 60.0

subs = tl.GetItemListInTrack("subtitle", 1)
subs.sort(key=lambda x: x.GetStart())
for s in subs:
    start = s.GetStart() / fps
    end = s.GetEnd() / fps
    name = s.GetName()
    print(f"{start:6.2f}s - {end:6.2f}s  {name!r}")