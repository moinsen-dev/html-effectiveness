# html-effectiveness

> *Twenty self-contained `.html` files an agent produced instead of a wall of
> markdown — plus a Claude Code plugin that makes your agent do the same.*

This repo is **two things at once**:

1. **A static showcase** — 20 HTML demos arguing that, for a wide class of
   tasks, an LLM should answer with rich, opinionated HTML rather than
   markdown. Live at
   **[thariqs.github.io/html-effectiveness](https://thariqs.github.io/html-effectiveness/)**.

2. **A Claude Code marketplace** — install the `html-output` plugin and your
   own Claude Code starts answering with HTML artifacts (saved to
   `./artifacts/`, opened in the browser) for the same categories.

The static demos are the evidence. The plugin is the consequence.

## Try the demos

Just open `index.html` locally or visit
[thariqs.github.io/html-effectiveness](https://thariqs.github.io/html-effectiveness/).
Each card on that page is a single `.html` file — open any of them.

The 20 examples cluster into 9 archetypes:

| # | Archetype | Files |
|---|---|---|
| 1 | Exploration & Planning | `01`, `02`, `16` |
| 2 | Code Review & Understanding | `03`, `04`, `17` |
| 3 | Design | `05`, `06` |
| 4 | Prototyping | `07`, `08` |
| 5 | Illustrations & Diagrams | `10`, `13` |
| 6 | Decks | `09` |
| 7 | Research & Learning | `14`, `15` |
| 8 | Reports | `11`, `12` |
| 9 | Custom Editing Interfaces | `18`, `19`, `20` |

## Install the Claude Code plugin

```bash
# inside Claude Code
/plugin marketplace add moinsen-dev/html-effectiveness
/plugin install html-output@html-effectiveness
```

Then ask Claude any of these — note that you do *not* type "as HTML":

- "Write me a weekly status report for the Acme engineering team."
- "Explain how HTTP/2 server push works."
- "Three approaches for rate-limiting our public API, with tradeoffs."
- "Design system for a fintech app — colours, type, primitives."
- "Slide deck: why HTML beats markdown for LLM output."
- "Internal tool: feature-flag editor for these 3 flags: …"

Each lands as `./artifacts/<slug>-<timestamp>.html` and pops open in your
browser.

### How the routing works

A `UserPromptSubmit` hook (`html-output/hooks/route-to-html.py`) sits in front
of every prompt:

- Regex-classifies your prompt against ~85 trigger phrases drawn from the 9
  `html-*` skill descriptions.
- On match: injects a system reminder telling the agent **which** skill to
  use and the write-and-open recipe. Pure regex, no model call, no network,
  fails open.
- Bypassed automatically for prompts starting with `!` or `/`, or containing
  the literal token `[no-html]` if you want a one-off plain answer.

That's why the plugin works without you typing "as HTML" — the hook is the
router, the skills are the templates.

For the full plugin readme — skill list, anti-patterns, customisation — see
[`html-output/README.md`](./html-output/README.md).

## Repo layout

```
.
├── .claude-plugin/marketplace.json   ← Claude Code marketplace manifest
├── html-output/                      ← the plugin (skills + command + hook + examples)
│   ├── .claude-plugin/plugin.json
│   ├── README.md                     ← plugin documentation
│   ├── commands/html.md              ← /html slash command
│   ├── hooks/
│   │   ├── hooks.json                ← UserPromptSubmit registration
│   │   └── route-to-html.py          ← regex router → skill picker
│   ├── examples/01-…html  …  20-…html
│   └── skills/
│       ├── _shared/{output-conventions,style-tokens}.md
│       └── html-{report,research,code-review,design,prototype,
│                  illustration,deck,editor,exploration}/SKILL.md
├── 01-…html  …  20-…html             ← static demos (also live on Pages)
├── index.html                        ← gallery page
└── README.md                         ← you are here
```

The 20 demo HTMLs exist twice: at the repo root (Pages) and under
`html-output/examples/` (self-contained plugin tree). They are byte-identical
copies; keep them in sync if you edit any.

## License

MIT.

## Credits

Demos by [Thariq Shihipar](https://thariqs.github.io/html-effectiveness/).
Marketplace + plugin scaffolding follows the Claude Code plugin convention.
