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

root = mp.GetRootFolder()
sfx_bin = None
for f in root.GetSubFolderList():
    if f.GetName() == "Master":
        for s in f.GetSubFolderList():
            if s.GetName() == "SFX":
                sfx_bin = s
mp.SetCurrentFolder(sfx_bin)
pool_items = {c.GetName(): c for c in sfx_bin.GetClipList()}

# per-clip known trimmed frame lengths
lens = {
    "pop-14-sting.wav": 24,
    "ding-12-sting.wav": 30,
    "sparkle-10-sting.wav": 36,
    "whoosh-clean-12-sting.wav": 30,
}
placements = [
    ("pop-14-sting.wav",        520, "วันที่ 10 joke punchline"),
    ("ding-12-sting.wav",       926, "1,000 sub goal number"),
    ("sparkle-10-sting.wav",   1453, "1,671 actual count"),
    ("whoosh-clean-12-sting.wav", 2280, "topic shift to other clips"),
]
clip_infos = []
for name, rf, why in placements:
    item = pool_items.get(name)
    if item is None:
        print("MISSING:", name); sys.exit(1)
    flen = lens[name]
    clip_infos.append({
        "mediaPoolItem": item,
        "startFrame": 0,
        "endFrame": flen,
        "trackIndex": 2,
        "recordFrame": rf,
        "mediaType": 2,
    })
    print(f"PLANNED {name} @ {rf}f ({rf/fps:.2f}s) len {flen}f")

print("track count before:", tl.GetTrackCount("audio"))
result = mp.AppendToTimeline(clip_infos)
print("APPEND:", "OK" if result else "FAILED")
if result:
    for it in result:
        print("PLACED:", it.GetName(), it.GetTrackTypeAndIndex(), it.GetStart())