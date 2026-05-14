---
name: html-illustration
description: Render diagrams, flowcharts, SVG figure sheets, system illustrations, request-lifecycle drawings, and architecture sketches as a self-contained HTML artifact in ./artifacts/ instead of an ASCII diagram or markdown list. Triggers on "diagram this", "flowchart", "illustrate", "draw the architecture", "request lifecycle", "system diagram", "SVG figure", "explain this with a picture", "show me the flow", "data flow diagram", "sequence diagram", or any request to make a system visible rather than narrated.
---

# html-illustration — flowcharts + SVG figures as HTML

## When this fires

The user asks to *see* a system, flow, or relationship. ASCII art breaks
on resize, markdown lists hide the structure, screenshots go stale —
inline SVG inside a single HTML file does not.

If the user wants a richer narrative around the diagram, hand off to
`html-research`. If they want the diagram as one slide in a deck, hand off
to `html-deck` (and embed the SVG there).

## Style templates

- `../../examples/10-svg-illustrations.html` — figure sheet. Multiple
  SVGs on one page, each captioned. Consistent stroke weight, palette,
  arrow style. The artifact reads as a textbook plate.
- `../../examples/13-flowchart-diagram.html` — annotated flowchart with
  branches, decision diamonds, side-notes explaining each step.
  Hand-drawn feel via slightly irregular stroke + rounded corners.

## Output convention

Follow `../_shared/output-conventions.md`. Slug examples:
`request-lifecycle-diagram`, `auth-flow`, `retry-state-machine`.

## Style tokens

Use `../_shared/style-tokens.md`. Diagrams especially: stick to
slate/clay/olive/rust strokes; oat + g100 fills; mono labels.
Stroke width 1.5-2px. Arrows: small triangle marker, never giant.

## What to include

- **Title strip**: name of the diagram, one-line caption.
- **Diagram canvas**: inline `<svg>` with explicit `viewBox`. Boxes/
  diamonds/lozenges as the shape vocabulary. Labels in `--mono` or
  small `--sans`.
- **Legend**: shape vocabulary (rectangle = process, diamond = decision,
  cylinder = store) plus colour roles (clay = primary path, rust = error
  path, olive = success).
- **Side annotations**: short numbered notes calling out specific edges
  or boxes. Connect by number, not by arrows-on-arrows.

## Anti-patterns

- Do not use Mermaid, PlantUML, Graphviz, or any rendering library. Hand-
  authored inline SVG only — it's more honest about layout choices and
  trivially editable.
- No raster images. No screenshots of whiteboards.
- Do not draw more boxes than fit comfortably in 1120px width. If the
  system is too big, split into two diagrams or pick a level of
  abstraction.
- Do not let arrows cross unless absolutely necessary; route around.
