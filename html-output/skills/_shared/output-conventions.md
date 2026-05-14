# HTML output convention (shared across all html-* skills)

Every skill in this plugin produces **one self-contained `.html` file** instead
of a markdown answer. Follow this recipe exactly — it is the contract that
makes the plugin worth installing.

## 1. Pick a slug

Derive a short kebab-case slug from what the user asked for (max 6 words).
Examples:
- "weekly status for Acme engineering" → `acme-weekly-status`
- "PR writeup for the auth refactor" → `auth-refactor-pr`
- "explain HTTP/2 server push" → `http2-server-push`

If the request is vague, prefer a verb-noun: `explore-rate-limiting`,
`triage-board`, `feature-flag-editor`.

## 2. Build the path

```
./artifacts/<slug>-<YYYYMMDD-HHMMSS>.html
```

Always under `./artifacts/` relative to the current working directory. The
timestamp prevents collisions when the same archetype is generated twice in
one session. Use 24h UTC or local — `date +%Y%m%d-%H%M%S` is fine.

## 3. Ensure the folder exists

```bash
mkdir -p ./artifacts
```

If `.gitignore` does not already mention `artifacts/`, mention it **once per
session** in the chat reply (a single line: "Tip: add `artifacts/` to
`.gitignore`"). Do not nag on subsequent generations.

## 4. Write a single-file HTML

- One `<!doctype html>` document.
- One inline `<style>` block — no external CSS, no Tailwind CDN, no Google
  Fonts. System-stack fonts only (see `style-tokens.md`).
- Inline `<script>` only when the artifact is genuinely interactive (slide
  deck, click-prototype, editor UI, animation sandbox). Static reports,
  research explainers, illustrations: no JS.
- All SVG is inline. No `<img src="https://…">`. Local data-URI images
  are fine if the user supplied them, but prefer inline SVG or unicode/emoji.
- No build step. The file must work when opened from the local filesystem
  with no server.

## 5. Open it in the browser

After writing, run **one** of these via the Bash tool:

```bash
# macOS
open ./artifacts/<file>.html

# Linux
xdg-open ./artifacts/<file>.html

# Windows (rare for Claude Code today)
start ./artifacts/<file>.html
```

Detect platform once with `uname` (Darwin → `open`, Linux → `xdg-open`,
otherwise → print the path with a "open this manually" line and skip the
open command).

## 6. Reply to the user

Keep the chat reply to **one or two lines**: the file path (clickable in
most terminals) and, if relevant, one sentence on what is inside.

**Do not** repeat the contents of the HTML in markdown in the chat. That
defeats the point of the plugin. If the user asks "what did you put in
there", summarize in 2-3 sentences — do not re-render.

## 7. Iteration

When the user asks for changes ("make it pinker", "add a sparkline", "drop
section 3"), **edit the same file in place** (do not create a new
timestamped sibling on every tweak). Re-open it via the platform command
above so the browser tab can be reloaded.

If the user explicitly asks for a *variant* ("show me a darker take", "what
if it were a slide deck instead"), then write a new file with a different
slug.
