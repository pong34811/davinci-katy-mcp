import os, sys
os.environ["RESOLVE_SCRIPT_API"] = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
os.environ["RESOLVE_SCRIPT_LIB"] = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
sys.path.append(r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules")

import DaVinciResolveScript as dvr
resolve = dvr.scriptapp("Resolve")
proj = resolve.GetProjectManager().GetCurrentProject()
mp = proj.GetMediaPool()
tl = proj.GetCurrentTimeline()
fps = float(tl.GetSetting("timelineFrameRate"))

print("audio tracks:", tl.GetTrackCount("audio"))
for i in range(1, tl.GetTrackCount("audio") + 1):
    print(f"  A{i}: '{tl.GetTrackName('audio', i)}' items={len(tl.GetItemListInTrack('audio', i))}")

# SFX bin clip durations
root = mp.GetRootFolder()
sfx_bin = None
for f in root.GetSubFolderList():
    if f.GetName() == "Master":
        for s in f.GetSubFolderList():
            if s.GetName() == "SFX":
                sfx_bin = s
print("SFX bin:", sfx_bin)
if sfx_bin:
    for c in sfx_bin.GetClipList():
        print(f"  {c.GetName()}: duration={c.GetClipProperty('Duration')}")

# current timeline setting: playhead, in/out
print("current folder:", mp.GetCurrentFolder().GetName())