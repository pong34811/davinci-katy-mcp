---
title: "lordhoell/davinci-resolve-mcp: MCP server + Claude Code skill exposing the complete DaVinci Resolve scripting API (440+ tools)"
source: "https://github.com/lordhoell/davinci-resolve-mcp"
author:
  - "[[lordhoell]]"
published:
created: 2026-09-02
description: "MCP server + Claude Code skill exposing the complete DaVinci Resolve scripting API (440+ tools) for AI-assisted video editing, color grading, and rendering."
tags:
  - "clippings"
  - "video-editing"
  - "davinci-resolve"
  - "mcp-server"
---

# lordhoell/davinci-resolve-mcp: MCP server + Claude Code skill (440+ tools)

> Alternative MCP server for DaVinci Resolve, exposing 440+ tools via the `fusionscript.dll` bridge.

## Overview

An [MCP](https://modelcontextprotocol.io/) server and Claude Code skill that expose the **complete** DaVinci Resolve scripting API — letting any MCP-compatible AI assistant control DaVinci Resolve programmatically.

```
AI Assistant  <-->  MCP Protocol  <-->  This Server  <-->  fusionscript  <-->  DaVinci Resolve
```

## Tool Categories

| Category | Tools | Examples |
| --- | --- | --- |
| Project Management | 25 | Create/load/export projects, manage databases, cloud projects |
| Timeline Editing | 59 | Add/remove tracks, insert titles & generators, manage markers |
| Media Pool | 27 | Import media, create timelines from clips, organize folders |
| Clip Operations | 80 | Set clip properties, manage Fusion comps, color versions, CDL, stabilize |
| Color Grading | 16 | Node graph control, LUT management, grade application |
| Rendering | 15 | Configure render settings, formats/codecs, add render jobs |

See the [GitHub repo](https://github.com/lordhoell/davinci-resolve-mcp) for the full tool list and setup instructions.

## See also

- [[samuelgursky davinci-resolve-mcp MCP server|Primary]] — the main open-source MCP server (36 compound / 353 granular tools)
- [[I Gave Claude Direct Access to DaVinci Resolve|Article]] — Python-bridged chat interface experiment
- [[Higgsfield Plugins for DaVinci Resolve|Alternative]] — AI plugins running natively inside Resolve

---
*Consolidated: 2026-09-02*