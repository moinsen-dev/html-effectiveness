---
name: html-research
description: Render explainers, deep-dives, concept explainers, feature walkthroughs, "how does X work" answers, and research summaries as a self-contained HTML artifact in ./artifacts/ instead of a markdown wall. Triggers on "explain how X works", "deep dive on", "concept explainer", "feature explainer", "research summary", "ELI5 but real", "walk me through the internals of", "how does X actually work", "investigate and explain", "study notes on", or any request for an article-style explanation with diagrams + examples + references.
---

# html-research — explainers + deep-dives as HTML

## When this fires

The user wants to *understand* something — a feature, a protocol, a
concept, a library's internals. The answer is article-length, mixes prose
with diagrams and code samples, and benefits from a real reading layout
(not a terminal scroll).

If the answer is mostly diagram, hand off to `html-illustration`. If the
goal is to *present* the explanation, hand off to `html-deck`. If the
user wants a roll-up of activity, hand off to `html-report`.

## Style templates

- `../../examples/14-research-feature-explainer.html` — feature deep
  dive. Hero with eyebrow, headline, summary. Table of contents in a
  side rail. Sections mix prose, inline SVG, code blocks. Footnotes/
  references at the bottom.
- `../../examples/15-research-concept-explainer.html` — concept
  explainer. Same shape but more analogies-and-diagrams, less
  code-and-API. Definition card at the top with the term + one-line gloss.

## Output convention

Follow `../_shared/output-conventions.md`. Slug examples:
`http2-server-push-explainer`, `vector-search-concept`,
`feature-X-deep-dive`.

## Style tokens

Use `../_shared/style-tokens.md`. Research artifacts especially: serif
headlines, sans body, plenty of vertical rhythm, max-width ≈ 720px for
the main column even though the page goes wider (the side rail TOC sits
outside).

## What to include

- **Hero**: eyebrow (topic class), serif headline, 2-3 sentence summary,
  reading-time estimate.
- **Side rail TOC**: sticky on wide viewports, hidden on narrow.
- **Body sections**: each one self-contained — intro paragraph, then
  diagram or code or callout. 3-6 sections total.
- **Code blocks**: inline mono, language label in eyebrow style, no
  syntax highlighting beyond colour for keywords/strings.
- **Inline SVG diagrams** where a picture helps more than a paragraph.
- **Callouts / asides**: paper background, clay border-left, mono
  eyebrow ("Note", "Caveat", "Why it matters").
- **References / further reading**: numbered list at the bottom, real
  URLs only if the user asked for citations.

## Clipboard relay — making the artefact actionable

Use the shared pattern (see `../_shared/clipboard-relay.md`) to let
the reader expand any sub-topic on demand.

For html-research:
- **Where buttons go**: end of each body section ("Go deeper"
  affordance); optional duplicates on each TOC entry.
- **`data-action`**: `Go deeper on "<concept>" from the research`.
- **`data-payload`**: the section's one-line claim.
- **`data-followup`**: `Show one concrete example with code.` for
  technical sections; `Walk me through a worked example.` otherwise.
- **Primary highlight**: rare — only if one section is explicitly
  flagged as "start here."

Hero summary, callouts and references are not action points.

## Anti-patterns

- Do not flatten into a single wall of paragraphs. Use the section
  vocabulary above.
- Do not invent citations. If you do not have a source, do not pretend
  to.
- No iframes, no embedded YouTube. Inline SVG and code only.
- Do not waste the hero on filler ("In this article we will…"). Open
  with the punchline.
