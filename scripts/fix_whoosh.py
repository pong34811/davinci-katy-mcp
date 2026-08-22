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

items = tl.GetItemListInTrack("audio", 2)
for it in items:
    if it.GetName() == "whoosh-intro-12.wav":
        print("found whoosh at", it.GetStart(), "-> deleting")
        print("delete:", tl.DeleteClips([it]))
        break

# re-append whoosh at 73.1s (transition into new rules segment, gap 72.40-73.18)
root = mp.GetRootFolder()
sfx_bin = None
for m in root.GetSubFolderList():
    if m.GetName() == "Master":
        for s in m.GetSubFolderList():
            if s.GetName() == "SFX":
                sfx_bin = s
mp.SetCurrentFolder(sfx_bin)
item = next(c for c in sfx_bin.GetClipList() if c.GetName() == "whoosh-intro-12.wav")
info = {
    "mediaPoolItem": item,
    "startFrame": 0,
    "endFrame": 36,
    "trackIndex": 2,
    "recordFrame": int(73.1 * fps),
    "mediaType": 2,
}
res = mp.AppendToTimeline([info])
print("re-append:", res is not None)
for it in res:
    print("NEW whoosh at", it.GetStart(), it.GetStart()/fps, "s")