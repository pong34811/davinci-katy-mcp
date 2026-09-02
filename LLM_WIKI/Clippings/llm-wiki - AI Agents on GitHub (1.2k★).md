---
title: "llm-wiki - AI Agents on GitHub (1.2k★)"
source: "https://skillsllm.com/skill/llm-wiki"
author:
  - "[[SkillsLLM]]"
published:
created: 2026-09-02
description: "LLM-compiled knowledge bases for any AI agent. Parallel multi-agent research, thesis-driven investigation, source ingestion, wiki compilation, querying, and..."
tags:
  - "clippings"
---
## llm-wiki

Verified

LLM-compiled knowledge bases for any AI agent. Parallel multi-agent research, thesis-driven investigation, source ingestion, wiki compilation, querying, and artifact generation.

1,176stars

111forks

Python

Added 4/7/2026

⚠️ Third-Party Software Notice

This skill is third-party open-source software developed and hosted independently on GitHub. SkillsLLM is an informational directory and does not control or maintain the underlying repository.

Any security checks, ratings, or warnings displayed by SkillsLLM are automated and limited in scope. They do not constitute a security certification or guarantee that the software is safe, error-free, or free from malicious code, vulnerabilities, compromised dependencies, or prompt-injection risks.

Review the source code, permissions, dependencies, and configuration before installing or running any third-party skill. Use is at your own risk. To the maximum extent permitted by applicable law, SkillsLLM is not liable for losses arising from third-party software.

