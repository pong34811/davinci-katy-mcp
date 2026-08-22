import os, sys, re
os.environ["RESOLVE_SCRIPT_API"] = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
os.environ["RESOLVE_SCRIPT_LIB"] = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
sys.path.append(r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules")
import DaVinciResolveScript as dvr

resolve = dvr.scriptapp("Resolve")
proj = resolve.GetProjectManager().GetCurrentProject()
tl = proj.GetCurrentTimeline()
fps = tl.GetSetting("timelineFrameRate") or 30.0
print("timeline:", repr(tl.GetName()), "fps:", fps)

items = []
for ti in range(1, tl.GetTrackCount("video") + 1):
    items += tl.GetItemListInTrack("video", ti) or []
items.sort(key=lambda x: x.GetStart())
print("total items:", len(items))

def strip(v):
    if not isinstance(v, str):
        return str(v)
    v = re.sub(r"<[^>]+>", " ", v)
    return re.sub(r"\s+", " ", v).strip()

for it in items:
    start = it.GetStart() / fps
    end = it.GetEnd() / fps
    text = ""
    try:
        cnt = it.GetFusionCompCount() or 0
        if cnt > 0:
            comp = it.GetFusionCompByIndex(1)
            if comp:
                for tool in comp.GetToolList().values():
                    try:
                        reg = (tool.GetAttrs() or {}).get("TOOLS_RegID", "")
                    except Exception:
                        reg = ""
                    if "Text" in reg:
                        v = tool.GetInput("StyledText")
                        if v:
                            text = strip(v)
                            break
    except Exception as exc:
        text = f"<err {exc}>"
    print(f"{start:6.2f}s - {end:6.2f}s  comps={cnt if 'cnt' in dir() else '?'}  {text!r}")