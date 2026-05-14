---
name: html-deck
description: Render slide decks, talk-style presentations, internal pitches, and "walk me through this in N slides" requests as a self-contained HTML artifact in ./artifacts/ instead of markdown bullets. Triggers on "slide deck", "presentation", "present this", "N slides on X", "talk slides", "internal pitch", "make a deck", "keynote-style", "all-hands deck", "lightning talk", "kickoff deck", or any request that explicitly asks for slides + arrow-key navigation.
---

# html-deck — arrow-key slide decks as HTML

## When this fires

The user wants to *walk through* a story in discrete frames with keyboard
navigation. Internal pitches, all-hands updates, kickoff decks, lightning
talks. The HTML deck loads instantly, works offline, exports to PDF via
print, and never asks for a Google login.

If the user wants a long-form article, hand off to `html-research`. If
they want a one-page summary that scrolls, hand off to `html-report`.

## Style templates

- `../../examples/09-slide-deck.html` — arrow-key deck. One slide
  full-viewport at a time, deck progress at the bottom, ←/→ to navigate,
  `s` for speaker notes, `g` to jump. Clean serif title slides, sans body
  slides, clay accent.

## Output convention

Follow `../_shared/output-conventions.md`. Slug examples:
`q2-kickoff-deck`, `auth-refactor-pitch`, `5min-lightning`.

## Style tokens

Use `../_shared/style-tokens.md`. Slide type is **bigger** than report
type — title at 56-80px, body at 20-28px. Generous whitespace; one idea
per slide.

## What to include

- **Title slide**: deck title, presenter, date, one-line subtitle.
- **5-12 content slides** (default 7 unless user specified): one
  headline + 1-3 supporting points OR one image/diagram OR one chart.
  Never paragraphs of body text.
- **Section dividers**: optional, full-bleed colour, just the section
  name in serif.
- **Closing slide**: "What's next" / "Discuss" / "Thank you" + contact.
- **Speaker notes**: hidden by default, toggleable with `s`. Each slide
  has a `<aside class="notes">` block with what to actually say.
- **Navigation**: ←/→ or PgUp/PgDn, `Home`/`End`, `s` for notes,
  `Esc` for overview grid (optional, nice).
- **Progress indicator**: subtle bar or `n / N` at the bottom corner.

## Anti-patterns

- Do not put paragraphs on slides. If you have a paragraph, it's a
  document, not a deck — hand off to `html-research`.
- No reveal.js, Spectacle, Marp, or other deck frameworks. Vanilla CSS +
  ~30 lines of JS for navigation.
- No autoplay anything. No transitions longer than 150ms.
- Do not number slides in the body title (no "Slide 3:"). The progress
  indicator handles that.
