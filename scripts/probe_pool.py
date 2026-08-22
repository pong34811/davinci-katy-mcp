import os, sys
os.environ["RESOLVE_SCRIPT_API"] = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
os.environ["RESOLVE_SCRIPT_LIB"] = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
sys.path.append(r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules")

import DaVinciResolveScript as dvr
resolve = dvr.scriptapp("Resolve")
proj = resolve.GetProjectManager().GetCurrentProject()
mp = proj.GetMediaPool()

def dump(folder, indent=0):
    pad = "  " * indent
    clips = folder.GetClipList()
    print(f"{pad}{folder.GetName()} ({len(clips)} clips)")
    for c in clips:
        print(f"{pad}  - {c.GetName()}")
    for s in folder.GetSubFolderList():
        dump(s, indent + 1)

root = mp.GetRootFolder()
print("=== MEDIA POOL TREE ===")
dump(root)

print()
cur = mp.GetCurrentFolder()
print("current folder:", cur.GetName() if cur else None)