---
name: html-exploration
description: Render exploration boards, "three approaches" comparisons, visual design directions, and implementation plans as a self-contained HTML artifact in ./artifacts/ instead of a markdown list of bullets. Triggers on "explore approaches", "three options", "compare approaches", "what would it look like", "visual directions", "implementation plan", "lay out the options", "weigh the tradeoffs of", "approach A vs B", "before we pick a direction", or any request for side-by-side option comparison or step-by-step build plan.
---

# html-exploration — option comparisons + implementation plans as HTML

## When this fires

Two distinct moments collapse here, both *before* code is written:

1. **Diverge**: "show me three ways to solve this" — code approaches,
   visual directions, API shapes. The user wants to compare *options*
   side by side, with tradeoffs visible.
2. **Converge**: "now plan the build" — a step-by-step implementation
   plan with phases, ordered tasks, risk callouts, success criteria.

Both benefit from a multi-column / multi-card layout that markdown can't
do well.

If the user has already picked an approach and wants to *do* it, hand
off to the relevant downstream skill (`html-code-review` for the
resulting PR, `html-report` for status, etc.).

## Style templates

- `../../examples/01-exploration-code-approaches.html` — three code
  approaches side by side. Each column: name, one-line summary, code
  sketch, pros/cons, recommendation badge.
- `../../examples/02-exploration-visual-designs.html` — three visual
  directions. Each column: name, mood-board snippet rendered in actual
  HTML/CSS (not images), copy samples, tradeoffs.
- `../../examples/16-implementation-plan.html` — sequenced build plan.
  Phases with goals, ordered tasks, risk panels, success criteria,
  estimate.

## Output convention

Follow `../_shared/output-conventions.md`. Slug examples:
`rate-limit-three-approaches`, `auth-impl-plan-v1`,
`visual-directions-pricing-page`.

## Style tokens

Use `../_shared/style-tokens.md`. Exploration artifacts especially:
column headers in serif, pros/cons in mono with olive/rust dots,
recommended option marked with a small clay ribbon — never a giant
"WINNER" banner.

## What to include (diverge / options)

- **Frame**: 2 sentences on what the user is choosing between and what
  matters (constraints, what "good" means here).
- **3-4 columns**: each a self-contained card with name, one-line
  description, the artefact (code sketch / mockup / API table), pros
  (olive), cons (rust), best-for line.
- **Tradeoff table** (optional): rows = criteria, columns = options,
  cells = short verdict ("✓ fastest", "needs migration").
- **Recommendation**: one paragraph at the bottom; pick one, say why,
  acknowledge what you give up.
- **Clipboard-relay button on every option card** (see below).

## Clipboard relay — making the artefact actionable

Exploration was the project's **first step-2 skill**: clicking a card
feeds Claude Code's next prompt instead of just looking pretty.

Every option card MUST end with a `<button class="pick-btn">` that
writes a continuation prompt to the user's clipboard on click.

For html-exploration:
- **Where buttons go**: end of each option card, after the chips row.
- **`data-action`**: `Continue with approach NN from the exploration`
  (e.g. `"Continue with approach 02 from the exploration"`).
- **`data-payload`**: the option's name plus a one-line description.
- **`data-followup`**: `Now write the implementation plan for it.`
- **Primary highlight**: the recommended card gets `class="picked"`
  on its `<article>` — its `::after` badge then reads "Recommended"
  (the word "Pick" now belongs to the button), and its `.pick-btn`
  gets a clay fill via the shared CSS.

For the CSS, JS body and prompt-assembly logic, see
`../_shared/clipboard-relay.md`. Convergence-mode artefacts
(implementation plans) do not need the relay — they're already the
*consequence* of a pick.

The reference implementation is
`../../examples/01-exploration-code-approaches.html`.

## What to include (converge / plan)

- **Goal**: one sentence, plus a "definition of done" checklist.
- **Phases**: 3-6, each with a goal, ordered tasks, risk callouts.
  Each task: short verb-phrase, optional file path, optional est.
- **Risk panel**: top 3 risks, each with severity dot and mitigation.
- **Dependencies**: anything blocking, anything blocked.
- **Smoke-test plan**: how the user knows phase N is actually done
  before starting phase N+1.

## Anti-patterns

- Do not produce one big bullet list. Use cards / columns / phase
  blocks. That's the whole point.
- Do not invent more than 4 options. If there really is a 5th, the
  framing is wrong — ask the user.
- No emoji bullets ("✅ ❌"). Use the palette's olive/rust dots in CSS.
- Do not hide the recommendation. A diverge artifact without an
  opinionated pick is half the value.