[Read the Terms of Service](https://skillsllm.com/terms)

[AI Agents](https://skillsllm.com/category/ai-agents) agentic-aiagentic-skillsagentic-workflowclaude-codecodexllmpluginwiki

```
# Add to your Claude Code skills
git clone https://github.com/nvk/llm-wiki
```

Getting Started

Guides for using ai agents skills like llm-wiki.

- [
	Caveman: Cut Claude Token Use by 65%
	How agent-side prompt compression works, when to use it, and when not to.
	](https://skillsllm.com/blog/caveman-token-compression-claude-code)
- [
	What is an AI Skills Marketplace?
	Definitions, how marketplaces work, and how to choose between them in 2026.
	](https://skillsllm.com/blog/what-is-ai-skills-marketplace)
- [
	Getting Started with AI Skills
	First-time install walkthrough for Claude Code, Codex CLI, and ChatGPT.
	](https://skillsllm.com/blog/getting-started-with-ai-skills)

Last scanned: 5/20/2026

```
{
  "issues": [],
  "status": "PASSED",
  "scannedAt": "2026-05-20T07:42:37.067Z",
  "semgrepRan": false,
  "npmAuditRan": true,
  "pipAuditRan": true
}
```

README.md

```
██╗     ██╗     ███╗   ███╗    ██╗    ██╗██╗██╗  ██╗██╗
██║     ██║     ████╗ ████║    ██║    ██║██║██║ ██╔╝██║
██║     ██║     ██╔████╔██║    ██║ █╗ ██║██║█████╔╝ ██║
██║     ██║     ██║╚██╔╝██║    ██║███╗██║██║██╔═██╗ ██║
███████╗███████╗██║ ╚═╝ ██║    ╚███╔███╔╝██║██║  ██╗██║
╚══════╝╚══════╝╚═╝     ╚═╝     ╚══╝╚══╝ ╚═╝╚═╝  ╚═╝╚═╝
```

[llm-wiki.net](https://llm-wiki.net/) · [@LLMWIKI on X](https://x.com/LLMWIKI) · [github.com/nvk/llm-wiki](https://github.com/nvk/llm-wiki)

LLM-compiled knowledge bases for any AI agent. Capture rough Ideas, research and shape them, then explicitly promote approved briefs into delivery Projects. Also includes parallel research, collector catalogs, session memory, source ingestion, compilation, audits, querying, and artifact generation. Ships for Claude Code, OpenAI Codex, OpenCode, and portable agents. Obsidian-compatible.

---

[Install](#install) · [Quick Start](#quick-start) · [Sessions](#session-memory) · [Commands](#commands) · [How It Works](#how-it-works) · [Research Modes](#research-modes) · [Thesis Research](#thesis-driven-research) · [Query Depths](#query-depths) · [Linking](#linking-works-everywhere) · [Obsidian](#obsidian-integration) · [Architecture](#claude-first-multi-runtime) · [Nono Sandbox](#nono-sandbox-permissions) · [Upgrade](#upgrade) · [Changelog](#changelog) · [Credits](#credits)

---

## Changelog

**v0.24.0** — **Project Knowledge Checkpoints Export.** Exports comprehensive, cross-topic project handoffs under `docs/knowledge/<slug>/` with dry-run-first create and refresh, read-only verification and bounded import, exact source and section coverage, explicit omissions, semantic privacy minimization, deterministic sealing, attested overrides, and a thin-output guard. Checkpoint writes never authorize commit, publication, or import.

**v0.23.0** — **Personal specialist framework.** Adds optional user-owned, instruction-only `SKILL.md` review methods under the user's local wiki hub, explicit per-topic allowlists, deterministic validation and management, and research selection with version/hash provenance. The public release contains the framework only; personal specialist packages and wiki-derived candidate reports are not bundled or published.

**v0.22.0** — **Declarative private-adapter routing.** Registered adapters may declare provider-neutral intent and exact-URL routes plus an adapter-owned workflow guide. The public plugin discovers the route before ingestion but no longer embeds any provider's authentication, browser, recovery, or editing workflow.

**v0.21.3** — **Adapter-boundary transition.** Consolidates the v0.21 line and keeps the session-hook compatibility fix. Provider-specific workflow material from that line is superseded in current source by manifest-driven routing and lives only in the corresponding private adapter.

**v0.20.0** — **Governed remote writes.** Extends private adapters with exact remote-resource allowlists, declared read/write effects, explicit approval bound to an exact plan hash, expected revisions, stable idempotency keys, private verified receipts, and content-free terminal reporting.

**v0.19.0** — **Private adapter protocol.** Adds an explicitly trusted, machine-local adapter registry and portable `llm-wiki-adapter/v1` JSON contract, with manifest handshakes, path scopes, sanitized environments, hash-verified artifacts, bundled management CLI, and an explicit workflow boundary that never passes a wiki destination or auto-promotes adapter output.

**v0.18.0** — **Hub-wide portfolio.** Adds `/wiki:portfolio`, a live read-only view across active topic wikis that lists canonical Ideas and active Projects separately, distinguishes explicitly promoted Projects from direct ones, preserves Concepts as supporting knowledge, and avoids catch-all topics, duplicated records, inferred lineage, and stale portfolio caches.

## Install

**Claude Code** (native plugin):

```bash
claude plugin install wiki@llm-wiki
```

**OpenAI Codex** (marketplace plugin):

Install from GitHub:

```bash
codex plugin marketplace add nvk/llm-wiki
codex plugin add wiki@llm-wiki
# Start a new Codex thread, then use @wiki or type $ to select wiki-query
```

Install from a local checkout with the managed bootstrap helper:

```bash
./scripts/bootstrap-codex-plugin.sh --scope user --verify
```

Or register the local checkout manually:

```bash
codex plugin marketplace add /absolute/path/to/llm-wiki
codex plugin add wiki@llm-wiki
```

Canonical explicit invocation:

```
$wiki-query "What does the wiki say about hardware wallet threat models?"
@wiki research "hardware wallet threat models"
@wiki collect "bitcoin memes" --wiki memes-bitcoin
@wiki ingest https://example.com/article
@wiki audit --project coldcard-threat-model
@wiki session status
@wiki feedback list --unpromoted
@wiki session disable   # optional opt-out
@wiki ll "codex plugin install gotchas"
```

Upgrade:

```bash
codex plugin marketplace upgrade llm-wiki
codex plugin add wiki@llm-wiki
```

Remove:

```bash
codex plugin remove wiki@llm-wiki
codex plugin marketplace remove llm-wiki
```

Troubleshooting:

- `codex plugin marketplace add` registers the catalog; `codex plugin add wiki@llm-wiki` installs and enables the cached plugin non-interactively.
- Open `/hooks` to review and trust the bundled hooks if you want automated session capture. The `@wiki` skill works without hook trust.
- `$wiki-query` is the small, explicit, read-only skill for lookups. In Codex CLI/IDE, type `$` or open `/skills` and select it. It never activates implicitly or changes wiki files.
- `@wiki` is the full research and maintenance entry point. Natural-language wiki requests can still auto-activate it.
- Restart Codex after changing config if an existing session does not pick up the new plugin state.
- If you run Codex under a sandbox wrapper like `nono`, see [Nono Sandbox Permissions](#nono-sandbox-permissions) — Codex needs r+w to `$HOME/.codex` for plugin install.

**OpenCode** (instruction file):

Add to your `opencode.json` (project-level or `~/.config/opencode/.opencode.json` for global):

```json
{
  "instructions": ["https://raw.githubusercontent.com/nvk/llm-wiki/master/plugins/llm-wiki-opencode/skills/wiki-manager/SKILL.md"],
  "permission": {
    "external_directory": {
      "~/.config/llm-wiki/**": "allow",
      "~/Library/Mobile Documents/com~apple~CloudDocs/wiki/**": "allow"
    }
  }
}
```

OpenCode fetches the URL fresh on every session start — no manual updates needed. If you prefer a local copy instead:

```bash
curl -sL https://raw.githubusercontent.com/nvk/llm-wiki/master/plugins/llm-wiki-opencode/skills/wiki-manager/SKILL.md > ~/.config/opencode/AGENTS.md
```

For a smaller read-only setup, use the best-effort query preset instead:

```json
{
  "instructions": ["https://raw.githubusercontent.com/nvk/llm-wiki/master/plugins/llm-wiki-opencode/skills/wiki-query/SKILL.md"]
}
```

The OpenCode profile is sync- and budget-tested, but not tied to one model, so it does not have a provider-specific live quality gate. Treat it as a portable best-effort preset and keep OpenCode's write and shell permissions disabled for query-only sessions.

The `external_directory` permission is required because the wiki hub lives outside the project directory. Set the paths to match your hub location. Alternatively, use `--local` mode (`.wiki/` in the project) to skip permissions entirely.

Web search requires `export OPENCODE_ENABLE_EXA=1`.

**Pi** (skill file, best for local models):

Pi's minimal system prompt leaves room for on-demand wiki workflows on local models. Load the full skill for research and write-capable maintenance:

```bash
pi --skill path/to/llm-wiki/plugins/llm-wiki-opencode/skills/wiki-manager/SKILL.md
```

Invoke it as `/skill:wiki-manager`, or let Pi load it when the request clearly matches its description.

For fast read-only queries with Pi's currently configured provider, use the generic launcher. It disables discovery and write tools and loads the compact shared query protocol:

```bash
./scripts/pi-wiki-query
```

For DS4, the provider-specific launcher additionally creates an isolated Pi state directory and pins the local model settings:

```bash
./scripts/pi-ds4-wiki-query
```

Set `PI_CLI`, `DS4_BASE_URL`, or `LLM_WIKI_PI_DS4_STATE_DIR` only when your local setup differs from the defaults. Both launchers accept `--dry-run` to show the exact command. The equivalent generic Pi settings are:

```bash
pi \
  --append-system-prompt path/to/llm-wiki/profiles/query-lite/SKILL.md \
  --tools read,grep,find,ls \
  --no-extensions --no-skills --no-prompt-templates --no-themes
```

The DS4 query profile is intentionally unable to write. Switch to the full skill for ingest, research, compile, lint, or other mutating workflows. See [`profiles/ds4/README.md`](https://skillsllm.com/skill/profiles/ds4/README.md) and the reproducible [`benchmarks/README.md`](https://skillsllm.com/skill/benchmarks/README.md) DS4 lane.

**Any LLM Agent** (portable instruction file):

```bash
# Read-only queries: small default
cp profiles/query-lite/SKILL.md ~/your-project/AGENTS.md

# Research and maintenance: complete protocol
cp AGENTS.md ~/your-project/AGENTS.md
```

The query-lite profile works with agents that can read and search files. The root `AGENTS.md` contains the complete write-capable protocol for agents that can also edit files and search the web.

## Claude-First, Multi-Runtime

Claude Code is the principal user. Keep one shared behavior layer and thin packaging layers per runtime:

- `claude-plugin/` is the primary distribution target and UX surface.
- `claude-plugin/skills/wiki-manager/` is the behavioral source of truth.
- `plugins/llm-wiki/skills/wiki/` is the generated Codex packaging target behind `@wiki`.
- `claude-plugin/skills/wiki-manager/references/query-lite.md` is the canonical read-only query protocol.
- `profiles/query-lite/SKILL.md` and generated `wiki-query` skills expose that protocol without the full research context.
- `plugins/llm-wiki-opencode/`

## Frequently Asked Questions

### What is llm-wiki?

llm-wiki is an open-source ai agents skill for AI coding assistants such as Claude Code, Codex CLI, and ChatGPT, built by nvk. LLM-compiled knowledge bases for any AI agent. Parallel multi-agent research, thesis-driven investigation, source ingestion, wiki compilation, querying, and artifact generation. It has 1,176 GitHub stars.

### Is llm-wiki safe to use?

Yes. llm-wiki passed SkillsLLM's automated security scan — a dependency vulnerability audit plus prompt-injection heuristics — with no high-severity issues. You can read the full report in the Security Report section on this page.

### How do I install llm-wiki?

Clone the repository with "git clone https://github.com/nvk/llm-wiki" and add it to your Claude Code skills directory (see the Installation section above).

### What programming language is llm-wiki written in?

llm-wiki is primarily written in Python. It is open-source under nvk on GitHub, so you can review or fork the full source.

### Are there alternatives to llm-wiki?

Yes. SkillsLLM lists many other AI Agents skills you can browse and compare side by side. Open the AI Agents category from the badge at the top of this page, or use the Related Skills and comparison links further down to weigh llm-wiki against similar tools.

[Agentic AI for Beginners](https://skillsllm.com/courses/agentic-ai-beginner)

[Build your first AI agent from scratch - tool use, ReAct pattern, memory, deployment](https://skillsllm.com/courses/agentic-ai-beginner)

[

41 minBeginner

](https://skillsllm.com/courses/agentic-ai-beginner)

Comments (0)

to leave a comment.

No comments yet. Be the first to share your thoughts!

## Related Skills

[ECC](https://skillsllm.com/skill/ecc)

by [affaan-m](https://github.com/affaan-m)

The agent harness performance optimization system. Skills, instincts, memory, security, and research-first development for Claude Code, Codex, Opencode, Cursor and beyond.

245,895

37,105

JavaScript

AI Agentsai-agentsanthropic

[View details](https://skillsllm.com/skill/ecc)

[Compare](https://skillsllm.com/compare/ecc-vs-llm-wiki)

[superpowers](https://skillsllm.com/skill/superpowers)

by [obra](https://github.com/obra)

An agentic skills framework & software development methodology that works.

234,966

20,863

Shell

AI Agentsaibrainstorming

[View details](https://skillsllm.com/skill/superpowers)

[Compare](https://skillsllm.com/compare/llm-wiki-vs-superpowers)

[everything-claude-code](https://skillsllm.com/skill/everything-claude-code)

by [affaan-m](https://github.com/affaan-m)

The agent harness performance optimization system. Skills, instincts, memory, security, and research-first development for Claude Code, Codex, Opencode, Cursor and beyond.

185,940

28,768

JavaScript

AI Agentsai-agentsanthropic

[View details](https://skillsllm.com/skill/everything-claude-code)

[Compare](https://skillsllm.com/compare/everything-claude-code-vs-llm-wiki)

[cc-switch](https://skillsllm.com/skill/cc-switch)

by [farion1231](https://github.com/farion1231)

A cross-platform desktop All-in-One assistant for Claude Code, Codex, OpenCode, OpenClaw, Grok Build & Hermes Agent. Only official website: ccswitch.io

130,638

8,975

Rust

AI Agentsai-toolsclaude-code

[View details](https://skillsllm.com/skill/cc-switch)

[Compare](https://skillsllm.com/compare/cc-switch-vs-llm-wiki)

An AI skill that provides design intelligence for building professional UI/UX across multiple platforms.

123,987

13,268

Python

CLI Toolsai-skillsantigravity

[View details](https://skillsllm.com/skill/ui-ux-pro-max-skill)

[Compare](https://skillsllm.com/compare/llm-wiki-vs-ui-ux-pro-max-skill)