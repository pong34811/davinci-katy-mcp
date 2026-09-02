
import os
import sys
import argparse
import subprocess

# --- Environment setup from .hermes.md ---
REPO_ROOT = r"C:\Users\warit\Desktop\davinci-katy-mcp"
MCP_DIR = os.path.join(REPO_ROOT, "davinci-resolve-mcp")

RESOLVE_LIB = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
RESOLVE_MODULES = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules"

# Add RESOLVE_MODULES to sys.path first (for current process)
if RESOLVE_MODULES not in sys.path:
    sys.path.insert(0, RESOLVE_MODULES)

# Add REPO_ROOT and MCP_DIR to sys.path (for current process)
for _p in (REPO_ROOT, MCP_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# Set environment variables for subprocess
env = os.environ.copy()
if os.path.isfile(RESOLVE_LIB):
    _d = os.path.dirname(RESOLVE_LIB)
    if not env.get("PYTHONHOME"):
        env["PYTHONHOME"] = sys.base_prefix
    env["PATH"] = _d + os.pathsep + env.get("PATH", "")
    # os.add_dll_directory only affects the current process, not subprocesses through env var
    if hasattr(os, "add_dll_directory"):
        try:
            os.add_dll_directory(_d)
        except OSError:
            pass
# --- End of Environment setup ---

# Now try to run sfx_place.py using subprocess
try:
    sfx_place_script = os.path.join(REPO_ROOT, "scripts", "sfx_place.py")
    
    # Construct the command to run sfx_place.py
    command = [
        sys.executable, # Use the same python interpreter
        sfx_place_script,
        "--plan", os.path.join(REPO_ROOT, "scripts", "plan.json"),
    ]

    # Add additional arguments if provided to run_sfx_place.py
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--sfx-dir", default=os.path.join(REPO_ROOT, "SFX"))
    parser.add_argument("--track-name", default="SFX 1")
    
    # Parse arguments for this wrapper script
    wrapper_args, unknown = parser.parse_known_args(sys.argv[1:])

    if wrapper_args.dry_run:
        command.append("--dry-run")
    if wrapper_args.verify:
        command.append("--verify")
    
    command.extend(["--sfx-dir", wrapper_args.sfx_dir])
    command.extend(["--track-name", wrapper_args.track_name])

    # Pass sys.path elements to the subprocess as PYTHONPATH for module discovery
    # This is crucial for the subprocess to find modules like 'config' and 'davinci_resolve_mcp.src.utils.platform'
    if 'PYTHONPATH' in env:
        env['PYTHONPATH'] = os.pathsep.join(sys.path) + os.pathsep + env['PYTHONPATH']
    else:
        env['PYTHONPATH'] = os.pathsep.join(sys.path)

    print(f"DEBUG: Command: {' '.join(command)}")
    print(f"DEBUG: PYTHONPATH for subprocess: {env.get('PYTHONPATH')}")
    print(f"DEBUG: PATH for subprocess: {env.get('PATH')}")
    print(f"DEBUG: PYTHONHOME for subprocess: {env.get('PYTHONHOME')}")
    
    # Run sfx_place.py as a subprocess
    result = subprocess.run(command, capture_output=True, text=True, env=env, cwd=REPO_ROOT)

    print(result.stdout)
    if result.stderr:
        print("--- STDERR ---")
        print(result.stderr)
    
    sys.exit(result.returncode)

except Exception as e:
    print(f"ERROR: An unexpected error occurred in wrapper: {e}")
    sys.exit(1)
