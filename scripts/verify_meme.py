import os, sys
os.environ["RESOLVE_SCRIPT_API"] = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
os.environ["RESOLVE_SCRIPT_LIB"] = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
sys.path.append(r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules")
import DaVinciResolveScript as dvr
resolve = dvr.scriptapp("Resolve")
tl = resolve.GetProjectManager().GetCurrentProject().GetCurrentTimeline()
fps = float(tl.GetSetting("timelineFrameRate"))
expect = {"sparkle-10.wav":0.12,"ding-12.wav":9.58,"pop-10.wav":11.95,"collect-10.wav":13.23,"pop-13.wav":32.52}
print("---SFX TRACK---")
for i in range(1, tl.GetTrackCount("audio")+1):
    for it in tl.GetItemListInTrack("audio", i):
        name = it.GetName()
        if name.endswith(".wav") or name.endswith(".mp3"):
            act = it.GetStart()/fps
            exp = expect.get(name)
            print(f"A{i} '{tl.GetTrackName('audio',i)}' {name}: {act:.2f}s expected={exp} -> {'OK' if exp and abs(act-exp)<0.5 else 'CHECK'}")
# spacing check
times = sorted([it.GetStart()/fps for it in tl.GetItemListInTrack("audio", 2)])
spacing_ok = all(times[i]-times[i-1] >= 1.0 for i in range(1, len(times)))
print("min spacing:", min([times[i]-times[i-1] for i in range(1, len(times))]) if len(times)>1 else "n/a", "(need >=1.0s)")
print("spacing OK:", spacing_ok)