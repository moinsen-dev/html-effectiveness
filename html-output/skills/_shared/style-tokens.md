# Style tokens (shared by all html-* skills)

All 20 example HTMLs share one design language. Use it. Deviating produces
artifacts that look like generic LLM output; staying in it makes the whole
plugin feel like a single product.

## Palette (paste into `:root` of every artifact)

```css
:root {
  /* surfaces */
  --ivory:    #FAF9F5;   /* page background */
  --paper:    #FFFFFF;   /* cards, panels */
  --slate:    #141413;   /* headlines, primary text */

  /* accents */
  --clay:     #D97757;   /* primary accent (warm) */
  --clay-d:   #B85C3E;   /* clay, deeper */
  --oat:      #E3DACC;   /* secondary, mute */
  --olive:    #788C5D;   /* success, callouts */
  --rust:     #B04A3F;   /* warning, error */

  /* neutrals */
  --g100:     #F0EEE6;
  --g200:     #E6E3DA;
  --g300:     #D1CFC5;   /* default border */
  --g500:     #87867F;   /* secondary text */
  --g700:     #3D3D3A;   /* body text */

  /* type */
  --serif: ui-serif, Georgia, 'Times New Roman', Times, serif;
  --sans:  system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  --mono:  ui-monospace, 'SF Mono', Menlo, Monaco, Consolas, monospace;

  /* shape */
  --radius-panel: 12px;
  --radius-row:   8px;
  --border:       1.5px solid var(--g300);
}
```

## Typography rules

- **Headlines / H1 / hero**: `--serif`, sometimes italic (`<em>`) for the
  emphasized word — see the masthead of `index.html`.
- **Body**: `--sans`, line-height 1.55, color `--g700` on `--ivory`.
- **Eyebrows / meta / tags / monospace inline**: `--mono`, font-size 12px,
  letter-spacing 0.08-0.12em, uppercase, color `--g500`.
- **Code blocks**: `--mono`, background `--g100`, padding 16px, radius 8px,
  no language label unless syntactically necessary.

## Layout rules

- Single-column for documents, wrap at `max-width: 1120px; margin: 0 auto;`
  with horizontal padding 24-32px.
- Use cards/panels (`--paper` on `--ivory` with `--border`) for grouped
  content; do not box everything.
- Generous vertical rhythm: 56-80px between major sections.

## Anti-patterns (do not ship)

- Tailwind utility soup, Bootstrap, any CDN CSS.
- Material/iOS-style elevation shadows. Use a single 1.5px border instead.
- Heavy gradients, neon colors, dark mode by default.
- Emoji in headlines (they're fine in micro-spots — checklists, status dots).
- More than three font families. Stick to the three above.

## When to break the rules

- The user explicitly asked for a different look ("make it look like a
  Stripe doc", "use my brand colors").
- The archetype demands it (slide deck = bigger type, illustration sheet =
  white/ivory only).

Otherwise: stay in the palette. The plugin's whole value proposition is
that the artifacts look like the demos at thariqs.github.io/html-effectiveness.
