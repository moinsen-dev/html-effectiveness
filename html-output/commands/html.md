---
description: Force the next answer into an HTML artifact. Pick the best archetype from the html-output skills based on the user's request and write a self-contained .html file to ./artifacts/.
argument-hint: "<what you want rendered as HTML>"
---

# /html — force HTML output

The user has explicitly asked for an HTML artifact. Even if no auto-trigger
in the `html-*` skills would have fired, produce an HTML file now.

## Step 1 — Classify

Read `$ARGUMENTS` (everything after `/html`) and pick the single best
archetype from the table below. If genuinely ambiguous, ask one short
clarifying question; otherwise commit.

| If the request smells like… | Use the archetype from |
|---|---|
| "what shipped", "weekly", "incident", "postmortem", "RCA", "retro" | `skills/html-report/SKILL.md` |
| "explain how X works", "deep dive", "research", "ELI5 but real" | `skills/html-research/SKILL.md` |
| "design system", "tokens", "variants", "style guide" | `skills/html-design/SKILL.md` |
| "review this PR", "annotate diff", "module map", "explain this code" | `skills/html-code-review/SKILL.md` |
| "diagram", "flowchart", "architecture sketch", "illustrate" | `skills/html-illustration/SKILL.md` |
| "deck", "slides", "present this", "pitch" | `skills/html-deck/SKILL.md` |
| "animation sandbox", "clickable flow", "prototype", "micro-interaction" | `skills/html-prototype/SKILL.md` |
| "triage board", "flag editor", "prompt tuner", "internal tool", "admin UI" | `skills/html-editor/SKILL.md` |
| "three approaches", "compare options", "implementation plan" | `skills/html-exploration/SKILL.md` |

If the user pinned an archetype explicitly (`/html as a deck:`,
`/html report:`, `/html prototype:`), honour that.

## Step 2 — Execute

Open the matched skill file and follow it. The output convention is the
same for every skill:

1. Read the style templates listed in that skill.
2. Compose a single self-contained `.html` file.
3. Write to `./artifacts/<slug>-<YYYYMMDD-HHMMSS>.html` (mkdir -p).
4. Open it: `open` on macOS, `xdg-open` on Linux, otherwise print the path.
5. Reply in chat with one line: the file path. Do **not** repeat the
   content as markdown.

## Step 3 — If the previous turn already produced content

If the previous assistant turn produced a long markdown answer and the
user now types `/html` (often `/html make that an HTML` or just `/html`),
treat that *previous answer* as the source material. Pick the archetype
that fits the content of the previous answer, then re-render it as HTML.

The chat reply notes: "Re-rendered the previous answer as
`./artifacts/<file>.html`."

## Anti-patterns

- Do not produce both markdown and HTML. The whole point is to replace
  the markdown answer.
- Do not invent content the user did not ask for to "fill" the artifact.
  Render exactly what was requested at the granularity that was
  requested.
- Do not skip the `open` step. The feedback loop is the value.
