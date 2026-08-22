import os, sys
os.environ["RESOLVE_SCRIPT_API"] = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
os.environ["RESOLVE_SCRIPT_LIB"] = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
sys.path.append(r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules")

import DaVinciResolveScript as dvr
resolve = dvr.scriptapp("Resolve")
proj = resolve.GetProjectManager().GetCurrentProject()
tl = proj.GetCurrentTimeline()
fps = float(tl.GetSetting("timelineFrameRate"))

# dialogue timeline from srt: (start_f, end_f)
dialogue = [
    (0,127),(128,242),(242,357),(379,549),(554,640),(640,725),(725,901),(906,995),(995,1084),
    (1316,1550),(1550,1648),(1648,1745),(1745,1843),(1863,1995),(2006,2195),(2195,2308),
    (2339,2485),(2485,2630),(2638,2875),(2876,3030),(3030,3176),(3176,3264),(3264,3390),
    (3391,3557),(3557,3658),(3658,3758),(3758,3845),(3845,3923),(3923,3999),(3999,4070),
    (4070,4119),(4070,4119),(4119,4241),(4267,4344),(4391,4460),(4460,4530),(4700,4760),
    (4760,4818),(4818,4888),(4888,4970),(4970,4995),(5114,5177),(5182,5197),(5262,5355),
    (5355,5385),(5385,5435),(5583,5683),(5683,5760),(5760,5803),(5803,5827),(5836,5907),
    (6023,6183),(6183,6241),(6241,6436),(6436,6631),(6631,6826),(6827,6994),(6994,7160),
    (7160,7220),(7220,7260),(7260,7300),(7300,7369),(7369,7470),(7507,7643),
]
# decode (start_f, end_f) from seconds
def sec(s): return round(s*fps)
dialogue = [(sec(0.0),sec(2.117)),(sec(2.133),sec(4.033)),(sec(4.033),sec(5.950)),
    (sec(6.317),sec(9.150)),(sec(9.233),sec(10.667)),(sec(10.667),sec(12.083)),(sec(12.083),sec(15.017)),
    (sec(15.100),sec(16.583)),(sec(16.583),sec(18.067)),
    (sec(21.933),sec(25.833)),(sec(25.833),sec(27.467)),(sec(27.467),sec(29.083)),(sec(29.083),sec(30.717)),
    (sec(31.050),sec(33.250)),(sec(33.433),sec(36.583)),(sec(36.583),sec(38.467)),
    (sec(38.983),sec(41.417)),(sec(41.417),sec(43.833)),(sec(43.967),sec(47.917)),(sec(47.933),sec(50.500)),
    (sec(50.500),sec(52.933)),(sec(52.933),sec(54.400)),(sec(54.400),sec(56.500)),(sec(56.517),sec(59.283)),
    (sec(59.283),sec(60.967)),(sec(60.967),sec(62.633)),(sec(62.633),sec(64.083)),(sec(64.083),sec(65.383)),
    (sec(65.383),sec(66.650)),(sec(66.650),sec(67.833)),(sec(67.833),sec(68.433)),(sec(68.433),sec(70.683)),
    (sec(71.117),sec(72.400)),(sec(73.183),sec(74.333)),(sec(74.333),sec(75.500)),(sec(75.500),sec(76.667)),
    (sec(78.333),sec(79.333)),(sec(79.333),sec(80.300)),(sec(80.300),sec(81.600)),(sec(81.600),sec(82.883)),
    (sec(82.883),sec(85.150)),(sec(85.150),sec(85.900)),(sec(88.567),sec(89.283)),(sec(89.700),sec(92.583)),
    (sec(93.050),sec(94.717)),(sec(94.717),sec(95.667)),(sec(95.667),sec(96.767)),(sec(96.767),sec(97.267)),
    (sec(97.267),sec(98.450)),(sec(98.450),sec(99.150)),(sec(100.517),sec(103.050)),(sec(103.050),sec(104.017)),
    (sec(104.017),sec(107.267)),(sec(107.267),sec(110.517)),(sec(110.517),sec(113.767)),(sec(113.783),sec(116.567)),
    (sec(116.567),sec(119.333)),(sec(119.333),sec(120.533)),(sec(120.533),sec(121.833)),(sec(121.833),sec(123.117)),
    (sec(125.117),sec(127.400))]

sfx_items = tl.GetItemListInTrack("audio", 2)
print("=== SFX TRACK READBACK ===")
issues = []
for item in sfx_items:
    name = item.GetName()
    start = item.GetStart()
    end = item.GetEnd()
    dur = end - start
    overlap = None
    for ds, de in dialogue:
        if start < de and end > ds + 0:  # any frame overlap with dialogue
            overlap = (round(ds/fps,2), round(de/fps,2))
            break
    status = "OVERLAP-DIALOGUE" if overlap else "gap-ok"
    print(f"{name}: start={start}f ({start/fps:.2f}s) dur={dur}f  -> {status}")
    if overlap:
        issues.append((name, overlap))
print("=== DIALOGUE OVERLAPS:", len(issues), "===")
for i in issues:
    print(i)