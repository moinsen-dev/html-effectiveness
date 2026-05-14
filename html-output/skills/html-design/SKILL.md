---
name: html-design
description: Render design systems, component variant sheets, style guides, design-token specifications, and brand pages as a self-contained HTML artifact in ./artifacts/ instead of a markdown spec. Triggers on "design system", "style guide", "component variants", "design tokens", "brand spec", "UI kit", "component library spec", "show me variants of", "spec out the button", "design palette + typography", or any request that asks for a visual specification of UI primitives.
---

# html-design — design systems + component variants as HTML

## When this fires

The user wants to *see* UI primitives, not read about them. Design-token
tables, button variant sheets, color palettes with usage notes, typography
ramps, spacing scales. Output is a single living spec the user can keep
open while building.

If the user wants a working interactive prototype (not just a spec), hand
off to `html-prototype`. If they want a slide-deck-style brand intro, hand
off to `html-deck`.

## Style templates

- `../../examples/05-design-system.html` — full design system. Color
  swatches with hex + role. Typography ramp with sample text. Spacing
  scale visualised. Button/input/card primitives rendered in all states.
- `../../examples/06-component-variants.html` — one component, many
  variants. Grid of cards each showing one state (default, hover, focus,
  disabled, danger). Each card labelled with its props/state.

## Output convention

Follow `../_shared/output-conventions.md`. Slug examples:
`acme-design-system-v1`, `button-variants`, `brand-palette`.

## Style tokens

Use `../_shared/style-tokens.md` *unless the user is specifying their own
brand* — in that case adopt their tokens but keep the layout discipline.

## What to include (design-system flavour)

- **Foreword**: 2-3 sentence intent ("This is the spec for X. Use these
  tokens. Components below are live HTML, copy-paste-able.").
- **Color**: swatch grid with hex, RGB, role ("primary action",
  "destructive"), and an `aria-friendly` contrast note.
- **Type**: full ramp (display → caption) with sample text, font-family,
  size, weight, line-height.
- **Spacing & radius**: visual scale (bars or boxes), token names.
- **Primitives**: at least button, input, card, table-row, badge. Each in
  default + 2-3 states.

## What to include (component-variants flavour)

- **Header**: component name, one-line role, link/anchor back to the
  design system.
- **Variant grid**: 6-12 cards. Each card = one variant, rendered live,
  with: state label, props as monospace, accessibility note (e.g., "disabled
  uses aria-disabled, not disabled, to remain focusable").
- **Composition examples**: 1-2 small layouts showing the component in
  context.

## Anti-patterns

- Do not embed Figma screenshots or external images. Render the components
  in actual HTML/CSS.
- Do not use a CSS framework. Bare CSS. The whole point is the spec is
  also the implementation reference.
- Do not invent design tokens beyond what the user described. If the user
  gave you 3 colors, do not extrapolate to 30.
- No `lorem ipsum`. Use realistic copy that matches the product domain.
