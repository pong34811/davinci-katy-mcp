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
print(f"FPS: {fps}, Timeline: {tl.GetName()}")
print(f"Duration: {tl.GetEndFrame()} frames = {tl.GetEndFrame()/fps:.1f}s")

# --- Step 1: Create Master/SFX bin ---
root = mp.GetRootFolder()
master = None
for f in root.GetSubFolderList():
    if f.GetName() == "Master":
        master = f
        break
if master is None:
    master = mp.AddSubFolder(root, "Master")
    print("Created Master folder")

sfx_bin = None
for f in master.GetSubFolderList():
    if f.GetName() == "SFX":
        sfx_bin = f
        break
if sfx_bin is None:
    sfx_bin = mp.AddSubFolder(master, "SFX")
    print("Created SFX bin")
else:
    print("SFX bin already exists")

# --- Step 2: Import SFX files ---
mp.SetCurrentFolder(sfx_bin)
existing = {c.GetName(): c for c in sfx_bin.GetClipList()}
print(f"Existing clips in SFX bin: {len(existing)}")

sfx_files = [
    r"Z:\SFX_processed\ding-12.wav",
    r"Z:\SFX_processed\pop-14.wav",
    r"Z:\SFX_processed\sparkle-10.wav",
    r"Z:\SFX_processed\whoosh-clean-12.wav",
]

to_import = [f for f in sfx_files if os.path.basename(f) not in existing]
if to_import:
    print(f"Importing {len(to_import)} files...")
    clips = mp.ImportMedia(to_import)
    if clips:
        for c in clips:
            print(f"  Imported: {c.GetName()}")
    else:
        print("IMPORT FAILED")
        sys.exit(1)
else:
    print("All SFX already imported")

# Refresh pool items
pool_items = {c.GetName(): c for c in sfx_bin.GetClipList()}
print(f"SFX bin now has {len(pool_items)} clips: {list(pool_items.keys())}")

# --- Step 3: Add SFX audio track ---
na_before = tl.GetTrackCount("audio")
# Check if we already have an SFX track
sfx_track_index = None
for i in range(1, na_before + 1):
    name = tl.GetTrackName("audio", i)
    if "SFX" in name.upper():
        sfx_track_index = i
        print(f"Found existing SFX track at index {i}: {name}")
        break

if sfx_track_index is None:
    tl.AddTrack("audio")
    na_after = tl.GetTrackCount("audio")
    sfx_track_index = na_after
    tl.SetTrackName("audio", sfx_track_index, "SFX 1")
    print(f"Created SFX track at index {sfx_track_index}")

# --- Step 4: Place SFX ---
placements = [
    ("ding-12.wav",        11.80, 30),  # 10K subscriber goal emphasis
    ("pop-14.wav",         15.17, 24),  # Cow surprise reaction
    ("sparkle-10.wav",     28.63, 36),  # Current subscriber count celebration
    ("whoosh-clean-12.wav",36.00, 30),  # Transition to outro
]

clip_infos = []
for name, sec, flen in placements:
    item = pool_items.get(name)
    if item is None:
        print(f"MISSING in pool: {name}")
        sys.exit(1)
    rf = int(tl.GetStartFrame() + round(sec * fps))
    clip_infos.append({
        "mediaPoolItem": item,
        "startFrame": 0,
        "endFrame": flen,
        "trackIndex": sfx_track_index,
        "recordFrame": rf,
        "mediaType": 2,
    })
    print(f"PLANNED {name}: recordFrame={rf} ({rf/fps:.2f}s), len {flen}f ({flen/fps:.2f}s)")

print(f"\nAppending {len(clip_infos)} SFX to timeline...")
result = mp.AppendToTimeline(clip_infos)
if result is None:
    print("APPEND FAILED")
    sys.exit(1)

print(f"\n=== PLACEMENT RESULTS ===")
for item in result:
    ti = item.GetTrackTypeAndIndex()
    print(f"  {item.GetName()} | track={ti} | start={item.GetStart()} ({item.GetStart()/fps:.2f}s) | end={item.GetEnd()} ({item.GetEnd()/fps:.2f}s)")

# --- Step 5: Verify ---
print(f"\n=== VERIFICATION ===")
sfx_items = tl.GetItemListInTrack("audio", sfx_track_index)
print(f"SFX track has {len(sfx_items)} items")
for item in sfx_items:
    name = item.GetName()
    start = item.GetStart()
    end = item.GetEnd()
    dur = end - start
    print(f"  {name}: start={start}f ({start/fps:.2f}s) dur={dur}f ({dur/fps:.2f}s)")

print("\nDone!")
