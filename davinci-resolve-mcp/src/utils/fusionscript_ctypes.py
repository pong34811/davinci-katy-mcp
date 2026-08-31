#!/usr/bin/env python3
"""Direct ctypes bridge to fusionscript.dll for DaVinci Resolve API.

This bypasses the broken DaVinciResolveScript.py import path by loading
fusionscript.dll directly via ctypes and wrapping the C API in Python.
"""

from __future__ import annotations

import ctypes
import os
import sys
from ctypes import c_char_p, c_int, c_void_p
from typing import Any, Optional


def _resolve_dir() -> str:
    return os.environ.get("RESOLVE_DIR", r"C:\Program Files\Blackmagic Design\DaVinci Resolve")


def _api_dir() -> str:
    return os.environ.get(
        "RESOLVE_SCRIPT_API",
        os.path.join(os.environ.get("PROGRAMDATA", r"C:\ProgramData"),
                     "Blackmagic Design", "DaVinci Resolve", "Support", "Developer", "Scripting"),
    )


def _load_fusionscript() -> ctypes.CDLL:
    resolve_dir = _resolve_dir()
    dll_path = os.path.join(resolve_dir, "fusionscript.dll")
    if not os.path.isfile(dll_path):
        raise FileNotFoundError(f"fusionscript.dll not found: {dll_path}")
    # Ensure the DLL's directory is in the DLL search path on Windows
    if hasattr(os, "add_dll_directory"):
        os.add_dll_directory(resolve_dir)
    return ctypes.CDLL(dll_path)


def _make_app_name(name: str) -> bytes:
    return name.encode("utf-8") + b"\0"


def _voidp_to_obj(ptr: int) -> Any:
    """Wrap an opaque C pointer in a minimal callable proxy."""
    if not ptr:
        return None

    class ResolveObject:
        def __init__(self, handle: int):
            self._h = handle

        def __getattr__(self, name: str):
            def _method(*args, **kwargs):
                raise NotImplementedError(
                    f"ctypes bridge: method '{name}' needs a typed wrapper"
                )
            return _method

        def __repr__(self):
            return f"<ResolveObject 0x{self._h:x}>"

    return ResolveObject(ptr)


def scriptapp(dll: ctypes.CDLL, app_name: str, host: str = "", timeout: float = 5.0) -> Any:
    """Call scriptapp via ctypes."""
    # Probe the actual signature by trying a few calling conventions.
    # Resolve's fusionscript.dll exports a C API; on Windows it's usually
    # `int scriptapp(const char* app_name, const char* host, void** out_resolve)`.
    # We attempt cdecl first; if that segfaults we cannot recover here.
    try:
        fn = dll.scriptapp
    except AttributeError as exc:
        raise ImportError("fusionscript.dll does not export 'scriptapp'") from exc

    fn.restype = c_int
    out = c_void_p()
    app_buf = _make_app_name(app_name)
    host_buf = _make_app_name(host) if host else c_char_p(None)

    rc = fn(app_buf, host_buf, ctypes.byref(out))
    if rc != 0 or not out.value:
        return None
    return _voidp_to_obj(out.value)


def main() -> int:
    print("Loading fusionscript.dll via ctypes...")
    dll = _load_fusionscript()
    print(f"Loaded: {dll._name}")

    print("Calling scriptapp('Resolve')...")
    resolve = scriptapp(dll, "Resolve")
    print("Resolve handle:", resolve)
    return 0


if __name__ == "__main__":
    sys.exit(main())
