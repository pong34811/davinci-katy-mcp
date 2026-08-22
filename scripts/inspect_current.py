import os, sys
os.environ["RESOLVE_SCRIPT_API"] = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
os.environ["RESOLVE_SCRIPT_LIB"] = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
sys.path.append(r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules")
import DaVinciResolveScript as dvr
resolve = dvr.scriptapp("Resolve")
proj = resolve.GetProjectManager().GetCurrentProject()
print("PROJECT:", proj.GetName())
print("---TIMELINES---")
for i in range(1, proj.GetTimelineCount()+1):
    t = proj.GetTimelineByIndex(i)
    print(f"  [{i}] {t.GetName()}")
tl = proj.GetCurrentTimeline()
print("CURRENT:", tl.GetName())
print("FPS:", tl.GetSetting("timelineFrameRate"), "start:", tl.GetStartFrame(), "end:", tl.GetEndFrame(), "dur_s:", round((tl.GetEndFrame()-tl.GetStartFrame())/float(tl.GetSetting("timelineFrameRate")),1))
print("---MEMBERS---")
for m in tl.GetTrackCount("audio") and range(1, tl.GetTrackCount("audio")+1) or []:
    items = tl.GetItemListInTrack("audio", m)
    print(f"audio {m}: '{tl.GetTrackName('audio', m)}' items={len(items)}")
    for it in items:
        print(f"    {it.GetName()} start={it.GetStart()} end={it.GetEnd()}")
for m in range(1, tl.GetTrackCount("video")+1):
    items = tl.GetItemListInTrack("video", m)
    print(f"video {m}: '{tl.GetTrackName('video', m)}' items={len(items)}")
print("---TRANSCRIPT---")
tr = tl.GetTranscript() if hasattr(tl, "GetTranscript") else None
if tr and len(tr) > 0:
    for seg in tr:
        print(f"  [{seg.get('start',0)/1000:.1f}s-{seg.get('end',0)/1000:.1f}s] {seg.get('text','')[:80]}")
else:
    print("  (none)")
print("---MARKERS---")
print(tl.GetMarkers())