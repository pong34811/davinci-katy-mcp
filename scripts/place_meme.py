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
print("FPS:", fps)

# 1. ensure SFX track
na = tl.GetTrackCount("audio")
sfx_idx = None
for i in range(1, na+1):
    if tl.GetTrackName("audio", i) == "SFX 1":
        sfx_idx = i
        break
if sfx_idx is None:
    tl.AddTrack("audio")
    sfx_idx = tl.GetTrackCount("audio")
    tl.SetTrackName("audio", sfx_idx, "SFX 1")
print("SFX track index:", sfx_idx)

# 2. import into Master/SFX bin (reuse existing)
root = mp.GetRootFolder()
sfx_bin = None
for m in root.GetSubFolderList():
    if m.GetName() == "Master":
        for s in m.GetSubFolderList():
            if s.GetName() == "SFX":
                sfx_bin = s
if sfx_bin is None:
    master = None
    for m in root.GetSubFolderList():
        if m.GetName() == "Master":
            master = m
    if master is None:
        master = mp.AddSubFolder(root, "Master")
    sfx_bin = mp.AddSubFolder(master, "SFX")
mp.SetCurrentFolder(sfx_bin)
existing = {c.GetName(): c for c in sfx_bin.GetClipList()}
need = ["sparkle-10.wav","ding-12.wav","pop-10.wav","collect-10.wav","pop-13.wav"]
to_import = [os.path.join(r"Z:\SFX_processed", f) for f in need if f not in existing]
if to_import:
    res = mp.ImportMedia(to_import)
    print("imported:", len(res) if res else 0)
pool = {c.GetName(): c for c in sfx_bin.GetClipList()}

# 3. place 5 stings
placements = [
    ("sparkle-10.wav", 0.12, 42),  # เปิด
    ("ding-12.wav",     9.58, 30),  # เผยวันเกิด
    ("pop-10.wav",     11.95, 24),  # เย้
    ("collect-10.wav", 13.23, 30),  # วันที่สำคัญ
    ("pop-13.wav",     32.52, 24),  # จุ๊บๆ
]
infos = []
for name, sec, flen in placements:
    item = pool.get(name)
    if item is None:
        print("MISSING:", name); sys.exit(1)
    infos.append({
        "mediaPoolItem": item,
        "startFrame": 0,
        "endFrame": flen,
        "trackIndex": sfx_idx,
        "recordFrame": int(round(sec*fps)),
        "mediaType": 2,
    })
result = mp.AppendToTimeline(infos)
print("APPEND:", result is not None)
if result:
    for it in result:
        print("PLACED:", it.GetName(), "track:", it.GetTrackTypeAndIndex(), "start:", it.GetStart(), f"({it.GetStart()/fps:.2f}s)")