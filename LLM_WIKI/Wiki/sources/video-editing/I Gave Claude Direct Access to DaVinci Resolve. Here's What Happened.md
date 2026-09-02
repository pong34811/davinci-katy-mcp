---
type: source-summary
source: raw/Wiki/sources/video-editing/I Gave Claude Direct Access to DaVinci Resolve. Here's What Happened.md
date_ingested: 2026-09-02
tags: [wiki, wiki/source, davinci-resolve, claude-code, python-api, video-editing]
---

# Source: I Gave Claude Direct Access to DaVinci Resolve

Experiment by Poul Waligora (Head of Post-Production at ACN International, runs Wild Lion Media) connecting Claude directly to a live DaVinci Resolve project via Python scripting.

## Key Facts

- **Author:** Poul Waligora
- **Published:** 2026-04-04
- **Source:** [wildlion.media/claude-davinci-resolve/](https://wildlion.media/claude-davinci-resolve/)
- **Architecture:** Python scripting API (`DaVinciResolveScript`) wrapped in ~35 tools, passed to Claude via Anthropic's tool-use framework
- **Model:** Claude Sonnet 4.5
- **Tool Set:** Project/timeline operations, clip operations, markers, media pool, render queue, gallery
- **API Ceiling:** Color nodes off-limits, Fusion inaccessible, Fairlight not exposed, no playback control

## Key Insight

The main point is not Resolve — it's terminal access. Claude connected to your PC through Terminal/PowerShell gives you a level of control over your workstation that used to belong to IT professionals. Resolve is one application inside that system; the terminal is the larger story.

## Related

- [[samuelgursky davinci-resolve-mcp MCP server|Primary MCP server]]
- [[lordhoell davinci-resolve-mcp MCP server|Alternative MCP server]]
- [[Higgsfield Plugins for DaVinci Resolve|AI plugins]]
- [[DaVinci Resolve Audio Workflow A Practical Guide to Pro Sound|Audio workflow]]

---
*Created: 2026-09-02*