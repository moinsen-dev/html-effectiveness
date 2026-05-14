---
name: html-code-review
description: Render code reviews, PR walkthroughs, annotated diffs, module maps, codebase explainers, and "what does this code do" answers as a self-contained HTML artifact in ./artifacts/ instead of a markdown wall. Triggers on "review this PR", "annotate this diff", "PR writeup", "explain this codebase", "module map", "code walkthrough", "what does X do", "trace this function", "review #1234", "code review", "diff annotation", "architecture overview of this repo", or any request to make a piece of code legible to a human reader.
---

# html-code-review — code review + codebase explanation as HTML

## When this fires

The user wants a piece of code (a PR, a module, a function, a whole repo)
explained or critiqued. Two flavours collapse here:

1. **Review-mode**: there is a diff or a PR. Annotate it. Surface risks,
   suggest changes, group comments.
2. **Map-mode**: there is a codebase or a feature spanning files. Draw the
   shape — entry points, modules, data flow, hot paths.

If the user wants to *plan* code that does not exist yet, hand off to
`html-exploration` or `html-research`.

## Style templates

- `../../examples/03-code-review-pr.html` — annotated PR view. File tree
  on the left, diff hunks on the right with inline review comments.
  Severity-tagged comments (nit / suggestion / blocker).
- `../../examples/17-pr-writeup.html` — author-side PR description.
  "Why / what changed / how to verify / risk" structure. Inline before/
  after snippets.
- `../../examples/04-code-understanding.html` — module map. Boxes for
  modules, arrows for dependencies, hot files highlighted, one-line
  descriptions per box.

## Output convention

Follow `../_shared/output-conventions.md`. Slug examples:
`auth-refactor-pr-review`, `feature-flag-module-map`,
`pr-1234-writeup`.

## Style tokens

Use `../_shared/style-tokens.md`. Code review needs:
- `--mono` for all diff content and file paths.
- `--g100` background for code hunks; red/green tints only on the changed
  lines — keep them subtle (≈10% saturation), not GitHub-loud.
- Severity dots: olive (nit), clay (suggestion), rust (blocker).

## What to include (review-mode)

- Header: PR title, branch, author, lines +/-, status badge.
- File-tree sidebar (or top strip on narrow viewports).
- Diff hunks with line numbers; each comment anchored to a line, with
  severity dot and one-paragraph rationale.
- "Summary" panel at the top: 3 bullets — overall verdict, biggest risk,
  recommended next step.

## What to include (map-mode)

- Header: feature/repo name, scope ("auth", "the whole repo").
- Module boxes laid out in a small SVG/flex grid; arrows for "imports /
  calls". Hot modules (high fan-in or recently changed) marked.
- For each module: one-line role, 2-3 key files, entry-point function.
- Optional "data flow" strip showing request → handler → store → response.

## Anti-patterns

- Do not paste 500-line diffs verbatim. Show the meaningful hunks; collapse
  the rest with line-count summaries.
- No markdown tables for the file tree — render it as a real nested list
  with file-type icons (use inline SVG or unicode).
- Do not invent issues. If you cannot read the code, say so in the summary
  panel rather than fabricating review comments.
- No syntax highlighting via JS libraries. Static CSS classes per token
  type, or none at all.
