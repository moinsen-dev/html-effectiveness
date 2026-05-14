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

## Clipboard relay — making the artefact actionable

The clipboard-relay pattern (see `../_shared/clipboard-relay.md`) is
how editor state hands off to the codebase. The editor is a step-2
surface by definition — every change the user makes is meant to go
somewhere real.

For html-editor:
- **Where buttons go**: in the header strip alongside Export-JSON — a
  single `Apply state to the codebase` button. No per-row buttons; the
  whole editor state is one decision.
- **`data-action`**: `Apply this editor state to the codebase`.
- **`data-payload`**: a compact serialisation of the *live* editor
  state, built at click time (not at HTML generation). Override the
  inline script for this skill: replace
  `var payload = btn.dataset.payload || '';` with
  `var payload = JSON.stringify(getCurrentState());`
  where `getCurrentState()` reads the live state from `localStorage`
  or in-page state.
- **`data-followup`**: `Update the source of truth — write code, open a
  PR, or run the migration.`
- **Primary highlight**: `class="primary"` — it's the artefact's one
  important action.

The existing "Export JSON" button stays; the relay button is *added*,
not a replacement. This is the one archetype where the artefact's
*state itself* becomes the prompt payload — not a one-line summary.

## Anti-patterns

- No React / Vue / Svelte. Vanilla JS — `<script type="module">` is fine.
- No backend calls except the clipboard write described above. Everything
  else happens in the page; `localStorage` is the store; "save" means
  export.
- Do not over-feature. If the user asked for a flag editor with 3
  flags, ship 3 flags and the minimum to manage them.
- Do not lock data inside the UI. Always provide a JSON export.
- No login screens, no auth flows. This is a local single-user tool.
