import os, sys
os.environ["RESOLVE_SCRIPT_API"] = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
os.environ["RESOLVE_SCRIPT_LIB"] = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
sys.path.append(r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules")

import DaVinciResolveScript as dvr
resolve = dvr.scriptapp("Resolve")
mp = resolve.GetProjectManager().GetCurrentProject().GetMediaPool()

# navigate to / create Master/SFX bin
root = mp.GetRootFolder()
master = None
for f in root.GetSubFolderList():
    if f.GetName() == "Master":
        master = f
        break
if master is None:
    master = mp.AddSubFolder(root, "Master")
    print("created Master")
sfx_bin = None
for f in master.GetSubFolderList():
    if f.GetName() == "SFX":
        sfx_bin = f
        break
if sfx_bin is None:
    sfx_bin = mp.AddSubFolder(master, "SFX")
    print("created SFX bin")

mp.SetCurrentFolder(sfx_bin)

files = [
    r"Z:\SFX_processed\ding-12.wav",
    r"Z:\SFX_processed\pop-13.wav",
    r"Z:\SFX_processed\collect-10.wav",
    r"Z:\SFX_processed\sparkle-10.wav",
    r"Z:\SFX_processed\whoosh-intro-12.wav",
    r"Z:\SFX_processed\impact-10.wav",
    r"Z:\SFX_processed\pop-10.wav",
]
clips = mp.ImportMedia(files)
if clips is None:
    print("IMPORT FAILED")
    sys.exit(1)
for c in clips:
    print("IMPORTED:", c.GetName(), "id=", c.GetClipProperty("Clip Name"))