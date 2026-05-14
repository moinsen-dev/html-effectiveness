# html-effectiveness — local working notes

> These notes live in the repo, not in the public README. They capture the *real* ambition
> of the project plus how we've agreed to work on it. The public pitch on `README.md` and
> `index.html` still describes step 1 only — that stays as-is until step 2 has a working
> prototype to point at.

## 1. North star

The project is **not** "Claude renders answers as HTML instead of markdown." That's the
*mechanism*.

The project **is**: *Claude's answers become 2-way interactive surfaces*. Every artefact
is a small custom UI through which the user **clicks the next prompt** instead of typing
it. The HTML is an input method, not just an output channel.

- **Step 1 — render** (mostly done): 20 demos + 9 skills + 1 hook + `/html` command.
- **Step 2 — feedback loop** (the actual unsolved problem): clicks in the artefact feed
  Claude Code's next continuation.

Step 1 without step 2 is a brochure. Step 2 is *der eigentliche Gag*.

## 2. The gap (audit, 14 May 2026)

The "interactive" examples are pseudo-interactive — they look clickable but nothing
flows back to Claude:

- `18-editor-triage-board.html` · `19-editor-feature-flags.html` · `20-editor-prompt-tuner.html` —
  each 250–390 lines of JS. Drag-to-move, inline-edit, dependency warnings. But every
  action terminates at `localStorage` or `navigator.clipboard.writeText`. Zero `fetch`,
  XHR, WebSocket, `postMessage`, or file write anywhere in the 20 demos.
- `07-prototype-animation.html` · `08-prototype-interaction.html` — pure CSS-var swaps.
- `01-exploration-code-approaches.html` and our `promote-html-effectiveness-*.html` —
  the "Pick" / recommendation badge is decorative, not actionable.

The anti-pattern is currently *codified* in `html-output/skills/html-editor/SKILL.md`
(lines 67–68):

> No backend calls. Everything happens in the page; `localStorage` is the store; "save"
> means export.

That line will need to evolve once step 2 has a chosen mechanism. Until then, leave it —
it's still correct for the demos that ship today.

## 3. Candidate mechanisms for step 2 (open question)

Three options on the table. Not picking one yet — that's a follow-up build session.

- **Clipboard relay** (lo-fi, ~1 evening). Every actionable element writes a Claude-ready
  follow-up prompt to clipboard with a visible affordance ("Click to copy a continuation
  prompt for Claude"). User pastes. The editor demos already prove the wiring works —
  promote it from "Copy JSON" curiosity to first-class pattern across all archetypes.
  *Pros*: works on every machine today, no infra, no port collisions. *Cons*: manual
  paste step, no closed loop, easy to forget.

- **Local broker file** (mid-fi, ~1 day). Plugin spins up a tiny local HTTP server when
  an artefact opens (or when `/html` runs). Clicks POST to it; the server writes
  `./artifacts/.next-prompt.txt`. Plugin ships a `/html-continue` slash command that
  pops the file as the next instruction. *Pros*: structured, scriptable, the user just
  types `/html-continue`. *Cons*: server lifecycle, port collisions, slightly more setup.

- **Hook bridge** (hi-fi, research territory). SSE / WebSocket between the artefact and
  a Claude Code session that's actively listening — the click *is* the prompt, no manual
  step. Requires plumbing Claude Code's hook system in a way that doesn't trivially exist
  today (UserPromptSubmit is initiated by the user, not by an external HTML page).
  *Pros*: the real two-way version. *Cons*: needs investigation, possibly Anthropic-side
  support.

**Lean** (to be confirmed when we actually build): start with clipboard relay because the
editor examples already prove every prerequisite. One evening turns the project from
"renders HTML" to "renders HTML that you click to continue." Mid- and hi-fi can layer on
top later without breaking the lo-fi pattern.

## 4. How we work in this repo

Captured from the session that produced this doc:

- **Bauen statt Planen.** Anything KI-codbar gets built immediately. The artefact is the
  reality-check. Memos cost more than features.
- **Auto-flow.** Hook fires → I write the HTML → I run `open` → I reply with the path.
  **Never re-render the contents as markdown in chat.** That defeats the whole point.
- **Surgical fixes.** No "while I'm here" cleanups. Example from this session: the regex
  word-vs-digit gap got fixed exactly where it bit ("3 approaches"), not preemptively
  across all patterns.
- **Style discipline.** Palette + type from `html-output/skills/_shared/style-tokens.md`
  only. Cards / columns over bullet walls. Opinionated pick at the bottom of every
  exploration artefact — never hide the recommendation.
- **Examples are the spec.** Every new skill output references an example at the repo
  root. Don't drift from the visual language.
- **Plugin-works checklist.** Before claiming "the plugin works": (1) `installed_plugins.json`
  has the entry, (2) cache file is executable + matches repo source, (3) at least one
  trigger phrase fires the hook end-to-end, (4) `open` returns exit 0.

## 5. Status snapshot

- Marketplace: `moinsen-dev/html-effectiveness` on GitHub.
- Plugin: `html-output@html-effectiveness` v0.2.0.
- 9 skills + 1 `/html` command + 1 UserPromptSubmit hook — installed and verified.
- Regex covers digit-and-word forms for "N approaches / options / ways / directions /
  alternatives" and "N ways to …" (fixed 14 May 2026 after a real-traffic miss on
  `"3 approaches"`). Same patch applied to the install cache for immediate effect.
- Open gap: the step-2 interactivity bridge.

## 6. What this doc is NOT

- Not a roadmap. Not a feature list. Not a public claim.
- The directional north star + working agreements only.
- Public surfaces (`README.md`, `index.html`) keep describing step 1 until step 2 has
  a prototype worth pointing at.
