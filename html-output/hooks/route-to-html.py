#!/usr/bin/env python3
"""
html-output / UserPromptSubmit hook.

Regex-classifies the user's prompt against the 9 html-* archetype trigger
phrases. If a match is found, injects a system reminder that tells the agent
to use the matched skill and produce an HTML artifact (not markdown).

No model call, no network. Pure regex. Fails open — any error or no-match
results in zero behaviour change.

Bypass: prompts starting with `!`, `/`, or containing the literal token
`[no-html]` are skipped (raw shell calls, slash commands, explicit opt-out).
"""

import json
import re
import sys


# Each entry: (skill name, list of regex patterns).
# Patterns are matched case-insensitively against the prompt text.
# Keep patterns specific enough to avoid catching casual mentions in
# unrelated requests ("I want to slide into your DMs" must not fire deck).
RULES = [
    ("html-report", [
        r"\bweekly status\b",
        r"\bstatus report\b",
        r"\bstatus update\b",
        r"\bengineering update\b",
        r"\bteam (status|report|update)\b",
        r"\bmonthly review\b",
        r"\bquarterly review\b",
        r"\bincident (report|writeup|timeline)\b",
        r"\bpost[- ]?mortem\b",
        r"\bRCA\b",
        r"\boutage (summary|report|writeup)\b",
        r"\bretro (summary|report)\b",
        r"\bwhat shipped\b",
    ]),
    ("html-research", [
        r"\bexplain how .{2,60}\s+works?\b",
        r"\bdeep[- ]dive\b",
        r"\bconcept explainer\b",
        r"\bfeature explainer\b",
        r"\bfeature deep[- ]dive\b",
        r"\bresearch summary\b",
        r"\bELI5\b",
        r"\bwalk me through (?:the )?internals\b",
        r"\bhow does .{2,60}\s+(?:actually )?work\b",
        r"\binvestigate and explain\b",
        r"\bstudy notes\b",
    ]),
    ("html-code-review", [
        r"\breview (?:this |the )?(?:pr|pull request|diff)\b",
        r"\bannotate (?:this |the )?diff\b",
        r"\bdiff annotation\b",
        r"\bPR write[- ]?up\b",
        r"\bcode review\b",
        r"\bmodule map\b",
        r"\bcodebase explainer\b",
        r"\bexplain this (?:codebase|repo)\b",
        r"\barchitecture overview of (?:this |the )?repo\b",
        r"\bcode walkthrough\b",
        r"\btrace this function\b",
    ]),
    ("html-design", [
        r"\bdesign system\b",
        r"\bstyle guide\b",
        r"\bcomponent variants?\b",
        r"\bdesign tokens?\b",
        r"\bUI kit\b",
        r"\bbrand spec\b",
        r"\bcomponent library spec\b",
        r"\bspec out the \w+",
        r"\bvariants of the \w+",
    ]),
    ("html-prototype", [
        r"\binteractive (?:demo|prototype)\b",
        r"\bclickable (?:demo|prototype|flow)\b",
        r"\banimation sandbox\b",
        r"\btweak (?:this )?animation\b",
        r"\bmicro[- ]interaction\b",
        r"\bspring animation\b",
        r"\bhover (?:demo|states?)\b",
        r"\btransition (?:demo|prototype)\b",
        r"\bclick[- ]through (?:flow|prototype)\b",
        r"\bprototype (?:a |the )\w+",
    ]),
    ("html-illustration", [
        r"\bdiagram (?:this|the)\b",
        r"\bflow ?chart\b",
        r"\bsequence diagram\b",
        r"\bstate (?:machine )?diagram\b",
        r"\bdata flow diagram\b",
        r"\barchitecture (?:diagram|sketch)\b",
        r"\bsystem diagram\b",
        r"\bSVG figure\b",
        r"\brequest lifecycle\b",
        r"\billustrate (?:this|the|how)\b",
        r"\bdraw (?:the |a )(?:flow|architecture|diagram)\b",
    ]),
    ("html-deck", [
        r"\bslide deck\b",
        r"\b\d{1,2}[- ]slide(?:s)?\b",
        r"\b\d{1,2}[- ]slides? (?:on|for|about)\b",
        r"\bmake (?:me )?a deck\b",
        r"\btalk slides\b",
        r"\bkeynote[- ]style\b",
        r"\ball[- ]hands deck\b",
        r"\blightning talk\b",
        r"\bkickoff deck\b",
        r"\bpresent (?:this |that )(?:as|in)\b",
        r"\binternal pitch deck\b",
    ]),
    ("html-editor", [
        r"\btriage board\b",
        r"\bkanban (?:board )?for\b",
        r"\bfeature flag editor\b",
        r"\bflag (?:editor|admin)\b",
        r"\bprompt tuner\b",
        r"\binternal tool\b",
        r"\badmin UI\b",
        r"\bcustom editor\b",
        r"\bconfig editor for\b",
        r"\bbuild me a UI to (?:manage|edit)\b",
        r"\bdashboard for \w+",
        r"\blet me edit .{1,40}\s+visually\b",
    ]),
    ("html-exploration", [
        r"\b(?:two|three|four|five|six|seven|eight|nine|ten|\d{1,2})\s+(?:approaches|options|ways|directions|alternatives)\b",
        r"\bcompare approaches\b",
        r"\bvisual directions\b",
        r"\bimplementation plan\b",
        r"\blay out the options\b",
        r"\bweigh (?:up )?the trade[- ]?offs of\b",
        r"\bapproach [A-D] vs[. ]+approach [A-D]\b",
        r"\bbefore we pick a direction\b",
        r"\b(?:two|three|four|five|six|seven|eight|nine|ten|\d{1,2})\s+ways\s+to\b",
        r"\bwhat would (?:it|that) look like\b",
    ]),
]


REMINDER_TEMPLATE = (
    "[html-output hook] User's prompt matches the `{skill}` archetype "
    "(matched pattern: {pattern!r}).\n\n"
    "Use the `{skill}` skill from the html-output plugin and produce a "
    "self-contained HTML artifact instead of a markdown answer. Recipe:\n"
    "  1. Read examples in plugins examples/ to absorb style.\n"
    "  2. Write a single self-contained .html to "
    "./artifacts/<slug>-<YYYYMMDD-HHMMSS>.html (mkdir -p first).\n"
    "  3. Open it via `open` (macOS) or `xdg-open` (Linux).\n"
    "  4. Reply with one line: the file path. Do NOT repeat the content "
    "as markdown.\n\n"
    "Override: if the user explicitly asked for plain text / markdown, "
    "ignore this reminder."
)


def classify(prompt: str):
    """Return (skill, matched_pattern) or (None, None)."""
    lower = prompt.lower()
    for skill, patterns in RULES:
        for pat in patterns:
            if re.search(pat, lower, re.IGNORECASE):
                return skill, pat
    return None, None


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    prompt = (data.get("prompt") or "").strip()
    if not prompt:
        sys.exit(0)

    # Opt-out clauses
    if prompt.startswith(("!", "/")) or "[no-html]" in prompt.lower():
        sys.exit(0)

    skill, pattern = classify(prompt)
    if not skill:
        sys.exit(0)

    reminder = REMINDER_TEMPLATE.format(skill=skill, pattern=pattern)

    # Emit additionalContext via the documented hookSpecificOutput shape.
    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": reminder,
        }
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
