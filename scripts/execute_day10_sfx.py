import os, sys, wave, struct
os.environ["RESOLVE_SCRIPT_API"] = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
os.environ["RESOLVE_SCRIPT_LIB"] = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
sys.path.append(r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules")

import DaVinciResolveScript as dvr

# --- trim helper: stdlib wave only ---
def trim_wav(src, dst, dur_sec, fade_sec=0.03):
    with wave.open(src, "rb") as w:
        nch, sw, fr = w.getnchannels(), w.getsampwidth(), w.getframerate()
        data = w.readframes(w.getnframes())
    keep = int(dur_sec * fr)
    nbytes = keep * sw * nch
    body = bytearray(data[:nbytes])
    fade_frames = int(fade_sec * fr)
    if 0 < fade_frames < keep:
        start = keep - fade_frames
        for i in range(fade_frames):
            gain = 1.0 - (i / fade_frames)
            for c in range(nch):
                off = (start + i) * sw * nch + c * sw
                if sw == 2:
                    v = struct.unpack("<h", body[off:off+2])[0]
                    body[off:off+2] = struct.pack("<h", int(v * gain))
    with wave.open(dst, "wb") as w:
        w.setnchannels(nch); w.setsampwidth(sw); w.setframerate(fr)
        w.writeframes(bytes(body))
    print(f"trimmed -> {os.path.basename(dst)} ({dur_sec:.2f}s)")

SPROC = r"C:\Users\warit\Desktop\davinci-katy-mcp\SFX_processed"
trim_wav(os.path.join(SPROC, "ding-12.wav"), os.path.join(SPROC, "ding-12-sting.wav"), 0.50)
trim_wav(os.path.join(SPROC, "pop-14.wav"), os.path.join(SPROC, "pop-14-sting.wav"), 0.40)

# --- Resolve setup ---
resolve = dvr.scriptapp("Resolve")
proj = resolve.GetProjectManager().GetCurrentProject()
mp = proj.GetMediaPool()
tl = proj.GetCurrentTimeline()
fps = float(tl.GetSetting("timelineFrameRate"))
print(f"Project: {proj.GetName()} | Timeline: {tl.GetName()} | FPS: {fps} | dur: {tl.GetEndFrame()}f")

# --- ensure Master/SFX bin exists ---
root = mp.GetRootFolder()
master = None
for f in root.GetSubFolderList():
    if f.GetName() == "Master":
        master = f
        break
if master is None:
    master = mp.AddSubFolder(root, "Master")
sfx_bin = None
for s in (master.GetSubFolderList() if master else []):
    if s.GetName() == "SFX":
        sfx_bin = s
        break
if sfx_bin is None:
    sfx_bin = mp.AddSubFolder(master, "SFX")
print("SFX bin:", sfx_bin.GetName())

# --- move existing sting clips (in Master) into SFX bin, then import the rest ---
def find_clip(folder, name):
    for c in folder.GetClipList():
        if c.GetName() == name:
            return c
    return None

# clips that already exist in pool (from earlier day-9 work) at any folder
# Move known stray clips from Master into SFX bin
for stray in ("sparkle-10-sting.wav", "whoosh-clean-12-sting.wav"):
    c = find_clip(master, stray)
    if c and not find_clip(sfx_bin, stray):
        mp.MoveClips([c], sfx_bin)
        print(f"moved {stray} -> SFX bin")

# import any missing sting files
mp.SetCurrentFolder(sfx_bin)
want = ["ding-12-sting.wav", "pop-14-sting.wav", "sparkle-10-sting.wav", "whoosh-clean-12-sting.wav"]
have = {c.GetName() for c in sfx_bin.GetClipList()}
paths = [os.path.join(SPROC, n) for n in want if n not in have]
if paths:
    imp = mp.ImportMedia(paths)
    if imp:
        for c in imp:
            print("imported:", c.GetName())
    else:
        print("IMPORT FAILED"); sys.exit(1)

pool_items = {c.GetName(): c for c in sfx_bin.GetClipList()}
print("SFX bin clips:", list(pool_items.keys()))

# --- SFX track ---
sfx_index = None
for i in range(1, tl.GetTrackCount("audio") + 1):
    if "SFX" in (tl.GetTrackName("audio", i) or "").upper():
        sfx_index = i
        break
if sfx_index is None:
    tl.AddTrack("audio")
    sfx_index = tl.GetTrackCount("audio")
    tl.SetTrackName("audio", sfx_index, "SFX 1")
print("SFX track index:", sfx_index)

# --- place (full-length stings, no endFrame reliance) ---
placements = [
    ("pop-14-sting.wav",       8.67, "วันที่ 10 joke punchline"),
    ("ding-12-sting.wav",     15.43, "1,000 sub goal number"),
    ("sparkle-10-sting.wav",  24.22, "1,671 actual count"),
    ("whoosh-clean-12-sting.wav", 38.00, "topic shift to other clips"),
]
clip_infos = []
for name, sec, why in placements:
    item = pool_items.get(name)
    if item is None:
        print("MISSING:", name); sys.exit(1)
    rf = int(round(sec * fps))
    clip_infos.append({
        "mediaPoolItem": item,
        "startFrame": 0,
        "endFrame": 0,
        "trackIndex": sfx_index,
        "recordFrame": rf,
        "mediaType": 2,
    })
    print(f"PLANNED {name} @ {rf}f ({rf/fps:.2f}s)  [{why}]")

result = mp.AppendToTimeline(clip_infos)
if result is None:
    print("APPEND FAILED"); sys.exit(1)

print("\n=== PLACED ===")
for it in tl.GetItemListInTrack("audio", sfx_index):
    s, e = it.GetStart(), it.GetEnd()
    print(f"  {it.GetName()}: {s/fps:.2f}s - {e/fps:.2f}s ({(e-s)/fps:.2f}s)")