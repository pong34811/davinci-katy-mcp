import os, sys, wave, struct
os.environ["RESOLVE_SCRIPT_API"] = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
os.environ["RESOLVE_SCRIPT_LIB"] = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
sys.path.append(r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules")

import DaVinciResolveScript as dvr

# --- trim source wav files (stdlib wave) to target sting lengths ---
def trim_wav(src, dst, dur_sec, fade_sec=0.03):
    with wave.open(src, "rb") as w:
        nch = w.getnchannels()
        sw = w.getsampwidth()
        fr = w.getframerate()
        nframes = w.getnframes()
        data = w.readframes(nframes)
    keep = int(dur_sec * fr)
    nbytes = keep * sw * nch
    body = bytearray(data[:nbytes])
    # linear fade-out over last fade_sec to avoid click
    fade_frames = int(fade_sec * fr)
    if fade_frames > 0 and fade_frames < keep:
        start = keep - fade_frames
        for i in range(fade_frames):
            gain = 1.0 - (i / fade_frames)
            for c in range(nch):
                off = (start + i) * sw * nch + c * sw
                if sw == 2:
                    v = struct.unpack("<h", body[off:off+2])[0]
                    body[off:off+2] = struct.pack("<h", int(v * gain))
    with wave.open(dst, "wb") as w:
        w.setnchannels(nch)
        w.setsampwidth(sw)
        w.setframerate(fr)
        w.writeframes(bytes(body))
    print(f"trimmed {src} -> {dst} ({keep} samples @{fr}Hz = {dur_sec:.2f}s)")

SRC = r"Z:\SFX_processed"
OUT = r"C:\Users\warit\Desktop\davinci-katy-mcp\SFX_processed"
trim_wav(os.path.join(SRC, "sparkle-10.wav"), os.path.join(OUT, "sparkle-10-sting.wav"), 0.60)
trim_wav(os.path.join(SRC, "whoosh-clean-12.wav"), os.path.join(OUT, "whoosh-clean-12-sting.wav"), 0.50)

# --- import trimmed files, replace over-long items on timeline ---
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

new_files = [
    os.path.join(OUT, "sparkle-10-sting.wav"),
    os.path.join(OUT, "whoosh-clean-12-sting.wav"),
]
clips = mp.ImportMedia(new_files)
if clips:
    for c in clips:
        print("IMPORTED:", c.GetName())
pool_items = {c.GetName(): c for c in sfx_bin.GetClipList()}

# delete the two over-long items (full length sparkle + whoosh)
items = tl.GetItemListInTrack("audio", 3)
to_delete = [it for it in items if it.GetName() in ("sparkle-10.wav", "whoosh-clean-12.wav")]
for it in to_delete:
    ok = tl.DeleteTimelineItems([it])
    print("DELETED:", it.GetName(), ok)

# append trimmed replacements at same record frames
placements = [
    ("sparkle-10-sting.wav",    1718, "sparkle-10-sting.wav"),
    ("whoosh-clean-12-sting.wav", 2160, "whoosh-clean-12-sting.wav"),
]
clip_infos = []
for name, rf, poolname in placements:
    item = pool_items.get(poolname)
    if item is None:
        print("MISSING:", poolname)
        sys.exit(1)
    clip_infos.append({
        "mediaPoolItem": item,
        "startFrame": 0,
        "endFrame": 0,  # full clip (already trimmed to desired length)
        "trackIndex": 3,
        "recordFrame": rf,
        "mediaType": 2,
    })
result = mp.AppendToTimeline(clip_infos)
print("APPEND:", "OK" if result else "FAILED")

print()
print("=== FINAL SFX TRACK 3 ===")
for it in tl.GetItemListInTrack("audio", 3):
    s, e = it.GetStart(), it.GetEnd()
    print(f"  {it.GetName()}: {s/fps:.2f}s - {e/fps:.2f}s ({(e-s)/fps:.2f}s)")