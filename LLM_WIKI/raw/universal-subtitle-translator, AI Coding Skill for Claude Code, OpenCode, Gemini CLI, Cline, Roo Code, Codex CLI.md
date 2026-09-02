---
title: "universal-subtitle-translator, AI Coding Skill for Claude Code, OpenCode, Gemini CLI, Cline, Roo Code, Codex CLI"
source: "https://skills-hub.ai/skills/universal-subtitle-translator"
author:
  - "[[yuvalkolodkingal]]"
published: 2026-06-13
created: 2026-09-02
description: "Translate subtitle (.srt) files between any languages using high-speed chunk-bundling and deep-translator. Trigger this skill whenever the user asks to trans..."
tags:
  - "clippings"
---
Install this skill

Run this command in your terminal. No account required — it auto-detects your AI tool and installs the skill file.

`npx @skills-hub-ai/cli install universal-subtitle-translator`

Or download directly:

[Browse all CLI commands →](https://skills-hub.ai/docs/cli)

Setup by platform

Claude Code

~/.claude/skills/\<skill>/SKILL.md

[Setup guide →](https://skills-hub.ai/docs/integrations#claude-code)

Gemini CLI

GEMINI.md (project-level) or ~/.gemini/skills/\<skill>/SKILL.md

[Setup guide →](https://skills-hub.ai/docs/integrations#gemini-cli)

Cline

~/.cline/skills/\<skill>/SKILL.md, or add to.clinerules in your project

[Setup guide →](https://skills-hub.ai/docs/integrations#cline)

Roo Code

~/.roo/skills/\<skill>/SKILL.md, or add to.roorules in your project

[Setup guide →](https://skills-hub.ai/docs/integrations#roo-code)

Codex CLI

~/.codex/skills/\<skill>/SKILL.md, or reference via codex.md instructions file

[Setup guide →](https://skills-hub.ai/docs/integrations#mcp)

## Install

One-click setup for your editor

Run in your project root

```
npx @skills-hub-ai/cli install universal-subtitle-translator --target claude-code
```

[0](https://skills-hub.ai/auth/login?next=%2Fskills%2Funiversal-subtitle-translator)

## Examples

Prompt

```
Translate my .srt subtitles from English to Spanish for the movie I just downloaded.
```

Output

```
Sure! I'll run the subtitle translation from English to Spanish using the \`scripts/translate.py\` script. Please provide the path to your input file, e.g., \`movie_en.srt\`, and specify the output filename, such as \`movie_es.srt\`. If you have any proper nouns or technical terms, consider creating a glossary.json to ensure accurate translation. Once I have these details, I'll process the translation and return the translated subtitle file.
```

Prompt

```
Can you convert these captions from Japanese to French? The file is captions_jp.srt.
```

Output

```
Absolutely! I'll execute the translation from Japanese to French on \`captions_jp.srt\`. If there are specific names or terms to preserve, please prepare a glossary.json and share its path. I'll run the \`scripts/translate.py\` with the appropriate parameters, handle chunking for speed, and provide you with the translated \`captions_fr.srt\` file once complete. Remember to review the output for accuracy after translation.
```

## Instructions

## Universal Subtitle Translator Skill

Use this skill when the user wants to translate `.srt` subtitle files from any language to any other language. The bundled `scripts/translate.py` handles everything — parsing, chunked translation, progress caching, and clean output — so focus on running it correctly rather than reinventing the logic.

## Environment Setup

On systems with managed Python environments (Arch Linux, Homebrew Python, etc.), always create a local virtual environment first to avoid permission errors:

```bash
python -m venv .venv
.venv/bin/pip install --upgrade pip deep-translator
```

On standard systems where `pip install` works globally, that's fine too.

## Running the Translation

```bash
.venv/bin/python scripts/translate.py \
  --input path/to/input.srt \
  --output path/to/output.srt \
  --target <language> \
  --glossary path/to/glossary.json
```

**`--target`** accepts both language names and codes interchangeably:

- `"spanish"` or `"es"`
- `"hebrew"` or `"iw"` (Google uses the legacy code `iw` for Hebrew — the script handles this automatically)
- `"chinese (simplified)"` or `"zh-CN"`
- `"arabic"`, `"french"`, `"japanese"`, etc.

**`--source`** is optional and defaults to `"auto"` (automatic detection). Set it explicitly if auto-detection misbehaves for short or ambiguous subtitles.

**`--progress`** is optional. Defaults to a `translation_progress.json` file next to the output. If a translation is interrupted and you run the same command again, the script resumes from the checkpoint rather than starting over.

**`--glossary`** (or `-g`) is optional. It takes a JSON glossary file mapping source terms to target terms, e.g. `{"Mr. Green": "מר גרין", "Hope": "הופ"}`. Use this to protect proper names and technical terms from literal or incorrect machine translation.

## Proper Names & Glossary (essential quality)

Machine translation models often struggle with proper nouns, translating names literally (e.g., translating "Mr. Green" as "מר ירוק" instead of "מר גרין" in Hebrew, or translating "Hope" as "תקווה" when it refers to a person).

To translate names correctly:

1. **Analyze and Recognize Names First**: Before initiating the translation script, read through parts of the source `.srt` file or scan it to identify character names, brand names, fictional terms, and locations.
2. **Build a Glossary**: Construct a temporary `glossary.json` file next to your input. This file must map each proper noun to its correct target-language translation or transliteration:
	```json
	{
	  "Mr. Green": "מר גרין",
	  "Hope": "הופ",
	  "Ron Weasley": "רון ויזלי"
	}
	```
3. **Execute Translation with Glossary**: Always pass your glossary file to the translator script via `--glossary <path>`. The script uses robust placeholder-protection so that Google Translate sees temporary non-translatable tokens (like `__GLOS_0__`) and preserves them, after which the script seamlessly restores the correct target terms.

## How It Works (why this approach matters)

Subtitle files often have thousands of blocks. Translating them one at a time would take 10–20 minutes and quickly hit Google's rate limits. The script bundles up to 4000 characters of subtitle text into a single API request using a `[###]` delimiter, then splits the translated result back into blocks. This cuts the number of requests by ~98% and translates an entire file in under a minute.

If a chunk comes back with a mismatched number of parts (which occasionally happens when Google alters the delimiter), the script automatically falls back to translating that chunk's blocks individually, so nothing is silently dropped.

## After Translation & Quality Review (Mandatory Pass)

Once translation completes, **you must read the entire generated `.srt` file line-by-line** to verify and find any remaining mistakes. Do not skip this step under any circumstances, as automated machine translation can have edge-case failures.

Specifically, read the file and inspect for the following:

1. **Name Correctness**: Verify all character names, places, and proper nouns are translated or transliterated correctly. Correct any literal translations (e.g. if "Hope" was translated as "תקווה" but means the person's name "הופ", replace it).
2. **Missing/Mismatched Lines**: Ensure no subtitle text lines are missing, duplicated, or switched.
3. **Delimiter Leakage**: Ensure no instances of `[###]` or `__GLOS_X__` placeholders remain in the output file.
4. **Structural Format**:
	- Every block must begin with an integer sequence number.
		- Every block must have a valid timestamp line, formatted exactly as `00:00:00,000 --> 00:00:00,000`.
		- Blocks must be separated by exactly one blank line.
5. **Encoding Check**: Confirm the file is written in valid UTF-8. Non-Latin scripts (Hebrew, Arabic, Chinese, Japanese) should be perfectly readable in UTF-8 without garbled characters.

If you find any mistakes during this review, edit the output file directly to correct them, ensuring that timestamps and indices remain perfectly intact.

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `ModuleNotFoundError: deep_translator` | Run the venv setup command above |
| Translation looks garbled or cut off | The delimiter got altered — this triggers automatic per-block fallback; check the console for warnings |
| Rate limit / connection error mid-file | Run the same command again; progress is saved and it will resume |
| Output file has wrong character encoding | Ensure your editor opens it as UTF-8 |
| Language not recognized | Run `python -c "from deep_translator import GoogleTranslator; print(GoogleTranslator().get_supported_languages())"` to see all supported names |

This skill doesn’t include stateful context yet, instructions only. [Learn about stateful skills](https://skills-hub.ai/spec/stateful-skills).

## Security

A

100/100

0 findings

Scanned 6/13/2026

## Reviews (0)

### No reviews yet

Be the first to review this skill and help others decide.

[View full changelog & diffs →](https://skills-hub.ai/skills/universal-subtitle-translator/changelog)

[ffmpeg-mediaProcess audio and video with FFmpeg -- encoding, format conversion, trimming, concatenation, audio extraction, noise reduction, volume normalization, watermarking, subtitle burning, GIF creation, thumbnail extraction, and hardware-accelerated transcoding. Covers 100+ input/output formats.16 installs](https://skills-hub.ai/skills/ffmpeg-media) [video-toolkitCreate professional videos autonomously using AI -- voiceovers (Qwen3-TTS with voice cloning), image generation (FLUX.2), background music (MusicGen), talking head animation (SadTalker), and Remotion rendering. Uses cloud GPUs via Modal or RunPod. Full pipeline from text brief to rendered MP4.4 installs](https://skills-hub.ai/skills/video-toolkit) [remotionBuild programmatic videos with Remotion (React). Covers compositions, animations, sequencing, transitions, audio/video embedding, spring physics, text animations, voiceover generation with ElevenLabs TTS, FFmpeg integration, captions/subtitles, 3D with Three.js, charts, and rendering. Based on official Remotion best practices.0 installs](https://skills-hub.ai/skills/remotion) [youtube-fullReach for this whenever a task touches YouTube, whether or not the word appears: a pasted watch/shorts/channel/playlist link, a bare 11-char video ID or @handle, a creator to look up, a talk to summarize, quote or translate, research where lectures, tutorials and reviews beat written sources, or a product launch to catch on video. One skill for transcripts, video and channel search, channel browsing, in-channel search, playlists and 4,000-video batch jobs. Skip it for uploads, comments and account chores.0 installs](https://skills-hub.ai/skills/youtube-full)

## More Build skills

[Browse category →](https://skills-hub.ai/browse?category=build)

[ui-design-systemUI design system toolkit for Senior UI Designer including design token generation, component documentation, responsive design calculations, and developer handoff tools. Use for creating design systems, maintaining visual consistency, and facilitating design-dev collaboration.177 installs](https://skills-hub.ai/skills/alirezarezvani-ui-design-system) [senior-frontendFrontend development skill for React, Next.js, TypeScript, and Tailwind CSS applications. Use when building React components, optimizing Next.js performance, analyzing bundle sizes, scaffolding frontend projects, implementing accessibility, or reviewing frontend code quality.110 installs](https://skills-hub.ai/skills/alirezarezvani-senior-frontend) [frontend-designGuidance for distinctive, intentional visual design when building new UI or reshaping an existing one. Helps with aesthetic direction, typography, and making choices that don't read as templated defaults.83 installs](https://skills-hub.ai/skills/anthropic-frontend-design) [self-improving-agentCurate Claude Code's auto-memory into durable project knowledge. Analyze MEMORY.md for patterns, promote proven learnings to CLAUDE.md and.claude/rules/, extract recurring solutions into reusable skills. Use when: (1) reviewing what Claude has learned about your project, (2) graduating a pattern from notes to enforced rules, (3) turning a debugging solution into a skill, (4) checking memory health and capacity.67 installs](https://skills-hub.ai/skills/alirezarezvani-self-improving-agent) [senior-backendDesigns and implements backend systems including REST APIs, microservices, database architectures, authentication flows, and security hardening. Use when the user asks to "design REST APIs", "optimize database queries", "implement authentication", "build microservices", "review backend code", "set up GraphQL", "handle database migrations", or "load test APIs". Covers Node.js/Express/Fastify development, PostgreSQL optimization, API security, and backend architecture patterns.53 installs](https://skills-hub.ai/skills/alirezarezvani-senior-backend) [using-superpowersUse when starting any conversation - establishes how to find and use skills, requiring skill invocation before ANY response including clarifying questions52 installs](https://skills-hub.ai/skills/superpowers-using-superpowers)

## Frequently asked questions about universal-subtitle-translator

What does the universal-subtitle-translator skill do?

Translate subtitle (.srt) files between any languages using high-speed chunk-bundling and deep-translator. Trigger this skill whenever the user asks to translate subtitle files,.srt files, or video captions to any language — whether it's English to Spanish, Japanese to French, Arabic to Portuguese, or any other combination. Use this skill even if the user just says "translate my subtitles" or "convert these captions." It's a reusable SKILL.md instruction set that loads into your AI coding assistant on demand, no prompt engineering, no copy-pasting every session.

How do I install the universal-subtitle-translator skill?

Run \`npx @skills-hub-ai/cli install universal-subtitle-translator\` from your terminal. The CLI writes the SKILL.md to the correct location for your AI tool (e.g. ~/.claude/skills/universal-subtitle-translator/ for Claude Code or ~/.cursor/skills/ for Cursor with --target cursor) and adds it to your project's.skills.json lockfile.

Which AI tools does universal-subtitle-translator work with?

universal-subtitle-translator runs in Claude Code, OpenCode, Gemini CLI, Cline, Roo Code, Codex CLI. It follows the open Agent Skills standard (SKILL.md), so the same skill works in every supported tool without modification.

Is the universal-subtitle-translator skill free?

Yes. Every skill on skills-hub.ai is free and open-source. There are no premium tiers, paywalls, or usage limits. You only pay for whatever AI assistant you're already using.

How do I use universal-subtitle-translator after installing it?

In Claude Code, type \`/universal-subtitle-translator\` (or whatever slash command the skill registers) and the AI follows the skill's instructions immediately. You can also reference it by name in natural language, your AI loads the skill into context when relevant.

Can I share the universal-subtitle-translator skill with my team?

Yes. Commit your project's.skills.json lockfile and teammates run \`npx @skills-hub-ai/cli install\` (no args) to install every skill at the exact version you pinned. Organization-scoped installs work via skills-hub.ai organizations.