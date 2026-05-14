---
name: html-editor
description: Render bespoke internal-tool UIs — triage boards, feature-flag editors, prompt tuners, config dashboards, queue inspectors — as a self-contained interactive HTML artifact in ./artifacts/ instead of a markdown spec. Triggers on "triage board", "feature flag editor", "prompt tuner", "internal tool", "admin UI", "custom editor", "config editor for", "build me a UI to manage", "give me a dashboard for", "let me edit X visually", or any request to build a small tailored editor surface around some data the user supplied.
---

# html-editor — custom internal-tool UIs as HTML

## When this fires

The user has a *thing they want to edit or triage* — a list of tickets,
a set of feature flags, prompt variants, a config blob — and asks for a
UI tailored to that data shape. Off-the-shelf admin panels are generic;
a hand-cut HTML editor that matches the user's exact data is the point.

If the user wants a *spec* of the UI without interactivity, hand off to
`html-design`. If they want a *prototype* showing one interaction in
isolation, hand off to `html-prototype`.

## Style templates

- `../../examples/18-editor-triage-board.html` — ticket triage board.
  Multi-column kanban (incoming / in review / blocked / done). Cards are
  inline-editable; drag-to-move; keyboard-driven. Filter bar at top.
- `../../examples/19-editor-feature-flags.html` — feature flag editor.
  Table view: flag name, scope, current state, last-changed, owner.
  Inline toggle + value-edit. Diff view between staged and live.
- `../../examples/20-editor-prompt-tuner.html` — prompt-iteration UI.
  Prompt editor left, sample inputs middle, generated-output preview
  right. Save-as-version button creates a history list.

## Output convention

Follow `../_shared/output-conventions.md`. Slug examples:
`triage-board`, `feature-flag-editor`, `prompt-tuner-v1`.

If the user supplied a JSON/CSV blob (flags, tickets, prompt variants),
embed it as a `<script type="application/json">` block inside the
artifact so the editor opens populated.

## Style tokens

Use `../_shared/style-tokens.md`. Editors should feel calm — `--ivory`
canvas, `--paper` panels, `--g300` borders. Reserve clay for primary
actions only; olive for "saved / live"; rust for "error / blocked".

## What to include

- **Header strip**: tool name, one-line purpose, save/export buttons,
  unsaved-changes indicator.
- **Filter / search bar** (when data is a list): real `<input>` with
  live filter via inline JS.
- **Main work area**: kanban columns, or table, or split-pane —
  whatever fits the data. Inline-editable cells/cards.
- **Detail pane** (when there is one selected item): right rail or
  modal, full edit form.
- **History / diff** (when the data is mutable): list of recent
  changes, optional revert button. Local only — no backend.
- **Persistence**: write all state to `localStorage` on change; read
  on load. The user must be able to close the tab and come back to
  the same state.
- **Export**: button that dumps current state as JSON (or CSV) for
  copy-paste back into the source of truth.

## Anti-patterns

- No React / Vue / Svelte. Vanilla JS — `<script type="module">` is fine.
- No backend calls. Everything happens in the page; `localStorage` is
  the store; "save" means export.
- Do not over-feature. If the user asked for a flag editor with 3
  flags, ship 3 flags and the minimum to manage them.
- Do not lock data inside the UI. Always provide a JSON export.
- No login screens, no auth flows. This is a local single-user tool.
