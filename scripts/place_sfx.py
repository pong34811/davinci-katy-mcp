import os, sys
os.environ["RESOLVE_SCRIPT_API"] = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
os.environ["RESOLVE_SCRIPT_LIB"] = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
sys.path.append(r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules")

import DaVinciResolveScript as dvr
resolve = dvr.scriptapp("Resolve")
mp = resolve.GetProjectManager().GetCurrentProject().GetMediaPool()
tl = resolve.GetProjectManager().GetCurrentProject().GetCurrentTimeline()
fps = float(tl.GetSetting("timelineFrameRate"))
print("FPS:", fps, "start:", tl.GetStartFrame())

# snapshots: (filename -> (start_sec, end_sec)) - sting size
# placements: (name, record_sec, frames_len)
placements = [
    ("ding-12.wav",        14.30, 30),  # เป้า 10,000 ซับ
    ("pop-13.wav",         30.20, 24),  # ฤดูหนาว (surprise)
    ("collect-10.wav",     37.00, 30),  # ตัวเลข 1,628
    ("sparkle-10.wav",     44.30, 42),  # ดีใจมากๆ
    ("whoosh-intro-12.wav",71.50, 36),  # transition ประเด็น Youtube
    ("impact-10.wav",     103.50, 30),  # ช็อก 8,000
    ("pop-10.wav",        126.60, 24),  # บ๊ายบาย
]

# get media pool items by name from SFX bin
root = mp.GetRootFolder()
sfx_bin = None
for m in root.GetSubFolderList():
    if m.GetName() == "Master":
        for s in m.GetSubFolderList():
            if s.GetName() == "SFX":
                sfx_bin = s
mp.SetCurrentFolder(sfx_bin)
pool_items = {c.GetName(): c for c in sfx_bin.GetClipList()}

clip_infos = []
for name, sec, flen in placements:
    item = pool_items.get(name)
    if item is None:
        print("MISSING in pool:", name)
        sys.exit(1)
    rf = int(tl.GetStartFrame() + round(sec * fps))
    clip_infos.append({
        "mediaPoolItem": item,
        "startFrame": 0,
        "endFrame": flen,
        "trackIndex": 2,
        "recordFrame": rf,
        "mediaType": 2,
    })
    print(f"PLANNED {name}: recordFrame={rf} ({rf/fps:.2f}s), len {flen}f")

result = mp.AppendToTimeline(clip_infos)
print("APPEND:", result)
if result is None:
    print("APPEND FAILED")
    sys.exit(1)
for item in result:
    print("PLACED:", item.GetName(), "| track:", item.GetTrackTypeAndIndex(), "| start:", item.GetStart())