# html-output

A Claude Code plugin that routes Claude's answers into **self-contained HTML
artifacts** instead of markdown walls — for the kinds of work where a real
document beats a terminal scroll.

Companion to *The unreasonable effectiveness of HTML* (live demos at
[thariqs.github.io/html-effectiveness](https://thariqs.github.io/html-effectiveness/)).

## What it does

When you ask Claude Code for any of the work below, instead of dumping
markdown into your terminal, it writes a `.html` file to `./artifacts/` and
opens it in your browser.

| Skill | Triggers on | Style templates |
|---|---|---|
| `html-report` | weekly status, incident report, postmortem, retro | 11, 12 |
| `html-research` | "explain how X works", deep-dive, concept explainer | 14, 15 |
| `html-code-review` | review a PR, annotate diff, module map | 03, 04, 17 |
| `html-design` | design system, component variants, style guide | 05, 06 |
| `html-prototype` | animation sandbox, clickable flow, micro-interaction | 07, 08 |
| `html-illustration` | flowchart, diagram, SVG figure | 10, 13 |
| `html-deck` | slide deck, presentation, pitch | 09 |
| `html-editor` | triage board, feature-flag editor, prompt tuner | 18, 19, 20 |
| `html-exploration` | three approaches, implementation plan, options | 01, 02, 16 |

Plus one slash command:

- `/html <freeform>` — force HTML output even when no auto-trigger fired.

## Install

```bash
# inside Claude Code
/plugin marketplace add github:thariqs/html-effectiveness
/plugin install html-output@html-effectiveness
```

For local development:

```bash
/plugin marketplace add /absolute/path/to/html-effectiveness
/plugin install html-output@html-effectiveness
```

## Use

Just ask. The skills auto-trigger:

> "Write me a weekly status report for the Acme engineering team — we
> shipped auth-v2, the payments retry refactor, and started on the new
> billing UI."

→ `./artifacts/acme-weekly-status-20260514-160233.html` opens in your
browser.

For forced HTML output:

> `/html three approaches for rate-limiting our public API`

## How artifacts are produced

Every skill follows the same recipe (see
`skills/_shared/output-conventions.md`):

1. Read the matching style template(s) from `examples/` to absorb palette,
   layout, and component vocabulary.
2. Compose a single self-contained `.html` (inline CSS, inline SVG, no
   CDNs, no external assets).
3. Write to `./artifacts/<slug>-<YYYYMMDD-HHMMSS>.html` in your current
   working directory.
4. Open it (`open` on macOS, `xdg-open` on Linux).
5. Reply in chat with one line — the file path — never repeating the
   content as markdown.

## Customizing the look

The default look is the warm-paper Anthropic palette shared by all 20
demos (`skills/_shared/style-tokens.md`). If you want a different one for
your team, two options:

- **Per-request**: tell Claude "use our brand colors: …".
- **Permanent**: fork the plugin, edit `style-tokens.md`, and reinstall
  from your fork.

## Why it works

LLMs are excellent at writing single-file HTML and CSS. The terminal is a
bad rendering surface for status reports, design specs, and slide decks.
Pointing the model at a small folder of opinionated style templates plus a
fixed write-and-open recipe gives you, every time:

- Documents that look the same across requests.
- Real interactivity for prototypes and editors.
- A `.html` file you can commit, share via Slack, or print to PDF.

The output is not Claude's *answer* anymore — it is an *artifact*.

## License

MIT (matches the upstream repo).
