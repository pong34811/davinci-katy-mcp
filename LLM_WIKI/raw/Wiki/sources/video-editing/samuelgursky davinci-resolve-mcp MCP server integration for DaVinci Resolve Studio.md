---
title: "samuelgursky/davinci-resolve-mcp: MCP server integration for DaVinci Resolve Studio"
source: "https://github.com/samuelgursky/davinci-resolve-mcp"
author:
  - "[[Samuel Gursky]]"
published: 2025-03-21
created: 2026-09-02
description: "MCP server integration for DaVinci Resolve Studio. Full API coverage plus guarded workflow helpers for editing, media pool, render, grading, Fusion, Fairlight, and source-safe media analysis."
tags:
  - "clippings"
  - "video-editing"
  - "davinci-resolve"
  - "mcp-server"
---

# samuelgursky/davinci-resolve-mcp: MCP server integration for DaVinci Resolve Studio

> Primary source for the `davinci-resolve-mcp` project — the open-source MCP server that connects AI assistants to DaVinci Resolve via the official Python Scripting API.

## Overview

A Model Context Protocol (MCP) server that lets AI assistants control DaVinci Resolve Studio through the official Scripting API. It provides full API coverage plus guarded workflow helpers for editing, media pool organization, render setup, review markers, grading, Fusion, Fairlight, project lifecycle tasks, extension authoring, and source-safe media analysis.

[![Local control panel](https://raw.githubusercontent.com/samuelgursky/davinci-resolve-mcp/main/docs/images/control-panel/01-overview.png)](https://github.com/samuelgursky/davinci-resolve-mcp/blob/main/docs/guides/control-panel.md)

A local browser control panel ships with the server for inspecting Resolve state, running source-safe analysis, drilling into analyzed clips and shots, and editing analysis output inline.

## Quick Start

```
npx davinci-resolve-mcp setup
```

Before connecting, open DaVinci Resolve Studio and set **Preferences > General > External scripting using** to **Local**. On the free edition, use the in-app bridge instead.

The npm launcher installs a managed copy under your user application-data directory, then runs the universal Python installer. It creates a virtual environment, detects Resolve paths, and can configure Claude Desktop, Claude Code, Cursor, VS Code, Windsurf, Zed, Continue, Cline, Roo Code, OpenCode, Codex CLI, and JetBrains IDEs.

## Free edition (in-app bridge)

Blackmagic gates external scripting to Studio — `scriptapp("Resolve")` refuses a foreign process on the free edition. The **Workspace ▸ Scripts** menu is not gated, so the server can reach the free edition through a small script that runs *inside* Resolve and re-exports it over an authenticated loopback listener.

```
python scripts/install_resolve_bridge.py
# restart Resolve, open a project, then: Workspace > Scripts > resolve_bridge
```

The bridge holds its port for as long as it serves. Loopback only, HMAC-signed requests, one-use nonces.

## Server Modes

| Mode | Entry point | Tools | Best for |
| --- | --- | --- | --- |
| Compound | `src/server.py` | 36 | Default mode — related operations grouped behind action parameters |
| Full / granular | `src/server.py --full` | 353 | Power users — one MCP tool per Resolve API method |

The compound server is recommended unless you specifically need the granular one-tool-per-method surface.

## Advanced server — beyond the scripting API (optional, Node)

The same package ships **`davinci-resolve-advanced-mcp`** (bin `bin/davinci-resolve-advanced-mcp.mjs`). Where the Python server drives a *live* Resolve over the sanctioned scripting API, the advanced server reads and edits Resolve **files** (.drp / .drt / .drx) with no Resolve running — so it runs cloud *or* local. 18 tools: `drp`, `drt`, `drx` (per-clip grade codec plus offline grading/QC catalog), `offline_ref`, `conform`, `color_trace`, `fusion`, `audio_plan`, `fairlight` (bus routing), `audio`, `project_read`, `project_db`, `pipeline`, `capabilities`, `deliverable`, `media`, `editorial`, `provenance`.

## Key Stats

| Metric | Value |
| --- | --- |
| MCP Tools | **36** compound / **353** granular (live server) |
| Advanced (offline) tools | **18** |
| API Methods Covered | **361/361** (100%) |
| Live Test Pass Rate | **338/338** (100%) |
| Tested Against | Resolve 19.1.3 Studio + Resolve 20.3.2 + Resolve 21.0.2 + Resolve 21.0.3 free (via bridge) |

## What This Does Not Do

- **Choosing the best take** — `rank_takes` ranks fluency, not quality
- **Cutting to music** — no beat or downbeat detection yet
- **Judging a cut** — every destructive action is plan → review → confirm
- **Replacing an editor** — first-pass assembly, not a finished cut
- **Modifying your source media** — source media is immutable

## Source Media Safety

This project treats camera originals and source media as immutable. Analysis tools read source files and write reports only to sidecar, scratch, or project analysis directories.

## Security Posture

The default server is a local stdio process launched by your MCP client. It does not expose a network listener or built-in multi-user auth surface. The control panel and networked MCP transport bind loopback only with per-launch bearer tokens.

## See also

- [[samuelgursky davinci-resolve-mcp MCP server integration for DaVinci Resolve Studio|Source]] — this file (primary)
- [[Automate Your Video Workflow A Deep Dive into the DaVinci Resolve MCP Server|Article]] — skywork.ai overview by a creative producer
- [[I Gave Claude Direct Access to DaVinci Resolve|Article]] — wildlion.media article on building a Python-bridged chat interface
- [[lordhoell davinci-resolve-mcp MCP server|Alternative]] — alternative MCP server with 440+ tools using fusionscript.dll
- [[Higgsfield Plugins for DaVinci Resolve|Alternative]] — AI plugins running natively inside Resolve
- [[MCP Server Plugin|Alternative]] — lobehub MCP server for Resolve
- [[DaVinci Resolve MCP (viaSocket)|Alternative]] — viaSocket MCP server for Resolve

## Consolidated from

This summary consolidates the following near-duplicate clippings into a single authoritative source:
- `DaVinci Resolve MCP Server for Claude Code & Claude Desktop.md` (mdskills.ai — same repo, same content as README)
- `Automate Your Video Workflow A Deep Dive into the DaVinci Resolve MCP Server.md` (skywork.ai — secondary article)
- `DaVinci Resolve MCP Server - Integrating AI Assistant and Editing Tool Functions via MCP Protocol.md` (mcp.aibase.com — analysis)
- `daVinci Resolve MCP Server.md` (samuelgursky.com — short stub)

---
*Consolidated: 2026-09-02*