import os, sys
os.environ["RESOLVE_SCRIPT_API"] = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
os.environ["RESOLVE_SCRIPT_LIB"] = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
sys.path.append(r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules")
import DaVinciResolveScript as dvr
resolve = dvr.scriptapp("Resolve")
proj = resolve.GetProjectManager().GetCurrentProject()
tl = proj.GetCurrentTimeline()
fps = float(tl.GetSetting("timelineFrameRate"))
items = tl.GetItemListInTrack("audio", 2)
expect = [(14.30),"ding-12.wav"], (30.20,"pop-13.wav"), (37.00,"collect-10.wav"), (44.30,"sparkle-10.wav"), (73.10,"whoosh-intro-12.wav"), (103.50,"impact-10.wav"), (126.60,"pop-10.wav")
exp_pos = dict()
for (t, n) in expect:
    exp_pos[n] = t
if len(items) != len(expect):
    print(f"COUNT MISMATCH: timeline has {len(items)}, expected {len(expect)}")
for it in items:
    name = it.GetName()
    start = it.GetStart()/fps
    exp = exp_pos.get(name)
    status = "OK" if exp is not None and abs(start-exp) < 1.0 else "MISMATCH"
    print(f"{name}: actual={start:.2f}s expected={exp} -> {status}")
# also check video tracks for this timeline type
for i in range(1, tl.GetTrackCount("video")+1):
    print(f"video track {i}: '{tl.GetTrackName('video', i)}' items={len(tl.GetItemListInTrack('video', i))}")