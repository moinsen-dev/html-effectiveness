---
name: html-report
description: Render status reports, incident reports, postmortems, weekly engineering updates, retro summaries, and quarterly reviews as a self-contained HTML artifact in ./artifacts/ instead of a markdown wall. Triggers on "weekly status", "engineering update", "team report", "status report", "incident report", "postmortem", "retro", "what shipped this week", "RCA", "outage summary", "monthly review", or any request that asks for a periodic or post-event roll-up of work + metrics + risks.
---

# html-report — periodic + post-event roll-ups as HTML

## When this fires

A report asks: "what happened, what does it mean, what's next" against a
specific timeframe or event. Status updates, weekly engineering reports,
quarterly reviews, incident postmortems, outage timelines, retro summaries.
If the user says "make me a status report" or "write up the incident", you
are here.

If the user actually wants to *understand* a system (not roll up activity),
hand off to `html-research`. If they want a slide presentation of the same
data, hand off to `html-deck`.

## Style templates

Read these first to absorb the layout, palette, and component vocabulary:

- `../../examples/11-status-report.html` — Acme weekly status. Header strip
  with week-of date and team meta. Metric tiles. "What shipped" list with
  PR-style rows. "Risks" panel with severity dots. Subtle sparkline-SVG.
- `../../examples/12-incident-report.html` — incident timeline. Severity
  banner. Chronological timeline with timestamps. "What broke / what
  helped / what we'll change" three-column block.

## Output convention

Follow `../_shared/output-conventions.md` exactly. Slug examples:
`acme-week-19-status`, `auth-outage-2026-05-12-rca`, `q1-retro`.

## Style tokens

Use `../_shared/style-tokens.md`. Reports especially need: mono eyebrows
for dates/IDs, olive for "shipped / resolved", rust for "broke / blocked",
clay for the primary accent (titles, key numbers).

## What to include

- **Header strip**: project/team name, period (week of, quarter, incident
  ID + start time), one-line summary.
- **Metric tiles** (3-5): the numbers that matter for *this* report. PRs
  merged, deploys, incidents, MTTR, etc. Each tile: big number, label,
  optional ↑↓ vs previous period.
- **Narrative body**: 2-4 sections. For weekly status: Shipped / In flight
  / Risks / Next. For incident: Timeline / Root cause / Customer impact /
  Action items with owners.
- **Inline data**: small SVG sparkline or bar — no chart libraries.
- **Footer**: who wrote it (the user or "Claude Code"), one-line link back
  to the source (PR list, dashboard URL).

## Anti-patterns

- No long markdown-style bullet lists. Use cards, tiles, two-column rows.
- No "TL;DR" — the metric tiles ARE the TL;DR.
- No external chart libraries. Inline SVG only.
- Do not invent metrics. If the user did not supply numbers, ask once or
  use clearly-labelled `--` placeholders.
