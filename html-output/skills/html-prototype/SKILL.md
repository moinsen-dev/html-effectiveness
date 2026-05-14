---
name: html-prototype
description: Render interactive prototypes — animation sandboxes, clickable flows, micro-interactions, hover/transition demos — as a self-contained HTML artifact in ./artifacts/ instead of describing them in markdown. Triggers on "prototype", "clickable demo", "animation sandbox", "interactive demo", "tweak this animation", "micro-interaction", "show me the easing", "make a hover demo", "click through this flow", "spring animation", "transition prototype", or any request to *see* a UI behaviour rather than read about it.
---

# html-prototype — interactive prototypes as HTML

## When this fires

The user wants to *feel* an interaction: an animation curve, a hover
state, a multi-step click-through, a transition. Static specs do not
answer "does this feel right" — a runnable prototype does.

If the user wants a *spec* of the same UI without interactivity, hand off
to `html-design`. If they want a presentation, hand off to `html-deck`.

## Style templates

- `../../examples/07-prototype-animation.html` — animation sandbox.
  Sliders for duration / easing / delay / amplitude. Preview area shows
  the animation looping. Inline CSS keyframes visible (and editable in
  the harder version).
- `../../examples/08-prototype-interaction.html` — clickable flow.
  Multi-screen, prev/next + jump-to-step. Each screen is a real HTML
  state, not an image. URL hash reflects the current step.

## Output convention

Follow `../_shared/output-conventions.md`. Slug examples:
`toggle-spring-anim`, `signup-click-flow`, `card-hover-states`.

## Style tokens

Use `../_shared/style-tokens.md`. Prototypes can use slightly more colour
saturation than reports — the artifact's purpose is to be looked at.

## What to include (animation sandbox)

- **Stage**: large preview area, neutral background, the animated element
  centred.
- **Controls panel**: real `<input type=range>` / `<select>` for the knobs
  (duration, easing, delta, repeat). Changes apply live via inline JS.
- **Spec readout**: the current values rendered as CSS the user can copy
  (animation-duration, cubic-bezier, etc.).
- **Reset button**.

## What to include (clickable flow)

- **Step indicator**: dots or numbered tabs at top, current step
  highlighted.
- **Prev / Next**: keyboard arrows AND on-screen buttons.
- **State per step**: real HTML, not images. URL hash (`#step-2`) reflects
  position so the user can deep-link.
- **Notes lane** (optional): for each step, a short caption explaining
  what the screen is meant to demonstrate.

## Clipboard relay — making the artefact actionable

Use the shared pattern (see `../_shared/clipboard-relay.md`) to let the
reader lock in a configuration and continue with production code.

For html-prototype:
- **Where buttons go (animation sandbox)**: alongside the spec readout —
  "Adopt this configuration." Optional: one button per preset row.
- **Where buttons go (clickable flow)**: one per step plus a single
  "Use this whole flow" at the end.
- **`data-action`**: `Adopt the "<config>" configuration from the prototype`
  (animation) or `Implement step <N> "<screen>" from the prototype`
  (flow).
- **`data-payload`**: the current CSS values (animation) or the step's
  one-line goal (flow).
- **`data-followup`**: `Write production-ready CSS/JSX.`
- **Primary highlight**: `class="primary"` on the user's last-tuned
  state's adopt button.

Sliders, prev/next and the stage preview are core interactions — the
relay button sits *alongside* them, never on top.

## Anti-patterns

- No animation libraries (GSAP, Framer Motion). Vanilla CSS + a few lines
  of inline JS only.
- No video embeds. The artifact must be the animation, not a recording of
  it.
- Do not autoplay sound, ever.
- Do not require a build step or a server. `open file://…` must work.
