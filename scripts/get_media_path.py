import os, sys
os.environ["RESOLVE_SCRIPT_API"] = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
os.environ["RESOLVE_SCRIPT_LIB"] = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
sys.path.append(r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules")
import DaVinciResolveScript as dvr
resolve = dvr.scriptapp("Resolve")
proj = resolve.GetProjectManager().GetCurrentProject()
tl = proj.GetCurrentTimeline()
items = tl.GetItemListInTrack("video", 1)
for it in items:
    print("NAME:", it.GetName())
    try:
        props = it.GetClipProperty() or {}
        for k in ("File Path", "File Name", "Path", "Name", "Media Path"):
            if k in props:
                print(k, "=", props[k])
    except Exception as exc:
        print("clipprops err:", exc)