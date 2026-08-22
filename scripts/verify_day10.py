import os, sys
os.environ["RESOLVE_SCRIPT_API"] = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
os.environ["RESOLVE_SCRIPT_LIB"] = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
sys.path.append(r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules")

import DaVinciResolveScript as dvr
resolve = dvr.scriptapp("Resolve")
proj = resolve.GetProjectManager().GetCurrentProject()
tl = proj.GetCurrentTimeline()
fps = 60.0

# dialogue segments from subtitle track
subs = tl.GetItemListInTrack("subtitle", 1)
speech = sorted([(s.GetStart(), s.GetEnd()) for s in subs])

print("=== SFX TRACK 2 READBACK ===")
sfx = []
for it in tl.GetItemListInTrack("audio", 2):
    s, e = it.GetStart(), it.GetEnd()
    name = it.GetName()
    sfx.append((s, e, name))
    print(f"  {name}: {s/fps:.2f}s - {e/fps:.2f}s ({(e-s)/fps:.2f}s)")

sfx.sort()

print("\n=== DIALOGUE OVERLAP CHECK (sting <0.7s on emphasized word = OK) ===")
for s, e, name in sfx:
    overlaps = [(ds, de) for ds, de in speech if s < de and e > ds]
    # how much overlap time
    total_overlap = sum(min(e, de) - max(s, ds) for ds, de in overlaps)
    if overlaps:
        print(f"  {name} @ {s/fps:.2f}s: overlaps {len(overlaps)} seg(s), {total_overlap/fps:.2f}s of {(e-s)/fps:.2f}s")
    else:
        print(f"  {name} @ {s/fps:.2f}s: clean gap")

print("\n=== SPACING ===")
for i in range(len(sfx) - 1):
    gap = (sfx[i+1][0] - sfx[i][1]) / fps
    print(f"  {sfx[i][2]} -> {sfx[i+1][2]}: gap={gap:.2f}s")