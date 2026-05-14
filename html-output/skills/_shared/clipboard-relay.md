# Clipboard relay (shared step-2 pattern)

Every html-* artefact has at least one **action point** — an element
the user can click to say "yes, do this next." This file specifies how
that click feeds Claude Code's next prompt.

The mechanism is lo-fi by design: a click writes a continuation prompt
to the user's clipboard. The user pastes it into Claude Code. The next
turn begins from the chosen branch.

The first skill to ship this is `html-exploration` (see
`../../examples/01-exploration-code-approaches.html` for the working
reference). All other html-* skills follow the same pattern — only the
`data-action` / `data-payload` / `data-followup` strings differ per
archetype.

## Button HTML

Use a real `<button>` (not a styled div), one per action point:

```html
<button class="pick-btn" type="button"
  data-action="Continue with approach 02 from the exploration"
  data-payload="Custom useDebounce hook — shared src/hooks/ module"
  data-followup="Now write the implementation plan for it.">
  <span>Continue with approach 02</span>
  <span class="arrow">→</span>
</button>
```

| attribute | purpose |
|---|---|
| `data-action` | The verb the prompt opens with. Archetype-specific (see each skill's recipe). |
| `data-payload` | A one-line summary of *what* is being chosen — enough for Claude to act without re-reading the artefact. |
| `data-followup` | *(optional)* A trailing sentence that tells Claude what to do next ("Now write the implementation plan", "Show me the diff", etc.). Omit for archetypes where the action verb is self-explanatory. |

The button label visible to the user can be shorter than `data-action`
(e.g. "Continue with approach 02" while `data-action` reads "Continue
with approach 02 from the exploration").

## CSS

Variable names tolerate both the new tokens (`--paper`, `--g100`,
`--g300`, `--slate`, `--ivory`, `--clay`) and the older example tokens
(`--white`, `--gray-150`, `--gray-300`). Use whatever the host
artefact already defines.

```css
.pick-btn {
  margin-top: 4px;
  background: var(--paper, var(--white, #fff));
  border: 1.5px solid var(--g300, var(--gray-300, #D1CFC5));
  color: var(--slate, #141413);
  font-family: var(--mono);
  font-size: 12px;
  letter-spacing: 0.04em;
  padding: 11px 16px;
  border-radius: 8px;
  cursor: pointer;
  text-align: left;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  transition: border-color 0.15s ease, background 0.15s ease, color 0.15s ease;
  width: 100%;
}
.pick-btn:hover {
  border-color: var(--clay);
  color: var(--clay);
  background: var(--g100, var(--gray-150, #F0EEE6));
}
.pick-btn:active { transform: translateY(1px); }
.pick-btn .arrow { display: inline-block; transition: transform 0.15s ease; }
.pick-btn:hover .arrow { transform: translateX(3px); }

/* Primary variant for the recommended/default action.
   Apply via `class="primary"` on the button OR `class="picked"` on a parent. */
.pick-btn.primary,
.picked .pick-btn {
  background: var(--clay);
  border-color: var(--clay);
  color: var(--paper, var(--white, #fff));
}
.pick-btn.primary:hover,
.picked .pick-btn:hover {
  filter: brightness(0.92);
  color: var(--paper, var(--white, #fff));
}

.toast {
  position: fixed;
  bottom: 28px;
  left: 50%;
  transform: translateX(-50%) translateY(16px);
  background: var(--slate);
  color: var(--ivory);
  font-family: var(--mono);
  font-size: 12px;
  line-height: 1.5;
  padding: 12px 18px;
  border-radius: 10px;
  opacity: 0;
  transition: opacity 0.25s ease, transform 0.25s ease;
  pointer-events: none;
  max-width: 520px;
  text-align: center;
  z-index: 100;
  box-shadow: 0 4px 16px rgba(20, 20, 19, 0.15);
}
.toast.show { opacity: 1; transform: translateX(-50%) translateY(0); }
.toast .kbd {
  background: rgba(255,255,255,0.12);
  padding: 1px 6px;
  border-radius: 4px;
  margin: 0 2px;
}
```

## JS (single inline `<script>` before `</body>`)

```html
<script>
  (function () {
    function buildPrompt(action, payload, followup) {
      var base = action + (payload ? ': "' + payload + '".' : '.');
      return followup ? base + ' ' + followup : base;
    }

    function writeToClipboard(text) {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        return navigator.clipboard.writeText(text);
      }
      return new Promise(function (resolve, reject) {
        try {
          var ta = document.createElement('textarea');
          ta.value = text;
          ta.setAttribute('readonly', '');
          ta.style.position = 'fixed';
          ta.style.opacity = '0';
          document.body.appendChild(ta);
          ta.select();
          document.execCommand('copy');
          ta.remove();
          resolve();
        } catch (err) { reject(err); }
      });
    }

    var toastEl = null, toastTimer = null;
    function showToast(html) {
      if (!toastEl) {
        toastEl = document.createElement('div');
        toastEl.className = 'toast';
        toastEl.setAttribute('role', 'status');
        toastEl.setAttribute('aria-live', 'polite');
        document.body.appendChild(toastEl);
      }
      toastEl.innerHTML = html;
      requestAnimationFrame(function () { toastEl.classList.add('show'); });
      clearTimeout(toastTimer);
      toastTimer = setTimeout(function () { toastEl.classList.remove('show'); }, 3200);
    }

    document.addEventListener('click', function (e) {
      var btn = e.target.closest('.pick-btn');
      if (!btn) return;
      e.preventDefault();
      var action = btn.dataset.action || 'Continue';
      var payload = btn.dataset.payload || '';
      var followup = btn.dataset.followup || '';
      writeToClipboard(buildPrompt(action, payload, followup)).then(
        function () {
          showToast('Copied prompt. Paste into Claude Code <span class="kbd">⌘V</span> <span class="kbd">↵</span> to continue.');
        },
        function () {
          showToast('Clipboard blocked — open browser console to copy manually.');
        }
      );
    });
  })();
</script>
```

## `data-action` template per archetype

Each skill's SKILL.md specifies its own templates. Quick reference:

| Skill | `data-action` template | typical `data-followup` |
|---|---|---|
| `html-exploration` | `Continue with approach NN from the exploration` | `Now write the implementation plan for it.` |
| `html-report` | `Drill into "<section>" from the report` | `Show me the next-level detail.` |
| `html-research` | `Go deeper on "<concept>" from the research` | `Show one concrete example with code.` |
| `html-code-review` | `Apply review finding "<title>"` | `Write the actual diff.` |
| `html-design` | `Implement variant "<name>" from the design system` | `Write the component code.` |
| `html-prototype` | `Adopt the "<config>" configuration from the prototype` | `Write production-ready CSS/JSX.` |
| `html-illustration` | `Explain "<node>" from the diagram in depth` | `Show the code that implements it.` |
| `html-deck` | `Expand slide N "<title>" into a full page` | `Use the html-research style.` |
| `html-editor` | `Apply this editor state to the codebase` | *(payload is a JSON snippet)* |

## Where to put the button

One per action point — never blanket. Decide per archetype:

- **Choice surfaces** (exploration, design variants, prototype presets, deck slide selection, editor toggles): one button per option.
- **Drill-down surfaces** (report, research, code-review findings): one button per item the reader could plausibly want to expand.
- **Pure information surfaces** (illustration nodes, status report "what shipped" list): button only if the item is genuinely something to act on, not just to read.

If you'd be hard-pressed to write a sensible `data-payload` for an
element, it probably doesn't need a button.

## Recommended/default highlighting

If the artefact has an opinionated default (exploration always does;
reports often do), give that one button `class="primary"` (or its
parent `class="picked"`). Use one — not both — per artefact, and only
on the single best option. The badge `::after { content: 'Recommended' }`
on `.picked` is the visual cousin.

## Anti-patterns

- Don't add a button on every item if most items aren't choices. Buttons
  should be rare and meaningful, not decorative.
- Don't write the payload with placeholders (`<your-choice>`) — fill it
  at generation time so the user pastes a ready-to-go instruction.
- Don't open new tabs / navigate / call backends. Clipboard only.
- Don't suppress the toast — it's the only feedback the user gets that
  the click worked.
