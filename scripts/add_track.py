import os, sys
os.environ["RESOLVE_SCRIPT_API"] = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
os.environ["RESOLVE_SCRIPT_LIB"] = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
sys.path.append(r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules")

import DaVinciResolveScript as dvr
resolve = dvr.scriptapp("Resolve")
proj = resolve.GetProjectManager().GetCurrentProject()
tl = proj.GetCurrentTimeline()
fps = float(tl.GetSetting("timelineFrameRate"))
print("FPS:", fps)

# 1. Add SFX audio track
na_before = tl.GetTrackCount("audio")
added = tl.AddTrack("audio")
print("AddTrack audio:", added)
na_after = tl.GetTrackCount("audio")
print("audio tracks before/after:", na_before, na_after)

# find the SFX track index (newly added)
sfx_index = na_after
# set its name
renamed = tl.SetTrackName("audio", sfx_index, "SFX 1")
print("Rename track", sfx_index, "->", renamed, tl.GetTrackName("audio", sfx_index))
